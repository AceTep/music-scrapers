from pydub import AudioSegment

# Set the ffmpeg path manually
AudioSegment.converter = r'C:\ffmpeg\bin\ffmpeg.exe'

# Function to convert WAV to MP3
def convert_wav_to_mp3(wav_file, mp3_file):
    # Load the WAV file
    audio = AudioSegment.from_wav(wav_file)
    
    # Export the audio in MP3 format
    audio.export(mp3_file, format="mp3")
    print(f"Conversion successful! {mp3_file} has been created.")

# Replace 'input.wav' with the path to your WAV file and 'output.mp3' with the desired MP3 output filename.
wav_file = 'prog1h.wav'
mp3_file = 'prog1h.mp3'

convert_wav_to_mp3(wav_file, mp3_file)
