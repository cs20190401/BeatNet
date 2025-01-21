from pydub import AudioSegment
from pydub.generators import Sine
from BeatNet.BeatNet import BeatNet

INPUT_PATH = "./test/test_data/Can't Sleep Love.mp3"
SLICED_PATH = "./test/test_data/Can't_Sleep_Love_Sliced.mp3"
output_path = "./test/output/Can't.mp3"

# Initialize BeatNet
estimator = BeatNet(1, mode='online', inference_model='PF', plot=['activations'], thread=False)

# Load the input audio
input_audio = AudioSegment.from_file(INPUT_PATH)

# Extract a 10-second segment from the input audio (from 0 to 10 seconds)
start_time = 0 * 1000  # start time in milliseconds
end_time = 10 * 1000  # end time in milliseconds
sliced_audio = input_audio[start_time:end_time]

# Save the sliced audio to a new file
sliced_audio.export(SLICED_PATH, format="mp3")

# Process the sliced audio to get the beat tracking output
output = estimator.process(SLICED_PATH)

# Define the threshold
threshold = 0.4
sample_rate = 22050  # Sample rate used in BeatNet
hop_length = int(20 * 0.001 * sample_rate) #20ms hop size
win_length = int(64 * 0.001 * sample_rate) #64ms window size

# Generate a click sound
low_click = Sine(500).to_audio_segment(duration=10)  # 10ms click sound
high_click = Sine(1500).to_audio_segment(duration=10)  # 10ms click sound

# Create an empty audio segment for the metronome track
metronome_track = AudioSegment.silent(duration=len(sliced_audio))

# Add click sounds to the metronome track based on the output vector
for i, (time, type) in enumerate(output):
    frame_position = int(time * 1000)  # s to ms
    metronome_track = metronome_track.overlay(high_click if type == 1 else low_click, position=frame_position)

'''
# Add click sounds to the metronome track based on the output vector
for i, (beat, downbeat) in enumerate(output):
    if downbeat > threshold:
        frame_position = int((i * hop_length / sample_rate) * 1000)  # Convert to milliseconds
        metronome_track = metronome_track.overlay(high_click, position=frame_position)
    elif beat > threshold:
        frame_position = int((i * hop_length / sample_rate) * 1000)  # Convert to milliseconds
        metronome_track = metronome_track.overlay(low_click, position=frame_position)
'''

# Adjust the volume of the input track and the metronome track
sliced_audio = sliced_audio - 2  # Decrease volume (dB)
metronome_track = metronome_track + 2  # Increase volume (dB)

# Mix the metronome track with the input audio
mixed_audio = sliced_audio.overlay(metronome_track)

# Save the mixed audio to a separate directory
mixed_audio.export(output_path, format="mp3")

print(f"Mixed audio saved to {output_path}")