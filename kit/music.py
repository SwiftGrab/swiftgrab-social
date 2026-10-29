"""Original synthesized background tracks for the SwiftGrab promo videos (royalty-free, made here).
120 BPM, 16 s = 8 bars. Bars 1-2: intro build, drop at 4.0 s, impact at 12.0 s (end card), fade out.
Usage: python3 music.py <any number; 6 different tracks rotate> <out.wav>
"""
import sys
import numpy as np
from scipy.signal import butter, lfilter, sosfilt

SR = 44100
BPM = 120
BEAT = 60 / BPM
DUR = 16.0
N = int(SR * DUR)
rng = np.random.default_rng(7)


def note(m):  # midi -> Hz
    return 440.0 * 2 ** ((m - 69) / 12)


def lp(x, f, order=2):
    return sosfilt(butter(order, f / (SR / 2), "low", output="sos"), x)


def hp(x, f, order=2):
    return sosfilt(butter(order, f / (SR / 2), "high", output="sos"), x)


def bp(x, lo, hi):
    return sosfilt(butter(2, [lo / (SR / 2), hi / (SR / 2)], "band", output="sos"), x)


def place(buf, sig, t, gain=1.0):
    i = int(t * SR)
    if i >= len(buf):
        return
    j = min(len(buf), i + len(sig))
    buf[i:j] += sig[: j - i] * gain


def env(n, a=0.002, d=0.2):
    t = np.arange(n) / SR
    e = np.exp(-t / d)
    k = int(a * SR)
    if k:
        e[:k] *= np.linspace(0, 1, k)
    return e


def saw(f, n, detune=0.0, phase=0.0):
    t = np.arange(n) / SR
    return 2 * ((t * f * (1 + detune) + phase) % 1) - 1


def kick(n=int(0.45 * SR)):
    t = np.arange(n) / SR
    f = 45 + 110 * np.exp(-t * 28)
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) * np.exp(-t * 7)
    s += 0.25 * np.sin(ph * 2) * np.exp(-t * 40)
    click = rng.standard_normal(n) * np.exp(-t * 400) * 0.3
    return np.tanh(1.6 * (s + click))


def clap(n=int(0.3 * SR)):
    t = np.arange(n) / SR
    noise = rng.standard_normal(n)
    e = np.exp(-t * 18)
    for off in (0.0, 0.011, 0.022):
        k = int(off * SR)
        e[k:k + int(0.004 * SR)] += 0.8
    return bp(noise, 900, 5000) * e * 0.9


def hat(open_=False):
    n = int((0.18 if open_ else 0.05) * SR)
    t = np.arange(n) / SR
    return hp(rng.standard_normal(n), 7500) * np.exp(-t * (14 if open_ else 70)) * 0.5


def supersaw(m, n, voices=5, spread=0.012):
    out = np.zeros(n)
    for v in range(voices):
        d = (v - (voices - 1) / 2) / ((voices - 1) / 2) * spread
        out += saw(note(m), n, d, rng.random())
    return out / voices


VARIANTS = {
    # (chord roots as midi, chord quality list, lead pattern offsets, bass octave)
    1: dict(key=57, prog=[(0, "m"), (8, "M"), (3, "M"), (10, "M")], arp=[0, 7, 12, 7, 3, 7, 12, 15]),  # A minor
    2: dict(key=60, prog=[(0, "M"), (7, "M"), (9, "m"), (5, "M")], arp=[0, 4, 7, 12, 7, 4, 12, 16]),   # C major
    3: dict(key=55, prog=[(0, "m"), (5, "m"), (10, "M"), (3, "M")], arp=[12, 7, 3, 7, 12, 15, 12, 7]),  # G minor
    4: dict(key=62, prog=[(0, "m"), (10, "M"), (8, "M"), (7, "M")], arp=[0, 3, 7, 10, 12, 10, 7, 3]),  # D minor
    5: dict(key=59, prog=[(0, "M"), (5, "M"), (7, "M"), (5, "M")], arp=[0, 7, 4, 12, 7, 16, 12, 7]),   # B major
    6: dict(key=53, prog=[(0, "m"), (3, "M"), (10, "M"), (5, "m")], arp=[7, 12, 15, 12, 7, 3, 0, 3]),  # F minor
}


def chord(root, q):
    return [root, root + (3 if q == "m" else 4), root + 7]


