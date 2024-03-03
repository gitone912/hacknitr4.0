import whisper

def transcribe_mp3(file_path):
    try:
        # Load the Whisper ASR model
        model = whisper.load_model("tiny")

        # Transcribe the MP3 file
        result = model.transcribe(file_path)

        # Return the transcribed text
        return result["text"]

    except Exception as e:
        # Handle exceptions, e.g., file not found, model loading error, etc.
        print(f"Error: {e}")
        return None