"""Voix de synthese ElevenLabs (modele v3), avec horodatage par caractere et cache.

Une prise deja payee n'est jamais regeneree : elle est gardee dans travail/<reel>/voix/, sous une cle tiree
du texte lu, de la voix et des reglages. La cle est calculee comme dans l'outil des reels LCDG (lcdg/voix.py) :
une prise faite par l'un se retrouve dans l'autre si on copie ses deux fichiers (.mp3 et .json).

La cle d'API se lit dans .env (ELEVENLABS_API_KEY), jamais affichee."""
import base64
import hashlib
import json
import os
from pathlib import Path

import requests

API = "https://api.elevenlabs.io/v1"
ICI = Path(__file__).resolve().parent

# voix de la bibliotheque ElevenLabs (comediennes enregistrees en studio, sans emplacement de voix)
EMILIE = "d3AXX0BlgJHYFCuH9X88"      # « vraiment tres pro » (Romain, 28/10/2026) : la voix des reels Medadom
JEANNE = "txtf1EDouKke753vN8SL"      # plus jeune, plus « punchy »
GUILLAUME = "3HZyQcLKlT0a3RDeXVsP"   # homme, pose
MODELE = "eleven_v3"
REGLAGES_V3 = {"stability": 0.5, "similarity_boost": 0.75}   # v3 : le jeu passe par les [indications]


def _cle():
    if not os.environ.get("ELEVENLABS_API_KEY"):
        env = ICI / ".env"
        if env.exists():
            for ligne in env.read_text(encoding="utf-8").splitlines():
                if ligne.startswith("ELEVENLABS_API_KEY="):
                    os.environ["ELEVENLABS_API_KEY"] = ligne.split("=", 1)[1].strip().strip('"')
    cle = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    if not cle:
        raise SystemExit("[!] ELEVENLABS_API_KEY absente : la mettre dans .env (ELEVENLABS_API_KEY=...)")
    return cle


def corps(texte, modele=MODELE, reglages=None):
    return {"text": texte, "model_id": modele, "voice_settings": reglages or REGLAGES_V3}


def chemins(texte, voice_id, dossier, modele=MODELE, reglages=None):
    """(mp3, alignement json) de ce texte lu par cette voix, dans le cache."""
    cle = hashlib.sha256(json.dumps([voice_id, corps(texte, modele, reglages)], sort_keys=True,
                                    ensure_ascii=False).encode("utf-8")).hexdigest()[:16]
    return Path(dossier) / f"{cle}.mp3", Path(dossier) / f"{cle}.json"


def synthese(texte, voice_id, dossier, modele=MODELE, reglages=None):
    """(mp3, alignement par caractere) du texte lu, depuis le cache s'il existe."""
    mp3, js = chemins(texte, voice_id, dossier, modele, reglages)
    if mp3.exists() and js.exists():
        return mp3, json.loads(js.read_text(encoding="utf-8"))
    Path(dossier).mkdir(parents=True, exist_ok=True)
    r = requests.post(f"{API}/text-to-speech/{voice_id}/with-timestamps", params={"output_format": "mp3_44100_128"},
                      headers={"xi-api-key": _cle()}, json=corps(texte, modele, reglages), timeout=300)
    if not r.ok:
        raise SystemExit(f"[!] ElevenLabs a refuse la generation ({r.status_code}) : {r.text[:300]}")
    reponse = r.json()
    alignement = reponse["alignment"]
    if len(alignement["characters"]) != len(texte):
        raise SystemExit("[!] ElevenLabs : l'horodatage ne correspond pas au texte envoye")
    mp3.write_bytes(base64.b64decode(reponse["audio_base64"]))
    js.write_text(json.dumps(alignement, ensure_ascii=False), encoding="utf-8")
    return mp3, alignement


def credits():
    """Credits ElevenLabs restants ce mois-ci."""
    j = requests.get(f"{API}/user/subscription", headers={"xi-api-key": _cle()}, timeout=30).json()
    return j["character_limit"] - j["character_count"]


def transcription(mp3):
    """Transcription Scribe (incluse dans le compte gratuit), gardee a cote du mp3."""
    cache = Path(mp3).with_suffix(".transcription.json")
    if not cache.exists():
        with open(mp3, "rb") as f:
            r = requests.post(f"{API}/speech-to-text", headers={"xi-api-key": _cle()},
                              data={"model_id": "scribe_v1", "language_code": "fra", "tag_audio_events": "false"},
                              files={"file": (Path(mp3).name, f, "audio/mpeg")}, timeout=300)
        if not r.ok:
            raise SystemExit(f"[!] transcription refusee ({r.status_code}) : {r.text[:200]}")
        cache.write_text(json.dumps(r.json(), ensure_ascii=False), encoding="utf-8")
    return json.loads(cache.read_text(encoding="utf-8"))["text"]
