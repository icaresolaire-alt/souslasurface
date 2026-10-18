"""Musiques de fond générées en MIDI puis rendues avec une banque de sons réalistes (FluidR3, GM).

Plusieurs ambiances tournent d'un épisode à l'autre pour éviter la lassitude.
Toutes gardent la même logique : intro légère, batterie qui s'arrête pendant
le retournement (≈ 35 à 40 s), puis reprise jusqu'à la fin.
"""
import math, subprocess, sys
import mido

TPB = 480
BAR = 4 * TPB

# Chaque style : tempo, instruments General MIDI, accords (4 mesures), basses, rythme de mélodie, batterie
STYLES = {
    'chill': dict(bpm=90, keys=4, lead=11, bass=33, pad=None,
        chords=[[57, 60, 64, 67], [53, 57, 60, 64], [55, 60, 64, 71], [55, 59, 62, 64]],
        roots=[33, 29, 36, 31], comp='stab', drums='boombap',
        rhythm=[(0, 2, 1), (1.5, 3, 0.5), (2, 1, 1.5)]),
    'piano': dict(bpm=84, keys=0, lead=None, bass=32, pad=48,
        chords=[[50, 57, 60, 65], [46, 53, 57, 62], [53, 57, 60, 64], [48, 55, 59, 64]],   # Ré m7, Si♭maj7, Fa, Do
        roots=[38, 34, 41, 36], comp='arp', drums='soft',
        rhythm=[]),
    'electro': dict(bpm=104, keys=89, lead=8, bass=38, pad=None,
        chords=[[52, 55, 59, 62], [48, 52, 55, 59], [55, 59, 62, 66], [50, 54, 57, 62]],   # Mi m7, Do maj7, Sol, Ré
        roots=[40, 36, 43, 38], comp='pad', drums='four',
        rhythm=[(0, 3, 0.5), (0.75, 2, 0.5), (1.5, 1, 0.5), (2.5, 2, 0.5), (3, 3, 1)]),
    'guitare': dict(bpm=96, keys=24, lead=12, bass=32, pad=None,
        chords=[[52, 59, 64, 67], [48, 55, 60, 64], [55, 59, 62, 67], [50, 57, 62, 66]],
        roots=[40, 36, 43, 38], comp='arp', drums='brush',
        rhythm=[(0, 2, 0.5), (0.5, 3, 0.5), (2, 1, 1), (3, 2, 1)]),
    'cinema': dict(bpm=80, keys=48, lead=60, bass=43, pad=None,
        chords=[[45, 52, 57, 60], [41, 48, 53, 57], [48, 55, 60, 64], [43, 50, 55, 59]],
        roots=[33, 29, 36, 31], comp='pulse', drums='timpani',
        rhythm=[(0, 3, 2), (2, 2, 2)]),
}
ORDER = ['chill', 'piano', 'electro', 'guitare', 'cinema']

def pick_style(key):
    """Style déterministe à partir d'un numéro d'épisode (ou de n'importe quelle chaîne)."""
    if isinstance(key, int): return ORDER[key % len(ORDER)]
    digits = ''.join(ch for ch in str(key) if ch.isdigit())
    return ORDER[int(digits) % len(ORDER)] if digits else 'chill'

