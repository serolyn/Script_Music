
"""

Génère un pattern MIDI aléatoire compatible FL Studio. Sur ordinateur, appuyez pour écouter les notes générées au piano dans votre lecteur audio.
Utilise le module mido pour créer un fichier MIDI standard.
"""

import random
from mido import Message, MidiFile, MidiTrack, MetaMessage, bpm2tempo

# ——— CONFIGURATION ——————————————————————————————————————————————
OUTPUT_FILE   = "random_pattern.mid"
TEMPO_BPM     = 120          # tempo en BPM
TPB           = 480          # ticks per beat (points par noire)
TRACK_CHANNEL = 0            # canal MIDI 0 (piano)
INSTRUMENT    = 0            # (0 = Acoustic Grand Piano)

NUM_BARS      = 4            # nombre de mesures
BEATS_PER_BAR = 4            # nombre de temps par mesure
SUBDIV        = 4            # subdivisions(16e notes)
SCALE_NOTES   = [60, 62, 64, 65, 67, 69, 71, 72]  
# (C4 majeur : C, D, E, F, G, A, B, C5)

VELOCITY_MIN  = 40           # vélocité minimale
VELOCITY_MAX  = 100          # vélocité maximale
# ————————————————————————————————————————————————————————————————

def generate_random_pattern():
    mid = MidiFile(ticks_per_beat=TPB)
    track = MidiTrack()
    mid.tracks.append(track)

    #tempo & instrument
    track.append(MetaMessage('set_tempo', tempo=bpm2tempo(TEMPO_BPM)))
    track.append(Message('program_change', program=INSTRUMENT, channel=TRACK_CHANNEL, time=0))

    #Génère les notes
    ticks_per_step = TPB // SUBDIV
    total_steps = NUM_BARS * BEATS_PER_BAR * SUBDIV

    time = 0
    for step in range(total_steps):
        # choix aléatoire : jouer une note ou silence ?
        if random.random() < 0.5:
            note = random.choice(SCALE_NOTES)
            vel  = random.randint(VELOCITY_MIN, VELOCITY_MAX)
            # note on
            track.append(Message('note_on', note=note, velocity=vel,
                                 time=time, channel=TRACK_CHANNEL))
            # note off après un step
            track.append(Message('note_off', note=note, velocity=0,
                                 time=ticks_per_step, channel=TRACK_CHANNEL))
            time = 0
        else:
            # silence = avance le temps
            time += ticks_per_step

    # Fin de piste
    track.append(MetaMessage('end_of_track', time=1))
    return mid

def main():
    mid = generate_random_pattern()
    mid.save(OUTPUT_FILE)
    print(f" Pattern MIDI aléatoire généré dans « {OUTPUT_FILE} »")

if __name__ == "__main__":
    main()
