from pydub import AudioSegment
import matplotlib.pyplot as plt
import numpy as np
from deotect_notes import classify_note, frequency_spectrum 
from output import playMelody
song = AudioSegment.from_file("cmajor.wav")
SEGMENT_MS = 50
volume = [segment.dBFS for segment in song[::SEGMENT_MS]]
VOLUME_THRESHOLD = -35
EDGE_THRESHOLD = 5
predicted_starts = []
MIN_MS_BETWEEN = 100
for i in range(1, len(volume)):
    if (
        volume[i] > VOLUME_THRESHOLD and
        volume[i] - volume[i - 1] > EDGE_THRESHOLD
    ):
        ms = i * SEGMENT_MS
        if (
            len(predicted_starts) == 0 or
            ms - predicted_starts[-1] >= MIN_MS_BETWEEN
        ):
            predicted_starts.append(ms)
for ms in predicted_starts:
    plt.axvline(x=(ms / 1000), color="g", linewidth=0.5, linestyle=":")

predicted_notes = []
for i, start in enumerate(predicted_starts):
    sample_from = start + 50
    sample_to = start + 550
    if i < len(predicted_starts) - 1:
        sample_to = min(predicted_starts[i + 1], sample_to)
    segment = song[sample_from:sample_to]
    freqs, freq_magnitudes = frequency_spectrum(segment)

    predicted = classify_note(freqs, freq_magnitudes)
    predicted_notes.append(predicted or "U")
playMelody(predicted_notes)
x_axis = np.arange(len(volume)) * (SEGMENT_MS / 1000)
plt.plot(x_axis, volume)
plt.show()





