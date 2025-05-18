
"""
drum_generator.py

Générateur de pattern de batterie MIDI aléatoire.
Utilise `mido` pour créer un fichier MIDI standard que

vous pouvez lire avec un séquenceur ou un DAW.
Le pattern est basé sur une grille de 4/4 avec des subdivisions
de 16e notes. Il utilise des notes MIDI standard pour
représenter les sons de batterie.
Les notes MIDI utilisées sont :
- 36 : grosse caisse (kick)
- 38 : caisse claire (snare)
- 42 : charleston fermé (closed hi-hat)
- 46 : charleston ouvert (open hi-hat)
- 49 : cymbale crash (crash cymbal)
Le pattern est généré aléatoirement en fonction de la configuration 
spécifiée par l'utilisateur.
Le fichier MIDI généré peut être ouvert dans un logiciel de musique
comme FL Studio, Ableton Live, Logic Pro, etc.
Vous pouvez l'ecouter le fichier sur votre ordinateur en double-cliquant dessus.
Usage :
    python drum_generator.py [--bars 4] [--beats 4] [--subdiv 4] [--tempo 120]
"""

import argparse
import random
from mido import Message, MidiFile, MidiTrack, MetaMessage, bpm2tempo

# ——— Configuration de base ——————————————————————————————————————
DEFAULT_TEMPO    = 120   # BPM
DEFAULT_BARS     = 4     # nombre de mesures
DEFAULT_BEATS    = 4     # temps par mesure
DEFAULT_SUBDIV   = 4     # subdivisions par temps (16e = 4)
TPB              = 480   # ticks par noire
DRUM_CHANNEL     = 9     # canal MIDI 10 (indexé à 0)
OUTPUT_FILENAME  = "drum_pattern.mid"

# MIDI notes standard percussion
NOTE_KICK      = 36  # Acoustic Bass Drum
NOTE_SNARE     = 38  # Acoustic Snare
NOTE_CLOSED_HH = 42  # Closed Hi-Hat
NOTE_OPEN_HH   = 46  # Open Hi-Hat
NOTE_CRASH     = 49  # Crash Cymbal 1
# ——————————————————————————————————————————————————————————————————

def generate_drum_pattern(bars, beats, subdiv, tempo):
    mid = MidiFile(ticks_per_beat=TPB)
    track = MidiTrack()
    mid.tracks.append(track)

    # Tempo meta message
    track.append(MetaMessage('set_tempo', tempo=bpm2tempo(tempo), time=0))

    ticks_per_step = TPB // subdiv
    total_steps = bars * beats * subdiv
    time_acc = 0

    for step in range(total_steps):
        # On transforme step en position dans mesure
        bar_pos = step % (beats*subdiv)
        is_downbeat = (bar_pos % subdiv == 0)  # début de chaque temps
        is_bar_start = (bar_pos == 0)          # tout début de mesure

        # Kick probabilité plus forte sur les temps 1er et 3e
        if is_downbeat and random.random() < (0.9 if (bar_pos//subdiv)%beats in (0,2) else 0.3):
            track.append(Message('note_on', note=NOTE_KICK, velocity=100,
                                 time=time_acc, channel=DRUM_CHANNEL))
            track.append(Message('note_off', note=NOTE_KICK, velocity=0,
                                 time=ticks_per_step, channel=DRUM_CHANNEL))
            time_acc = 0

        # Snare probabilité sur 2e et 4e temp
        if is_downbeat and (bar_pos//subdiv)%beats in (1,3) and random.random() < 0.8:
            track.append(Message('note_on', note=NOTE_SNARE, velocity=100,
                                 time=time_acc, channel=DRUM_CHANNEL))
            track.append(Message('note_off', note=NOTE_SNARE, velocity=0,
                                 time=ticks_per_step, channel=DRUM_CHANNEL))
            time_acc = 0

        # Hi-Hat fermée se joue à chaque subdivision hautement probable
        if random.random() < 0.7:
            track.append(Message('note_on', note=NOTE_CLOSED_HH, velocity=random.randint(70, 110),
                                 time=time_acc, channel=DRUM_CHANNEL))
            track.append(Message('note_off', note=NOTE_CLOSED_HH, velocity=0,
                                 time=ticks_per_step, channel=DRUM_CHANNEL))
            time_acc = 0

        # Crash: seulement au début des mesures
        if is_bar_start and random.random() < 0.3:
            track.append(Message('note_on', note=NOTE_CRASH, velocity=120,
                                 time=time_acc, channel=DRUM_CHANNEL))
            track.append(Message('note_off', note=NOTE_CRASH, velocity=0,
                                 time=ticks_per_step*2, channel=DRUM_CHANNEL))
            time_acc = 0

        # Avance le temps si rien déclenché
        time_acc += ticks_per_step

    # End 
    track.append(MetaMessage('end_of_track', time=1))
    return mid

def main():
    parser = argparse.ArgumentParser(description="Générateur de pattern de batterie MIDI")
    parser.add_argument("--bars",   type=int, default=DEFAULT_BARS,  help="Nombre de mesures")
    parser.add_argument("--beats",  type=int, default=DEFAULT_BEATS, help="Temps par mesure")
    parser.add_argument("--subdiv", type=int, default=DEFAULT_SUBDIV,help="Subdivisions par temps")
    parser.add_argument("--tempo",  type=int, default=DEFAULT_TEMPO, help="Tempo (BPM)")
    parser.add_argument("--out",    type=str, default=OUTPUT_FILENAME, help="Fichier de sortie MIDI")
    args = parser.parse_args()

    mid = generate_drum_pattern(args.bars, args.beats, args.subdiv, args.tempo)
    mid.save(args.out)
    print(f"✅ Fichier MIDI généré : {args.out}")

if __name__ == "__main__":
    main()
