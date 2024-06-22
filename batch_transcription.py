import os  # 1
import subprocess  # 2
from pathlib import Path  # 3
from pydub import AudioSegment  # 4
import numpy as np  # 5
from scipy.io import wavfile  # 6
import whisper  # 7
import psutil  # 8

# 9 Paths
input_folder = Path("D:/0 Pessoal/Auto Analise")
output_wav_folder = input_folder / "wav_files"
output_txt_folder = input_folder / "transcriptions"
transcribed_folder = input_folder / "Transcribed"
not_transcribed_folder = input_folder / "Not Transcribed Yet"

# 10 Create output folders if they don't exist
output_wav_folder.mkdir(exist_ok=True)
output_txt_folder.mkdir(exist_ok=True)
transcribed_folder.mkdir(exist_ok=True)
not_transcribed_folder.mkdir(exist_ok=True)

# 11 Initialize Whisper models
models = {
    "base": whisper.load_model("base"),
    "small": whisper.load_model("small"),
    "medium": whisper.load_model("medium"),
    "large": whisper.load_model("large")
}

# 12 Function to calculate audio quality
def calculate_audio_quality(audio_path):
    # 13 Load audio file
    audio = AudioSegment.from_file(audio_path)
    samples = np.array(audio.get_array_of_samples())
    
    # 14 Calculate RMS (Root Mean Square) to get volume level
    rms = np.sqrt(np.mean(samples**2))
    
    # 15 Calculate signal-to-noise ratio (SNR)
    snr = 10 * np.log10(np.mean(samples**2) / np.var(samples))
    
    return rms, snr

# 16 Function to select appropriate model based on audio quality
def select_model(rms, snr):
    # 17 Define thresholds (these are example values, adjust based on your data)
    if snr > 30 and rms > 1000:
        return "large"
    elif snr > 20 and rms > 500:
        return "medium"
    elif snr > 10 and rms > 100:
        return "small"
    else:
        return "base"

# 18 Function to convert .MOV to .WAV
def convert_mov_to_wav(input_file, output_file):
    if not output_file.exists():
        command = [
            "ffmpeg",
            "-i", str(input_file),
            str(output_file)
        ]
        try:
            subprocess.run(command, check=True)
            print(f"Successfully converted {input_file} to {output_file}")
        except subprocess.CalledProcessError as e:
            print(f"Error converting {input_file} to {output_file}: {e}")
    else:
        print(f"{output_file} already exists. Skipping conversion.")

# 19 Function to transcribe .WAV to .TXT
def transcribe_wav_to_txt(input_file, output_file, model_name):
    model = models[model_name]
    if not output_file.exists():
        try:
            result = model.transcribe(str(input_file))
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(result["text"])
            print(f"Successfully transcribed {input_file} to {output_file} using {model_name} model")
        except Exception as e:
            print(f"Error transcribing {input_file} with {model_name} model: {e}")
    else:
        print(f"{output_file} already exists. Skipping transcription.")

# 20 Function to log resource usage
def log_resource_usage():
    process = psutil.Process(os.getpid())
    print(f"Memory Usage: {process.memory_info().rss / (1024 * 1024):.2f} MB")
    print(f"CPU Usage: {psutil.cpu_percent()}%")

# 21 Process files in batches
batch_size = 1
mov_files = list(input_folder.glob("*.MOV"))

for i in range(0, len(mov_files), batch_size):
    batch_files = mov_files[i:i+batch_size]
    for mov_file in batch_files:
        wav_file = output_wav_folder / (mov_file.stem + ".wav")
        txt_file = output_txt_folder / (mov_file.stem + ".txt")
        
        try:
            convert_mov_to_wav(mov_file, wav_file)
            
            # 22 Calculate audio quality
            rms, snr = calculate_audio_quality(wav_file)
            print(f"Audio quality for {wav_file} - RMS: {rms}, SNR: {snr}")
            
            # 23 Select appropriate Whisper model
            model_name = select_model(rms, snr)
            print(f"Selected model for {wav_file}: {model_name}")
            
            transcribe_wav_to_txt(wav_file, txt_file, model_name)
            
            # 24 Move processed .MOV files to "Transcribed" folder if transcription succeeded
            if txt_file.exists():
                mov_file.rename(transcribed_folder / mov_file.name)
                print(f"Moved {mov_file} to {transcribed_folder / mov_file.name}")
            
            log_resource_usage()
        except Exception as e:
            print(f"Error processing {mov_file}: {e}")
    
    print(f"Processed batch {i//batch_size + 1} of {len(mov_files)//batch_size + 1}")

# 25 Move untranscribed .MOV files to "Not Transcribed Yet" folder
for mov_file in input_folder.glob("*.MOV"):
    if not (output_txt_folder / (mov_file.stem + ".txt")).exists():
        mov_file.rename(not_transcribed_folder / mov_file.name)
        print(f"Moved {mov_file} to {not_transcribed_folder / mov_file.name}")

# 26 List files that were not processed successfully
not_converted = [mov_file for mov_file in input_folder.glob("*.MOV") if not (output_wav_folder / (mov_file.stem + ".wav")).exists()]
not_transcribed = [wav_file for wav_file in output_wav_folder.glob("*.wav") if not (output_txt_folder / (wav_file.stem + ".txt")).exists()]

print("\nFiles not converted to WAV:")
for file in not_converted:
    print(file)

print("\nFiles not transcribed to TXT:")
for file in not_transcribed:
    print(file)