def build(variant):
    V = VARIANTS[variant]
    drums = np.zeros(N)
    bass = np.zeros(N)
    pad = np.zeros(N)
    lead = np.zeros(N)
    fx = np.zeros(N)
    bar = 4 * BEAT
    K = kick()
    for b in range(8):
        root_off, q = V["prog"][b % 4]
        root = V["key"] + root_off
        notes = chord(root, q)
        t0 = b * bar
        full = 2 <= b  # drop at bar 3 (4.0 s)
        # pad chords (whole bar)
        n = int(bar * SR)
        p = sum(supersaw(m + 12, n) for m in notes) / 3
        p = lp(p, 2600 if full else 900 + 900 * b)
        a = np.minimum(1, np.arange(n) / (0.05 * SR))
        place(pad, p * a, t0, 0.32 if full else 0.75)
        for beat in range(4):
            tb = t0 + beat * BEAT
            if full or (b == 1 and beat >= 2):
                place(drums, K, tb, 0.7)
            if full and beat in (1, 3):
                place(drums, clap(), tb, 0.55)
            # hats on 8ths (offbeat open hat when full)
            place(drums, hat(), tb, 0.35 if full else 0.45)
            place(drums, hat(open_=full), tb + BEAT / 2, 0.45 if full else 0.25)
            if full:
                place(drums, hat(), tb + BEAT / 4, 0.18)
                place(drums, hat(), tb + 3 * BEAT / 4, 0.18)
            # offbeat bass
            if full:
                bn = int(BEAT / 2 * SR * 0.9)
                bs = lp(saw(note(root - 12), bn) + 0.5 * np.sin(2 * np.pi * note(root - 24) * np.arange(bn) / SR), 700)
                place(bass, bs * env(bn, 0.004, 0.12), tb + BEAT / 2, 0.55)
        # pluck arp on 16ths
        for s in range(16):
            ts = t0 + s * BEAT / 4
            m = root + 12 + V["arp"][s % 8]
            pn = int(0.22 * SR)
            pl = lp(saw(note(m), pn) * 0.6 + np.sign(np.sin(2 * np.pi * note(m) * np.arange(pn) / SR)) * 0.25,
                    3800 if full else 1400 + 600 * b)
            g = 0.22 if full else 0.3
            place(lead, pl * env(pn, 0.002, 0.07), ts, g)
            place(lead, pl * env(pn, 0.002, 0.07) * 0.35, ts + BEAT * 0.75, g)  # dotted echo

    # riser into the drop (2.0 -> 4.0 s) and a smaller one before the end card (10.5 -> 12.0 s)
    for (a, b, g) in ((2.0, 4.0, 0.35), (10.5, 12.0, 0.25)):
        n = int((b - a) * SR)
        x = rng.standard_normal(n)
        out = np.zeros(n)
        chunk = 1024
        for i in range(0, n, chunk):
            f = 400 + 9000 * (i / n) ** 2
            out[i:i + chunk] = bp(x[i:i + chunk], f * 0.7, min(f * 1.3, 20000))
        place(fx, out * np.linspace(0, 1, n) ** 2, a, g)
    # impacts
    for t in (4.0, 12.0):
        n = int(1.2 * SR)
        tt = np.arange(n) / SR
        boom = np.sin(2 * np.pi * (38 + 50 * np.exp(-tt * 10)) * tt) * np.exp(-tt * 3)
        crash = hp(rng.standard_normal(n), 4000) * np.exp(-tt * 2.5) * 0.35
        place(fx, boom * 0.7 + crash, t, 0.8)

    # sidechain duck pads/bass/lead to the kick
    duck = np.ones(N)
    for b in range(2, 8):
        for beat in range(4):
            i = int((b * bar + beat * BEAT) * SR)
            n = int(BEAT * SR)
            j = min(N, i + n)
            curve = 1 - 0.6 * np.exp(-np.arange(j - i) / SR / 0.09)
            duck[i:j] = np.minimum(duck[i:j], curve)
    music = drums + (bass + pad + lead) * duck + fx

    # simple stereo: lead/pad slightly delayed on the right
    d = int(0.012 * SR)
    wide = pad * duck + lead * duck
    left = music
    right = music - wide + np.concatenate([np.zeros(d), wide[:-d]])
    st = np.stack([left, right], 1)
    st = np.tanh(st * 1.1)
    st /= np.max(np.abs(st)) / 0.89
    # fade out last 0.8 s, tiny fade in
    f = int(0.8 * SR)
    st[-f:] *= np.linspace(1, 0, f)[:, None]
    st[: int(0.01 * SR)] *= np.linspace(0, 1, int(0.01 * SR))[:, None]
    return st


if __name__ == "__main__":
    from scipy.io import wavfile
    v, out = (int(sys.argv[1]) - 1) % len(VARIANTS) + 1, sys.argv[2]
    wavfile.write(out, SR, (build(v) * 32767).astype(np.int16))
    print("wrote", out)
