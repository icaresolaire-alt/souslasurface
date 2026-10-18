"""Instrumental chill / lo-fi généré en MIDI puis rendu avec une banque de sons réalistes (FluidR3)."""
import mido, subprocess, sys

BPM = 90
TPB = 480
BAR = 4 * TPB

# accords : La m7 – Fa maj7 – Do maj7 – Sol6
CHORDS = [[57, 60, 64, 67], [53, 57, 60, 64], [55, 60, 64, 71], [55, 59, 62, 64]]
ROOTS = [33, 29, 36, 31]
FIFTHS = [40, 36, 43, 38]
# petite mélodie de vibraphone sur 4 mesures : (temps en noires, note, durée en noires)
MELODY = [(0, 76, 1), (1.5, 79, 0.5), (2, 81, 1.5), (4.5, 77, 0.5), (5, 76, 1), (6, 72, 2),
          (8, 76, 1), (9, 79, 1), (10, 84, 1.5), (12.5, 83, 0.5), (13, 79, 1), (14, 74, 2)]

def song(bars, breakdown=(), intro=2):
    """breakdown : mesures (index 0) où seuls piano et vibraphone jouent."""
    evs = []  # (tick, msg)
    def note(ch, n, start, dur, vel):
        evs.append((int(start), mido.Message('note_on', channel=ch, note=n, velocity=vel)))
        evs.append((int(start + dur), mido.Message('note_off', channel=ch, note=n, velocity=0)))
    q = TPB
    for b in range(bars):
        s = b * BAR; ci = b % 4
        full = b >= intro and b not in breakdown
        last = b == bars - 1
        # piano électrique : accord tenu + relance sur le temps 3 et demi
        for n in CHORDS[ci]:
            note(0, n, s, 2.4 * q, 58)
            if not last: note(0, n, s + 2.5 * q, 1.4 * q, 46)
        # mélodie (pas dans l'intro ni la dernière mesure)
        if b >= intro and not last:
            for (bt, n, d) in MELODY:
                if (b - intro) % 4 * 4 <= bt < ((b - intro) % 4 + 1) * 4:
                    note(1, n, s + (bt - ((b - intro) % 4) * 4) * q, d * q * 0.95, 70 if b not in breakdown else 52)
        if full and not last:
            # basse
            note(2, ROOTS[ci], s, 1.4 * q, 92)
            note(2, ROOTS[ci], s + 1.75 * q, 0.5 * q, 70)
            note(2, ROOTS[ci], s + 2 * q, 1.2 * q, 88)
            note(2, FIFTHS[ci], s + 3.5 * q, 0.45 * q, 74)
            # batterie (canal 9) avec un léger swing sur les charlestons
            for k in (0, 1.75, 2.5): note(9, 36, s + k * q, 0.2 * q, 100 if k == 0 else 82)
            for k in (1, 3): note(9, 38, s + k * q, 0.2 * q, 88)
            for i in range(8):
                sw = 0.08 * q if i % 2 else 0
                note(9, 42, s + i * 0.5 * q + sw, 0.1 * q, 62 if i % 2 else 78)
            if b % 4 == 3: note(9, 46, s + 3.5 * q, 0.4 * q, 60)
        elif b < intro and not last:
            # intro : charleston seul pour donner le tempo dès la première seconde
            for i in range(8): note(9, 42, s + i * 0.5 * q, 0.1 * q, 50 if i % 2 else 64)
    # fin : accord final tenu
    s = bars * BAR
    for n in CHORDS[0]: note(0, n, s, 4 * q, 55)
    evs.sort(key=lambda e: (e[0], e[1].type == 'note_on'))
    mid = mido.MidiFile(ticks_per_beat=TPB); tr = mido.MidiTrack(); mid.tracks.append(tr)
    tr.append(mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(BPM)))
    for ch, prog in ((0, 4), (1, 11), (2, 33)):
        tr.append(mido.Message('program_change', channel=ch, program=prog))
    tr.append(mido.Message('control_change', channel=0, control=91, value=70))   # réverbe piano
    tr.append(mido.Message('control_change', channel=1, control=91, value=90))   # réverbe vibra
    tr.append(mido.Message('control_change', channel=1, control=7, value=88))
    tr.append(mido.Message('control_change', channel=9, control=7, value=96))
    last = 0
    for t, m in evs:
        tr.append(m.copy(time=t - last)); last = t
    return mid

def render(path_wav, bars, breakdown=()):
    mid = song(bars, breakdown); midp = path_wav.replace('.wav', '.mid'); mid.save(midp)
    subprocess.run(['fluidsynth', '-ni', '-g', '0.7', '-r', '44100', '-F', path_wav,
                    '/usr/share/sounds/sf2/FluidR3_GM.sf2', midp], check=True, capture_output=True)

if __name__ == '__main__':
    render(sys.argv[1], int(sys.argv[2]))
