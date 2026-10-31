"""Voice-over for the promo videos (offline, no account needed).

    python3 kit/voice.py <script.json> <out.wav> [music.wav]

script.json:
    {"voice": "af_heart", "secs": 24, "lines": [
        {"t": 0.3, "text": "Tired of downloads that stop halfway?"},
        {"t": 4.0, "text": "SwiftGrab is a download manager for Windows."}
    ]}

Each line starts at its time "t" (seconds), so the video can show exactly what the
voice is talking about. The script prints every line's start and end time; build the
video's scenes to match them. A line that would run into the next one is spoken a bit
faster (up to 1.2x); if it still doesn't fit, the script stops and says which line to shorten.
With a music file, the music plays quietly under the voice and comes back up in pauses.

Setup (once per session; everything is in kit/tts, nothing is downloaded):
    pip install --break-system-packages --no-index --no-deps -q kit/tts/*.whl
Voices: af_heart (warm female, default), af_bella, am_michael (male), am_fenrir, bf_emma (British).
"""
import json
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np

KIT = Path(__file__).resolve().parent
SR = 24000


def synth(k, text, voice, speed):
    samples, sr = k.create(text, voice=voice, speed=speed, lang="en-us")
    assert sr == SR, sr
    return np.asarray(samples, dtype=np.float32)


def write_wav(path, data, sr):
    data = np.clip(data, -1, 1)
    pcm = (data * 32767).astype("<i2")
    if pcm.ndim == 1:
        pcm = np.stack([pcm, pcm], axis=1)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(pcm.tobytes())


def main():
    script_path, out = Path(sys.argv[1]), Path(sys.argv[2])
    music = Path(sys.argv[3]) if len(sys.argv) > 3 else None
    sc = json.loads(script_path.read_text(encoding="utf-8"))
    voice = sc.get("voice", "af_heart")
    secs = float(sc["secs"])
    lines = sorted(sc["lines"], key=lambda l: l["t"])

    from kokoro_onnx import Kokoro
    k = Kokoro(str(KIT / "tts" / "kokoro-v1.0.int8.onnx"), str(KIT / "tts" / "voices-v1.0.bin"))

    track = np.zeros(int(secs * SR) + SR, dtype=np.float32)
    talking = np.zeros_like(track)
    timing, problems = [], []
    for i, ln in enumerate(lines):
        start = float(ln["t"])
        limit = (float(lines[i + 1]["t"]) if i + 1 < len(lines) else secs) - start - 0.15
        speed = float(ln.get("speed", sc.get("speed", 1.0)))
        clip = synth(k, ln["text"], voice, speed)
        while len(clip) / SR > limit and speed < 1.2:
            speed = round(speed + 0.05, 2)
            clip = synth(k, ln["text"], voice, speed)
        dur = len(clip) / SR
        if dur > limit:
            problems.append(f'line {i + 1} ("{ln["text"][:40]}…") needs {dur:.1f}s but has {limit:.1f}s: shorten it or move the next line later')
        a = int(start * SR)
        track[a:a + len(clip)] += clip[:len(track) - a]
        talking[a:a + len(clip)] = 1
        timing.append({"t": start, "end": round(start + dur, 2), "speed": speed, "text": ln["text"]})

    peak = float(np.max(np.abs(track))) or 1.0
    track = track / peak * 0.89                    # voice about -1 dB peak before loudnorm
    track = track[:int(secs * SR)]
    talking = talking[:int(secs * SR)]

    tmp_voice = out.with_suffix(".voice.wav")
    write_wav(tmp_voice, track, SR)
    if music and music.exists():
        # music ducks under the voice (sidechain) and fills the pauses
        subprocess.run([
            "ffmpeg", "-y", "-loglevel", "error", "-i", str(music), "-i", str(tmp_voice),
            "-filter_complex",
            "[0:a]aresample=48000,volume=0.55[m];[1:a]aresample=48000,asplit=2[v][sc];"
            "[m][sc]sidechaincompress=threshold=0.02:ratio=10:attack=15:release=350[duck];"
            "[duck][v]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11",
            "-t", str(secs), "-ar", "48000", str(out)], check=True)
        tmp_voice.unlink()
    else:
        tmp_voice.replace(out)

    for t in timing:
        print(f'{t["t"]:5.2f} – {t["end"]:5.2f}s  (x{t["speed"]})  {t["text"]}')
    if problems:
        print("\nTOO LONG:\n  " + "\n  ".join(problems))
        sys.exit(2)


if __name__ == "__main__":
    main()
