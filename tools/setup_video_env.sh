#!/usr/bin/env bash
# One-shot setup for rendering Find It Cheaper videos in a fresh session.
# Installs piper-tts, fetches the voice, checks ffmpeg and the Poppins fonts.
set -euo pipefail
VOICE_DIR="${FIC_VOICE_DIR:-$HOME/.cache/fic-voices}"
VOICE="${FIC_VOICE:-en-gb-southern_english_female-low}"
mkdir -p "$VOICE_DIR"
python3 -c "import piper" 2>/dev/null || pip install --quiet --break-system-packages piper-tts
python3 -c "import PIL, numpy" 2>/dev/null || pip install --quiet --break-system-packages pillow numpy
command -v ffmpeg >/dev/null || { echo "ffmpeg missing: apt-get install -y ffmpeg"; exit 1; }
if [ ! -f "$VOICE_DIR/$VOICE.onnx" ]; then
  # HuggingFace is blocked from the sandbox; the GitHub release mirror works.
  curl -sSL -o "$VOICE_DIR/voice.tar.gz" "https://github.com/rhasspy/piper/releases/download/v0.0.2/voice-$VOICE.tar.gz"
  tar -xzf "$VOICE_DIR/voice.tar.gz" -C "$VOICE_DIR" && rm "$VOICE_DIR/voice.tar.gz"
fi
FONT_DIR="${FIC_FONT_DIR:-/usr/share/fonts/truetype/google-fonts}"
[ -f "$FONT_DIR/Poppins-Bold.ttf" ] || { echo "Poppins not found in $FONT_DIR; install google fonts or set FIC_FONT_DIR"; exit 1; }
echo "ok: voice at $VOICE_DIR/$VOICE.onnx"
