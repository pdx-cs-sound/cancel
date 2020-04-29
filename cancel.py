# Audio Cancellation Demo
# Bart Massey

# https://www.uaudio.com/blog/audio-compression-basics/

import argparse
import numpy as np
import soundfile

samplerate = 48000

ap = argparse.ArgumentParser()
ap.add_argument(
    "-f", "--freq",
    help="Fundamental frequency.",
    type=float,
    default=1000.0,
)
ap.add_argument(
    "-t", "--time",
    help="Total time.",
    type=float,
    default=1.0,
)
ap.add_argument(
    "-o", "--offset",
    help="Offset time.",
    type=float,
    default=0.001,
)
ap.add_argument(
    "outfile",
    help="Output audio file.",
)
args = ap.parse_args()

# Sine
ts = np.linspace(
    0,
    2 * np.pi * args.freq * samplerate * args.time,
    int(args.time * samplerate),
)
psignal = 0.5 * np.sin(ts)

offset = int(samplerate * args.offset)
earlysignal = np.append(psignal, np.zeros(offset))
latesignal = np.append(np.zeros(offset), psignal)
outsignal = earlysignal + latesignal

outfile = open(args.outfile, "wb")
soundfile.write(
    outfile,
    outsignal,
    samplerate,
    subtype='PCM_16',
    format='WAV',
)
