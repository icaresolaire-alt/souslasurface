"""Rendu complet d'un épisode.
Usage (depuis pipeline/) : python3 build.py episodes/epXXX_nom.py ../videos/AAAA-MM-JJ-nom.mp4
Images fixes de contrôle : python3 build.py episodes/epXXX_nom.py --stills 2 10 30 50
"""
import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'episodes'))
from lib import render, still
from make_audio import build_audio

def load(path):
    spec = importlib.util.spec_from_file_location(os.path.basename(path)[:-3], path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

if __name__ == '__main__':
    mod = load(sys.argv[1])
    if sys.argv[2] == '--stills':
        d = os.environ.get('STILLS_DIR', '/tmp'); os.makedirs(d, exist_ok=True)
        for x in sys.argv[3:]: still(f'{d}/still_{x}.png', float(x), mod.draw)
        print(f'images dans {d}/still_*.png')
    else:
        out = os.path.abspath(sys.argv[2]); wav = out[:-4] + '.wav'
        build_audio(mod, wav)
        render(out, mod.TOTAL, mod.draw, audio=wav)
        os.remove(wav); os.remove(wav.replace('.wav', '-musique.wav'))
        for ext in ('.mid',):
            p = wav.replace('.wav', '-musique' + ext)
            if os.path.exists(p): os.remove(p)
        print('ok', out)
