#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
publier.py - Met en ligne la dernière version du CRM BF Conseil : https://crm.bfconseil-lyon.com/

Utilisation (dans ce dossier), après un « py -3 build.py » dans facturation-bf-conseil :
    py -3 publier.py

Copie facturation-bf-conseil/en_ligne/ ici, vérifie qu'aucune donnée personnelle ne s'y trouve,
puis envoie sur GitHub (dépôt belelhanachi-Hub/crm). Le site se met à jour en une à deux minutes.
Les données ne sont jamais ici : elles sont dans le Google Drive BF Conseil.
"""
import os
import shutil
import subprocess
import sys
from datetime import datetime

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ICI = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(ICI, "..", "facturation-bf-conseil", "en_ligne")
FICHIERS = ["index.html", "manifest.webmanifest", "icone-180.png", "icone-192.png", "icone-512.png"]
CONFIDENTIEL = ("FR76", "929 011 369", "Jules Favre", "06 69 99 96 05", "GROUPE ALTERNANCE", "SELFORM", "ADMTC", "HOURIA", "YOUNES")


def git(*args):
    return subprocess.run(["git", *args], cwd=ICI, text=True, capture_output=True)


def main():
    for nom in FICHIERS:
        source = os.path.join(SOURCE, nom)
        if not os.path.exists(source):
            sys.exit("ERREUR : %s introuvable. Lance d'abord py -3 build.py dans facturation-bf-conseil." % source)
        shutil.copyfile(source, os.path.join(ICI, nom))
    with open(os.path.join(ICI, "index.html"), encoding="utf-8") as f:
        page = f.read()
    for interdit in CONFIDENTIEL:
        if interdit in page:
            sys.exit("ERREUR de confidentialité : « %s » se trouve dans la page. Rien n'a été envoyé." % interdit)
    git("add", *FICHIERS)
    if not git("status", "--porcelain").stdout.strip():
        print("Rien de nouveau : le CRM en ligne est déjà à jour.")
        return
    git("commit", "-m", "Mise à jour du CRM du %s" % datetime.now().strftime("%d/%m/%Y à %Hh%M"))
    envoi = git("push")
    if envoi.returncode != 0:
        sys.exit("ERREUR pendant l'envoi sur GitHub :\n" + envoi.stderr)
    print("Envoyé. Le CRM sera à jour dans une à deux minutes : https://crm.bfconseil-lyon.com/")


if __name__ == "__main__":
    main()