def song(style='chill', seconds=66, quiet=(34.5, 40.0)):
    S = STYLES[style]; bpm = S['bpm']
    bar_s = 4 * 60 / bpm
    bars = int(math.ceil(seconds / bar_s))
    breakdown = {b for b in range(bars) if quiet[0] <= b * bar_s < quiet[1]}
    intro = 2
    evs = []
    def note(ch, n, start, dur, vel):
        evs.append((int(start), mido.Message('note_on', channel=ch, note=n, velocity=vel)))
        evs.append((int(start + dur), mido.Message('note_off', channel=ch, note=n, velocity=0)))
    q = TPB
    for b in range(bars):
        s = b * BAR; ci = b % 4; ch_notes = S['chords'][ci]
        last = b == bars - 1
        full = b >= intro and b not in breakdown and not last
        # accompagnement
        if S['comp'] == 'stab':
            for n in ch_notes:
                note(0, n, s, 2.4 * q, 58)
                if not last: note(0, n, s + 2.5 * q, 1.4 * q, 46)
        elif S['comp'] == 'arp':
            seq = ch_notes + [ch_notes[2] + 12, ch_notes[1] + 12] + ch_notes[1:3]
            for i in range(8):
                note(0, seq[i % len(seq)], s + i * 0.5 * q, 0.9 * q, 60 if i % 4 == 0 else 48)
        elif S['comp'] == 'pad':
            for n in ch_notes: note(0, n, s, 3.9 * q, 52)
        elif S['comp'] == 'pulse':
            for i in range(8):
                for n in ch_notes[1:]: note(0, n, s + i * 0.5 * q, 0.45 * q, 50 if i % 2 else 62)
        if S.get('pad') is not None:
            for n in ch_notes: note(3, n + 12, s, 4 * q, 40)
        # mélodie : notes de l'accord, une octave au-dessus
        if S['lead'] is not None and b >= intro and not last:
            for (bt, idx, d) in S['rhythm']:
                note(1, ch_notes[idx % 4] + 12, s + bt * q, d * q * 0.95, 70 if b not in breakdown else 50)
        if full:
            r = S['roots'][ci]
            note(2, r, s, 1.4 * q, 92); note(2, r, s + 2 * q, 1.2 * q, 86)
            if S['drums'] in ('boombap', 'four'): note(2, r + 7, s + 3.5 * q, 0.45 * q, 74)
            d = S['drums']
            if d == 'boombap':
                for k in (0, 1.75, 2.5): note(9, 36, s + k * q, 0.2 * q, 100 if k == 0 else 82)
                for k in (1, 3): note(9, 38, s + k * q, 0.2 * q, 88)
                for i in range(8): note(9, 42, s + i * 0.5 * q + (0.08 * q if i % 2 else 0), 0.1 * q, 62 if i % 2 else 78)
            elif d == 'four':
                for k in range(4): note(9, 36, s + k * q, 0.2 * q, 96)
                for k in (1, 3): note(9, 39, s + k * q, 0.2 * q, 70)
                for i in range(8): note(9, 42 if i % 2 == 0 else 46, s + i * 0.5 * q + 0.5 * q * (i % 2 == 0) * 0, 0.1 * q, 58)
            elif d == 'brush':
                for k in (0, 2.5): note(9, 36, s + k * q, 0.2 * q, 72)
                for k in (1, 3): note(9, 37, s + k * q, 0.2 * q, 66)          # side stick
                for i in range(8): note(9, 70, s + i * 0.5 * q, 0.1 * q, 44)   # maracas
            elif d == 'soft':
                note(9, 36, s, 0.2 * q, 60); note(9, 51, s + 2 * q, 0.4 * q, 40)  # grosse caisse + ride
            elif d == 'timpani':
                note(4, r + 12, s, 1.5 * q, 90); note(4, r + 12, s + 3 * q, 0.5 * q, 70)
        elif b < intro and not last and S['drums'] in ('boombap', 'four'):
            for i in range(8): note(9, 42, s + i * 0.5 * q, 0.1 * q, 50 if i % 2 else 64)
    s = bars * BAR
    for n in S['chords'][0]: note(0, n, s, 4 * q, 55)
    evs.sort(key=lambda e: (e[0], e[1].type == 'note_on'))
    mid = mido.MidiFile(ticks_per_beat=TPB); tr = mido.MidiTrack(); mid.tracks.append(tr)
    tr.append(mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(bpm)))
    progs = {0: S['keys'], 1: S['lead'] if S['lead'] is not None else 0, 2: S['bass'], 3: S['pad'] or 0, 4: 47}
    for ch, prog in progs.items(): tr.append(mido.Message('program_change', channel=ch, program=prog))
    for ch, rev in ((0, 70), (1, 90), (3, 100)): tr.append(mido.Message('control_change', channel=ch, control=91, value=rev))
    tr.append(mido.Message('control_change', channel=1, control=7, value=86))
    tr.append(mido.Message('control_change', channel=3, control=7, value=70))
    tr.append(mido.Message('control_change', channel=9, control=7, value=96))
    last = 0
    for t, m in evs:
        tr.append(m.copy(time=t - last)); last = t
    return mid

def render(path_wav, style='chill', seconds=66):
    mid = song(style, seconds); midp = path_wav.replace('.wav', '.mid'); mid.save(midp)
    subprocess.run(['fluidsynth', '-ni', '-g', '0.7', '-r', '44100', '-F', path_wav,
                    '/usr/share/sounds/sf2/FluidR3_GM.sf2', midp], check=True, capture_output=True)

if __name__ == '__main__':
    render(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else 'chill')
