# Life Stories Organizer

This repository contains scripts to organize the stories of your life by transcribing audio files, extracting key information, organizing the data chronologically, and creating a narrative storyline.

## Table of Contents

1. [Setup](#setup)
2. [Folder Structure](#folder-structure)
3. [Script Overview](#script-overview)
4. [Usage](#usage)
   - [Transcription](#transcription)
   - [Analysis](#analysis)
   - [Organization](#organization)
   - [Narrative Creation](#narrative-creation)
5. [Handling Different File Types](#handling-different-file-types)

## Setup

1. **Clone the Repository**

    ```bash
    git clone https://github.com/lucasbilma/transcription-scripts.git
    cd transcription-scripts
    ```

2. **Create a Virtual Environment**

    ```bash
    python -m venv newenv
    source newenv/bin/activate  # On Windows use `newenv\Scripts\activate`
    ```

3. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4. **Install FFmpeg**

    Follow the instructions to install FFmpeg from [FFmpeg's official site](https://ffmpeg.org/download.html).

## Folder Structure
Organize your working directory as follows:
D:/
└── 0 Pessoal/
├── Auto Analise/
│ ├── Not Transcribed Yet/
│ ├── Transcribed/
│ ├── wav_files/
│ ├── transcriptions/
│ ├── analysis/
│ ├── life-stories-organizer/
│ │ ├── transcription.py
│ │ ├── analysis.py
│ │ ├── organize.py
│ │ ├── narrative.py
│ │ ├── requirements.txt
│ │ └── README.md


## Script Overview

1. **transcription.py**
    - Converts audio files to WAV format.
    - Transcribes audio files to text files using the Whisper model.

2. **analysis.py**
    - Extracts key information from the transcriptions such as topics, events, and sentiments.

3. **organize.py**
    - Organizes the transcribed data chronologically.

4. **narrative.py**
    - Develops a narrative storyline based on the organized information.

## Usage

### Transcription

1. **Run the Transcription Script**

    ```bash
    python transcription.py
    ```

    This script will convert all audio files in the `Not Transcribed Yet` folder to WAV format and transcribe them to text files.

### Analysis

1. **Run the Analysis Script**

    ```bash
    python analysis.py
    ```

    This script will extract key information from the transcriptions and save the results in the `analysis` folder.

### Organization

1. **Run the Organization Script**

    ```bash
    python organize.py
    ```

    This script will organize the analyzed data chronologically and save the organized data to `organized_data.json`.

### Narrative Creation

1. **Run the Narrative Script**

    ```bash
    python narrative.py
    ```

    This script will create a narrative storyline based on the organized data and save it to `narrative.txt`.

## Handling Different File Types

To handle different file types such as WhatsApp audio files:

1. Place the audio files (e.g., .opus files from WhatsApp) in the `Not Transcribed Yet` folder.
2. Ensure the `transcription.py` script includes handling for the specific audio file types you are using.

### Example: Adding OPUS File Handling in `transcription.py`

Modify the `convert_audio_to_wav` function to handle .opus files:

```python
def convert_audio_to_wav(input_file, output_file):
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
