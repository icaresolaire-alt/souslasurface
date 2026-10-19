"""Musique + effets pour un épisode."""
import numpy as np, soundfile as sf
import music
SR = 44100
MIN_GAP = 1.2    # secondes minimum entre deux effets
FX_LEVEL = 0.022  # niveau des effets (avant : 0.055)

def build_audio(mod, out_path):
    mw = out_path.replace('.wav', '-musique.wav')
    style = getattr(mod, 'MUSIC_STYLE', None) or music.pick_style(getattr(mod, '__name__', ''))
    music.render(mw, style, mod.TOTAL)
    print('musique :', style)
    m, sr = sf.read(mw)
    if m.ndim == 1: m = np.stack([m, m], 1)
    N = int(mod.TOTAL * SR)
    m = m[:N] if len(m) >= N else np.concatenate([m, np.zeros((N - len(m), 2))])
    fade = int(2.0 * SR); m[-fade:] *= np.linspace(1, 0, fade)[:, None]
    # Effets sonores : peu nombreux et doux (demande du propriétaire).
    # 1) on n'en garde qu'un toutes les MIN_GAP secondes ;
    # 2) on adoucit l'attaque et on coupe les aigus ;
    # 3) on les mixe nettement sous la musique.
    fx = np.zeros(N + SR * 3)
    last = -99.0
    for t0, snd in sorted(mod.sfx_events(), key=lambda e: e[0]):
        if t0 - last < MIN_GAP: continue
        last = t0
        snd = np.asarray(snd, dtype=float).copy()
        k = min(len(snd), int(0.015 * SR)); snd[:k] *= np.linspace(0, 1, k)   # attaque adoucie
        i = int(t0 * SR); fx[i:i + len(snd)] += snd[:len(fx) - i]
    fx = fx[:N]
    a = np.exp(-2 * np.pi * 2500 / SR)                                         # passe-bas ~2,5 kHz
    y = np.zeros_like(fx); acc = 0.0
    for j in range(0, len(fx), SR):                                            # par blocs pour la vitesse
        blk = fx[j:j + SR]; out_b = np.empty_like(blk)
        for n, v in enumerate(blk): acc = (1 - a) * v + a * acc; out_b[n] = acc
        y[j:j + SR] = out_b
    fx = y
    rms = lambda x: np.sqrt((x ** 2).mean()) + 1e-9
    out = m * (0.145 / rms(m)) + (fx * (FX_LEVEL / rms(fx)))[:, None]
    out = 0.92 * np.tanh(out / 0.92)
    sf.write(out_path, out.astype(np.float32), SR)
