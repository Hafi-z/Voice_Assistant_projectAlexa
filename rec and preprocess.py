## 1st and 2nd step
from scipy import signal
import numpy as np
import sounddevice as sd
import soundfile as sf

duration = 20  # seconds
fs = 44100

print("Recording started")
recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
sd.wait()  # Wait until recording is finished
print("Recording finished")

# sf.write('yes.wav',recording,fs)

# Apply a bandpass filter to the recording
nyquist = 0.5 * fs
low = 300 / nyquist
high = 3000 / nyquist
b, a = signal.butter(4, [low, high], btype='band')
filtered_recording = signal.lfilter(b, a, recording)

# Normalize the filtered recording
normalized_recording = filtered_recording / np.max(np.abs(filtered_recording))

sf.write('train10.wav',normalized_recording,fs)

# Print the shape of the filtered and normalized recordings
print("Filtered recording shape:", filtered_recording.shape)
print("Normalized recording shape:", normalized_recording.shape)