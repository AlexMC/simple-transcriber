import argparse
import os
import requests
from whisper import load_model, transcribe

def parse_args():
    """ Parse command-line arguments for audio file path or URL """
    parser = argparse.ArgumentParser(description="Transcribe audio files using Whisper")
    parser.add_argument("audio_source", help="Path or URL to the audio file")
    return parser.parse_args()

def download_audio(url):
    """ Download audio file from URL """
    response = requests.get(url)
    filename = url.split("/")[-1]
    with open(filename, 'wb') as f:
        f.write(response.content)
    return filename

def transcribe_audio(audio_path):
    """ Load model, transcribe audio, and save results to a text file """
    # Load the Whisper model
    model = load_model("base")
    
    # Transcribe the audio
    result = model.transcribe(audio_path)
    
    # Get the base name of the audio file (without extension)
    base_filename = os.path.splitext(os.path.basename(audio_path))[0]
    
    # Create a txt file with the same base name
    txt_filename = f"{base_filename}.txt"
    
    # Write the transcription to the text file
    with open(txt_filename, 'w') as f:
        f.write(result['text'])
    
    # Also print the transcription in the console
    print(result['text'])
    print(f"Transcription saved to {txt_filename}")

def main():
    args = parse_args()
    audio_path = args.audio_source
    if audio_path.startswith('http://') or audio_path.startswith('https://'):
        audio_path = download_audio(audio_path)
    transcribe_audio(audio_path)

if __name__ == "__main__":
    main()
