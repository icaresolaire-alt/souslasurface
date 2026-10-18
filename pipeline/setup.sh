#!/bin/bash
# Installe ce qu'il faut pour fabriquer les vidéos (à lancer au début de chaque session).
set -e
python3 -c "import cairo, mido, soundfile, numpy" 2>/dev/null || pip install --break-system-packages -q pycairo mido soundfile numpy
which fluidsynth >/dev/null && [ -f /usr/share/sounds/sf2/FluidR3_GM.sf2 ] || (apt-get update -qq && DEBIAN_FRONTEND=noninteractive apt-get install -y -qq fluidsynth fluid-soundfont-gm >/dev/null)
which ffmpeg >/dev/null || (apt-get update -qq && DEBIAN_FRONTEND=noninteractive apt-get install -y -qq ffmpeg >/dev/null)
fc-list | grep -q "Inter Display" || echo "ATTENTION : police Inter Display absente, le rendu utilisera une police de secours"
echo "pipeline prêt"
