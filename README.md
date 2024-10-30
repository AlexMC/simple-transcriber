# Audio Transcriber

A command-line tool that transcribes audio files to text using OpenAI's Whisper model. It supports local files and URLs, shows progress during transcription, and can handle various audio formats.

## Features

- **Transcribe audio files** from local paths or URLs
- **Support for multiple audio formats**: MP3, WAV, M4A, OGG
- **Progress indication** during transcription
- **Automatic clipboard copying** of transcription
- **Optional saving** to a text file
- **Memory-efficient chunked processing** for large files

## Prerequisites

- **Python 3.7** or higher
- **ffmpeg** (required by pydub for audio processing)

### Installing ffmpeg

- **Ubuntu/Debian:**
  ```bash
  sudo apt update
  sudo apt install ffmpeg
  ```

- **macOS:**
  ```bash
  brew install ffmpeg
  ```

- **Windows:**
  Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to system PATH

## Installation

1. **Clone the repository:**
   ```bash
   git clone [your-repo-url]
   cd audio-transcriber
   ```

2. **Create and activate a virtual environment (recommended):**

   - **Linux/macOS:**
     ```bash
     python -m venv venv
     source venv/bin/activate
     ```

   - **Windows:**
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```

3. **Install required Python packages:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Make the script executable and create a system-wide command:**

   - **Linux/macOS:**
     ```bash
     chmod +x transcribe.py
     sudo ln -s "$(pwd)/transcribe.py" /usr/local/bin/transcribe
     ```

   - **Windows:**
     1. Add the script directory to your system PATH
     2. Create a batch file named `transcribe.bat` in the same directory:
        ```batch
        @echo off
        python "%~dp0transcribe.py" %*
        ```

## Usage

- **Basic usage:**
  ```bash
  transcribe path/to/audio.mp3
  ```

- **With output file:**
  ```bash
  transcribe path/to/audio.mp3 -o /output/directory
  ```

- **From URL:**
  ```bash
  transcribe https://example.com/audio.mp3
  ```

### Command-line Options

- `audio_source`: Path or URL to the audio file (required)
- `-o, --output`: Directory to save the transcription file (optional)

## Supported Audio Formats

- MP3 (.mp3)
- WAV (.wav)
- M4A (.m4a)
- OGG (.ogg)

## How It Works

1. Validates the input (local file or URL)
2. Downloads the audio file if it's a URL
3. Loads the Whisper model (tiny.en)
4. Splits the audio into 30-second chunks for efficient processing
5. Transcribes each chunk with progress indication
6. Combines the transcriptions
7. Copies the result to the clipboard and optionally saves it to a file
8. Cleans up temporary files and frees memory

## Dependencies

The tool relies on the following Python packages:
- **openai-whisper**: Core transcription functionality (includes torch as a dependency)
- **tqdm**: Progress bar display
- **requests**: URL handling and downloads
- **pyperclip**: Clipboard operations
- **pydub**: Audio file processing and chunking

### System Dependencies
- **ffmpeg**: Required by pydub for audio processing

## Troubleshooting

### Common Issues

1. **ffmpeg not found:**
   - Ensure ffmpeg is installed and in your system PATH
   - Try running `ffmpeg -version` to verify installation

2. **Clipboard access error:**
   - On Linux, install xclip: `sudo apt-get install xclip`
   - On Windows, ensure you have access to the clipboard

3. **Memory issues with large files:**
   - The tool automatically processes audio in chunks
   - If still experiencing issues, try closing other applications

### Error Messages

- "File does not exist": Check the file path and permissions
- "Not a supported audio format": Convert your audio to a supported format
- "Could not copy to clipboard": Check clipboard access permissions