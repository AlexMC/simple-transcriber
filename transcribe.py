#!/usr/bin/env python3
import argparse
import os
import requests
import sys
import pyperclip
from pathlib import Path
from whisper import load_model, transcribe
import torch
from tqdm import tqdm
from pydub import AudioSegment
from pydub.utils import make_chunks
import warnings
import gc  # For garbage collection
import time  # For adding a small delay between chunks
import whisper  # Add this import

warnings.filterwarnings("ignore")

def parse_args():
    """ Parse command-line arguments for audio file path or URL """
    parser = argparse.ArgumentParser(description="Transcribe audio files using Whisper")
    parser.add_argument("audio_source", help="Path or URL to the audio file")
    parser.add_argument(
        "-o", "--output",
        help="Directory to save the transcription file (optional)",
        type=str,
        default=None
    )
    
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)
        
    args = parser.parse_args()
    
    # Validate output directory if specified
    if args.output:
        output_path = Path(args.output)
        if not output_path.exists():
            print(f"Error: Output directory '{args.output}' does not exist")
            sys.exit(1)
        if not output_path.is_dir():
            print(f"Error: '{args.output}' is not a directory")
            sys.exit(1)
    
    return args

def download_audio(url):
    """ Download audio file from URL with streaming """
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        filename = url.split("/")[-1]
        total_size = int(response.headers.get('content-length', 0))
        
        with open(filename, 'wb') as f, tqdm(
            desc="Downloading",
            total=total_size,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as pbar:
            for data in response.iter_content(chunk_size=1024):
                size = f.write(data)
                pbar.update(size)
        return filename
        
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")
        sys.exit(1)

def validate_audio_file(path):
    """Validate that the audio file exists and has the correct extension"""
    file_path = Path(path)
    if not file_path.exists():
        print(f"Error: File '{path}' does not exist")
        sys.exit(1)
        
    if not file_path.suffix.lower() in ['.mp3', '.wav', '.m4a', '.ogg']:
        print(f"Error: File '{path}' is not a supported audio format (mp3, wav, m4a, or ogg)")
        sys.exit(1)
    
    return str(file_path)

def transcribe_audio(audio_path, output_dir=None):
    print("Loading model...")
    model = whisper.load_model("tiny.en")
    
    try:
        print("Loading audio file...")
        audio = AudioSegment.from_file(audio_path)
        
        # Split into 30-second chunks
        chunk_length = 30 * 1000  # 30 seconds in milliseconds
        chunks = make_chunks(audio, chunk_length)
        
        print(f"\nProcessing {len(chunks)} chunks...")
        transcription = ""
        
        for i, chunk in enumerate(tqdm(chunks, desc="Transcribing")):
            # Export chunk to temporary file
            temp_path = f"temp_chunk_{i}.wav"
            chunk.export(temp_path, format="wav")
            
            # Transcribe chunk
            result = model.transcribe(
                temp_path,
                fp16=False,
                language="en",
                task="transcribe",
                best_of=1,
                beam_size=1
            )
            
            transcription += result["text"] + " "
            
            # Clean up temporary file
            os.remove(temp_path)
            
            # Small delay to prevent potential memory issues
            time.sleep(0.1)
        
        # Copy to clipboard
        try:
            pyperclip.copy(transcription)
            print("\nTranscription copied to clipboard!")
        except Exception as e:
            print(f"\nWarning: Could not copy to clipboard: {e}")
        
        print("\nTranscription:")
        print(transcription)
        
        # Save to file if output directory specified
        if output_dir:
            base_filename = os.path.splitext(os.path.basename(audio_path))[0]
            output_path = Path(output_dir) / f"{base_filename}.txt"
            
            try:
                with open(output_path, 'w') as f:
                    f.write(transcription)
                print(f"\nTranscription saved to: {output_path}")
            except Exception as e:
                print(f"Error saving transcription file: {e}")
                sys.exit(1)
                
    except Exception as e:
        print(f"Error during transcription: {e}")
        sys.exit(1)
    finally:
        del model
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

def main():
    args = parse_args()
    audio_path = args.audio_source
    
    if audio_path.startswith(('http://', 'https://')):
        audio_path = download_audio(audio_path)
    else:
        audio_path = validate_audio_file(audio_path)
        
    try:
        transcribe_audio(audio_path, args.output)
    except Exception as e:
        print(f"Error during transcription: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
