
````markdown
# 🎛️ Générateur de Patterns MIDI – FL Studio Ready

**Auteur :** Walid Filali (`serolyn`)  
**Description :** Ce repo propose deux scripts Python permettant de générer automatiquement des patterns MIDI compatibles FL Studio (ou tout autre DAW).  
- `beatmaker_pattern.py` – Générateur de patterns mélodiques aléatoires (basses, leads, etc.).
- `drum_generator.py` – Générateur de patterns drums aléatoires (kick, snare, hats, crash) au format MIDI (canal 10).

---

## 🚀 Utilisation rapide

### 1. Prérequis

- **Python 3.x** (recommandé 3.8+)
- **[mido](https://pypi.org/project/mido/)**  
  Installer via :
  ```bash
  python -m pip install mido
````

### 2. Générer un pattern mélodique

```bash
python beatmaker_pattern.py
```

* Fichier généré : `random_pattern.mid`
* Modifie la gamme, la durée ou la densité directement dans le script.

### 3. Générer un pattern drums

```bash
python drum_generator.py --bars 8 --beats 4 --subdiv 4 --tempo 100 --out my_drums.mid
```

* Paramètres customisables via la ligne de commande.

---

## 🎹 Import dans FL Studio

* **Glisse-dépose** simplement le `.mid` dans un Channel MIDI, le Piano Roll, ou l’Arrangement de FL Studio.
* Par défaut, les notes drums sont mappées sur le channel 10 (GM Standard Drum Map).

---

## ⚙️ Scripts inclus

### `beatmaker_pattern.py`

* Génère un pattern mélodique aléatoire sur 4 mesures (modifiable).
* Notes dans la gamme de Do majeur (par défaut).
* Vélocité humanisée, subdivisions réglables.
* Compatible avec n’importe quel VSTi ou synth.

### `drum_generator.py`

* Génère un pattern drums (kick, snare, hi-hat, crash) réaliste.
* Probabilités d’apparition humanisées pour chaque élément.
* Paramètres CLI : nombre de mesures, subdivisions, tempo, fichier de sortie.

---

## 🧩 Customisation

* Modifie la gamme, les notes, les instruments ou la densité dans les scripts selon tes besoins.
* Pour une autre gamme ou d’autres instruments, adapte la variable `SCALE_NOTES` ou les numéros de notes MIDI.

---

## 📄 Licence

MIT – libre d’usage, modifiez, partagez.

---

> Pour toute question ou nouvelle feature, ouvrez une issue ou contactez-moi sur GitHub.

```

---
```
