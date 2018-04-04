######################################################################
# Might want to change NOTE_MIN and NOTE_MAX especially for guitar/bass.
# Probably want to keep FRAME_SIZE and FRAMES_PER_FFT to be powers of two.

NOTE_MIN = 60       # C4
NOTE_MAX = 69       # A4
FSAMP = 22050       # Sampling frequency in Hz
FRAME_SIZE = 1024   # Samples per frame
FRAMES_PER_FFT = 16 # FFT average across frames
