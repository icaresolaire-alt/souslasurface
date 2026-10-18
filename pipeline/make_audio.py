"""Musique + effets pour un épisode."""
import numpy as np, soundfile as sf
import music
SR = 44100

def build_audio(mod, out_path):
    mw = out_path.replace('.wav', '-musique.wav')
    music.render(mw, 24, breakdown=(13, 14))
    m, sr = sf.read(mw)
    if m.ndim == 1: m = np.stack([m, m], 1)
    N = int(mod.TOTAL * SR)
    m = m[:N] if len(m) >= N else np.concatenate([m, np.zeros((N - len(m), 2))])
    fade = int(2.0 * SR); m[-fade:] *= np.linspace(1, 0, fade)[:, None]
    fx = np.zeros(N + SR * 3)
    for t0, snd in mod.sfx_events():
        i = int(t0 * SR); fx[i:i + len(snd)] += snd[:len(fx) - i]
    fx = fx[:N]
    rms = lambda x: np.sqrt((x ** 2).mean()) + 1e-9
    out = m * (0.10 / rms(m)) + (fx * (0.055 / rms(fx)))[:, None]
    out = 0.92 * np.tanh(out / 0.92)
    sf.write(out_path, out.astype(np.float32), SR)
