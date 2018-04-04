import numpy as np
import pyaudio as ap
import sys
from config import *

SAMPLES_PER_FFT = FRAME_SIZE*FRAMES_PER_FFT
FREQ_STEP = float(FSAMP)/SAMPLES_PER_FFT


NOTE_NAMES = 'C. C# D. D# E. F. F# G. G# A. A# B.'.split()


def freq_to_number(f):
    return 69 + 12*np.log2(f/440.0)


def number_to_freq(n):
    return 440 * 2.0**((n-69)/12.0)


def note_name(n):
    return NOTE_NAMES[n % 12] + str(n/12 - 1)


def note_to_fftbin(n):
    return number_to_freq(n)/FREQ_STEP


imin = max(0, int(np.floor(note_to_fftbin(NOTE_MIN-1))))
imax = min(SAMPLES_PER_FFT, int(np.ceil(note_to_fftbin(NOTE_MAX+1))))

buf = np.zeros(SAMPLES_PER_FFT, dtype=np.float32)
num_frames = 0

stream = ap.PyAudio().open(format=ap.paInt16,
                                channels=1,
                                rate=FSAMP,
                                input=True,
                                frames_per_buffer=FRAME_SIZE)

stream.start_stream()

window = 0.5 * (1 - np.cos(np.linspace(0, 2*np.pi, SAMPLES_PER_FFT, False)))


print 'Sampling at', FSAMP, 'Hz with max resolution of', FREQ_STEP, 'Hz'

border = '+----------------------------------------------------------+'
title =  '|                          TUNERR                          |'
notes =  '| C   C#    D   D#    E    F   F#    G   G#    A   A#    B |'
cents = '|  -0.5 -0.4 -0.3 -0.2 -0.1   0  +0.1 +0.2 +0.3 +0.4 +0.5  |'

print(border + '\n' + title + '\n' + border + '\n' + notes)

while stream.is_active():


    buf[:-FRAME_SIZE] = buf[FRAME_SIZE:]
    buf[-FRAME_SIZE:] = np.fromstring(stream.read(FRAME_SIZE), np.int16)


    fft = np.fft.rfft(buf * window)


    freq = (np.abs(fft[imin:imax]).argmax() + imin) * FREQ_STEP


    n = freq_to_number(freq)
    n0 = int(round(n))


    num_frames += 1


    if num_frames >= FRAMES_PER_FFT:

        pointer1 = list(border)
        pointer2 = list(border)

        pointer1[2+(n0%12)*5] = '^'
        pointer2[int(30+(n-n0)*50)] = '^'

        pointer1 = ''.join(pointer1)
        pointer2 = ''.join(pointer2)

        stats = '|  FREQ: {:7.2f} Hz                       NOTE: {:>3s} {:+.2f}  |'.format(freq, note_name(n0), n-n0)
        output = pointer1 + '\n' + cents + '\n' + pointer2 + '\n' + stats + '\n' + border  + '\n'
        print(output)

        for i in range(0,6):
            sys.stdout.write("\033[F")


'''
inspired by Matt Zucker's tuner
<https://mzucker.github.io/2016/08/07/ukulele-tuner.html>
'''
