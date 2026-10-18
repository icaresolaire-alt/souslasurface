"""Bande son synthétisée : effets calés sur l'animation + nappe d'ambiance discrète. Aucun son sous droits."""
import numpy as np, soundfile as sf

SR = 44100
rng = np.random.default_rng(3)

def env(n, a=0.005, d=0.2):
    t = np.arange(n) / SR
    att = np.clip(t / max(a, 1e-4), 0, 1)
    return att * np.exp(-t / d)

def pop(f0=520, dur=0.12):
    n = int(dur * SR); t = np.arange(n) / SR
    f = f0 * (1 + 0.8 * np.exp(-t / 0.02))
    return 0.5 * np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.002, 0.035)

def tick(dur=0.03):
    n = int(dur * SR); x = rng.standard_normal(n)
    x = np.diff(x, prepend=0)
    return 0.12 * x * env(n, 0.0005, 0.006)

def clink(f0=2100):
    n = int(0.35 * SR); t = np.arange(n) / SR
    x = np.sin(2*np.pi*f0*t) + 0.6*np.sin(2*np.pi*f0*1.52*t) + 0.3*np.sin(2*np.pi*f0*2.4*t)
    return 0.18 * x * env(n, 0.001, 0.07)

def ding(f0=880, dur=1.6, amp=0.28):
    n = int(dur * SR); t = np.arange(n) / SR
    x = np.sin(2*np.pi*f0*t) + 0.5*np.sin(2*np.pi*f0*2*t) * np.exp(-t/0.3) + 0.25*np.sin(2*np.pi*f0*3.01*t) * np.exp(-t/0.15)
    return amp * x * env(n, 0.003, 0.45)

def whoosh(dur=0.6, amp=0.22):
    n = int(dur * SR); t = np.arange(n) / SR
    x = rng.standard_normal(n)
    # passe-bande glissant approché : lissage de bruit à fenêtre variable
    k = np.linspace(40, 6, n).astype(int)
    c = np.cumsum(np.concatenate([[0], x]))
    idx = np.arange(n)
    y = (c[np.minimum(idx + k, n)] - c[idx]) / k
    shape = np.sin(np.pi * t / dur) ** 2
    return amp * y / (np.abs(y).max() + 1e-9) * shape

def rise(dur=2.0, f0=300, f1=900, amp=0.08):
    n = int(dur * SR); t = np.arange(n) / SR
    f = f0 * (f1 / f0) ** (t / dur)
    return amp * np.sin(2*np.pi*np.cumsum(f)/SR) * np.sin(np.pi * t / dur) ** 2

def chord(freqs=(220, 277.2, 329.6, 440), dur=2.5, amp=0.16):
    n = int(dur * SR); t = np.arange(n) / SR
    x = sum(np.sin(2*np.pi*f*t) + 0.3*np.sin(2*np.pi*2*f*t) for f in freqs) / len(freqs)
    e = np.clip(t / 0.05, 0, 1) * np.exp(-t / 0.9)
    return amp * x * e

def pad(total, amp=0.05):
    """Nappe très douce : La m – Fa – Do – Sol, 4 s par accord, attaques lentes."""
    prog = [(110, 130.8, 164.8), (87.3, 110, 130.8), (130.8, 164.8, 196), (98, 123.5, 146.8)]
    out = np.zeros(int(total * SR)); seg = 4.0; n = int(seg * SR); t = np.arange(n) / SR
    for i in range(int(np.ceil(total / seg))):
        fr = prog[i % 4]
        x = sum(np.sin(2*np.pi*f*t + j) + 0.25*np.sin(2*np.pi*2*f*t) for j, f in enumerate(fr)) / 3
        trem = 1 + 0.15 * np.sin(2*np.pi*0.25*t)
        e = np.clip(t / 1.2, 0, 1) * np.clip((seg + 0.8 - t) / 1.2, 0, 1)
        s = int(i * seg * SR); seg_x = amp * x * trem * e
        out[s:s+n] += seg_x[:len(out)-s]
    fade = int(1.5 * SR)
    out[:fade] *= np.linspace(0, 1, fade); out[-fade:] *= np.linspace(1, 0, fade)
    return out

def mix(total, events, path, pad_amp=0.05):
    out = pad(total, pad_amp)
    out = np.concatenate([out, np.zeros(SR * 3)])
    for t0, snd in events:
        i = int(t0 * SR)
        if 0 <= i < len(out):
            out[i:i+len(snd)] += snd[:len(out)-i]
    out = out[:int(total * SR)]
    out = out * (0.13 / (np.sqrt((out ** 2).mean()) + 1e-9))   # niveau moyen plus fort
    out = 0.92 * np.tanh(out / 0.92)                            # limiteur doux sur les pics
    sf.write(path, np.stack([out, out], 1).astype(np.float32), SR)
