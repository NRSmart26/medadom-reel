"""Controle de la voix d'un reel Medadom, sans pouvoir l'ecouter : transcription Scribe comparee au texte lu,
puis un extrait sonore des passages a risque (DCI, sigles, mots longs), a faire ecouter a Romain.

    python controle_voix.py reels/<reel>.py "mot ou debut de passage" [...]

Pour chaque prise, la liste des ecarts entre ce qui devait etre lu et ce que Scribe a entendu. Les sigles
epeles (« E.C.B.U. » / « ECBU ») et les nombres en lettres different toujours : ils ne comptent pas. Un mot
deforme (« bandette » pour « bandelette », « pivmeciliname ») est a faire ecouter.
Scribe « corrige » souvent une mauvaise prononciation (« consulpation » transcrit « consultation ») : la
transcription ne remplace pas l'ecoute, d'ou l'extrait, depose dans SORTIE (extrait_voix_mots_difficiles.mp3)."""
import difflib
import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

ICI = Path(__file__).resolve().parent
sys.path.insert(0, str(ICI))
import fabrique
import voix

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def mots(s):
    s = re.sub(r"\[[^\]]*\]", " ", s)
    s = unicodedata.normalize("NFKD", s.lower().replace("’", "'"))
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    return re.findall(r"[a-z0-9]+", s)


reel = fabrique.charger(sys.argv[1])
passages = sys.argv[2:]
prises = fabrique.prises_de(reel, False, ICI / "travail" / reel.NOM / "voix")
segments = []
for n, pr in enumerate(prises):
    al = json.loads(pr["mp3"].with_suffix(".json").read_text(encoding="utf-8"))
    al = al.get("alignment", al)
    lu = "".join(al["characters"])
    entendu = voix.transcription(pr["mp3"])
    a, b = mots(pr["texte"]), mots(entendu)
    print(f"== prise {n + 1} ({pr['mp3'].name}) : {len(a)} mots attendus, {len(b)} transcrits")
    for op, a0, a1, b0, b1 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if op != "equal":
            print(f"  {op:8} attendu « {' '.join(a[a0:a1])} »  entendu « {' '.join(b[b0:b1])} »")
    deb, fin = al["character_start_times_seconds"], al["character_end_times_seconds"]
    for p in passages:
        i = pr["texte"].find(p)
        if i < 0:
            continue
        j = i + len(p) - 1
        segments.append((pr["mp3"], max(0.0, deb[i] - 0.3), min(fin[j] + 0.35, pr["coupe"])))
if segments:
    entrees, filtres = [], []
    for k, (mp3, t0, t1) in enumerate(segments):
        entrees += ["-i", str(mp3)]
        filtres.append(f"[{k}:a]atrim={t0:.2f}:{t1:.2f},asetpts=PTS-STARTPTS,apad=pad_dur=0.5[s{k}]")
    filtres.append("".join(f"[s{k}]" for k in range(len(segments))) +
                   f"concat=n={len(segments)}:v=0:a=1,atempo={fabrique.TEMPO},loudnorm=I=-16:TP=-1.5")
    sortie = Path(reel.SORTIE) / "extrait_voix_mots_difficiles.mp3"
    Path(reel.SORTIE).mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", *entrees, "-filter_complex", ";".join(filtres),
                    "-c:a", "libmp3lame", "-b:a", "192k", str(sortie)], check=True)
    print(f"extrait : {sortie} ({len(segments)} passages)")
print(f"credits ElevenLabs restants : {voix.credits()}")
