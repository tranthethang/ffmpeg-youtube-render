import subprocess
import json
from .config import Config

class AudioProcessor:
    @staticmethod
    def get_duration(file_path):
        """Get the duration of an audio file using ffprobe."""
        cmd = [
            "ffprobe", 
            "-v", "error", 
            "-show_entries", "format=duration", 
            "-of", "default=noprint_wrappers=1:nokey=1", 
            str(file_path)
        ]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return float(result.stdout.strip())
        except Exception as e:
            print(f"Error getting duration for {file_path}: {e}")
            return 0

    @staticmethod
    def get_ffmpeg_trim_args():
        """Return a list of FFmpeg arguments for trimming based on config."""
        args = []
        if Config.AUDIO_TRIM_START and Config.AUDIO_TRIM_START != "00:00:00":
            args.extend(["-ss", Config.AUDIO_TRIM_START])
        
        # Note: -to or -t could be used for TRIM_END, but depends on whether 
        # it's an absolute timestamp or relative duration.
        # For simplicity, we assume AUDIO_TRIM_END is an absolute timestamp if provided.
        if Config.AUDIO_TRIM_END:
            args.extend(["-to", Config.AUDIO_TRIM_END])
            
        return args

if __name__ == "__main__":
    # Example usage
    print(f"Trim arguments: {AudioProcessor.get_ffmpeg_trim_args()}")
