# Audio Cancellation Demo
# Bart Massey

import argparse
import numpy as np
import soundfile

samplerate = 48000

ap = argparse.ArgumentParser()
ap.add_argument(
    "-f", "--freq",
    help="Fundamental frequency in Hz.",
    type=float,
    default=1000.0,
)
ap.add_argument(
    "-t", "--time",
    help="Total time in secs.",
    type=float,
    default=1.0,
)
ap.add_argument(
    "--mod_offset",
    help="Offset time as fraction of cycle.",
    type=float,
    default=0.0,
)
ap.add_argument(
    "--mod-freq",
    help="Modulation frequency in Hz.",
    type=float,
)
ap.add_argument(
    "--mod-range",
    help="Modulation range as fraction of cycle.",
    type=float,
    default=1.0,
)
ap.add_argument(
    "--mod-depth",
    help="Modulation depth as fraction of full amplitude.",
    type=float,
    default=1.0,
)
ap.add_argument(
    "outfile",
    help="Output audio file.",
)
args = ap.parse_args()

# Sine
nsamples = int(samplerate * args.time)
ts = np.linspace(
    0,
    2 * np.pi * args.freq * args.time,
    nsamples,
)
mod_offset = 2 * np.pi * args.mod_offset
tms = ts + mod_offset
if args.mod_freq is not None:
    mod_range = args.mod_range * np.pi
    print(mod_range)
    tm = np.linspace(
        0,
        2 * np.pi * args.mod_freq * args.time,
        nsamples,
    )
    tms += mod_range * np.sin(tm)
ssignal = np.sin(ts)
msignal = args.mod_depth * np.sin(tms)
outsignal = 0.5 * (ssignal + msignal)

def write_wave(name, sig):
    outfile = open(name, "wb")
    soundfile.write(
        outfile,
        sig,
        samplerate,
        subtype='PCM_16',
        format='WAV',
    )

write_wave(args.outfile, outsignal)
