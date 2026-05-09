import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
load_dotenv()

class Config:
    # --- Hardware & Paths ---
    FFMPEG_PATH = os.getenv("FFMPEG_PATH", "ffmpeg")
    ASSETS_DIR = Path(os.getenv("ASSETS_DIR", "./assets"))
    INPUT_DIR = Path(os.getenv("INPUT_DIR", "./input"))
    OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", "./output"))
    DONE_DIR = Path(os.getenv("DONE_DIR", "./done"))
    LOGS_DIR = Path("./logs")

    # --- Video Settings ---
    VIDEO_QUALITY = os.getenv("VIDEO_QUALITY", "480p")
    VIDEO_BITRATE = os.getenv("VIDEO_BITRATE", "1.5M")
    VIDEO_CODEC = os.getenv("VIDEO_CODEC", "hevc_nvenc")
    SELECTED_SAMPLE = os.getenv("SELECTED_SAMPLE", "sample_01.m4v")

    # --- Layer Order ---
    LAYER_VIDEO_ORDER = int(os.getenv("LAYER_VIDEO_ORDER", "1"))
    LAYER_OVERLAY_ORDER = int(os.getenv("LAYER_OVERLAY_ORDER", "2"))
    LAYER_COVER_ORDER = int(os.getenv("LAYER_COVER_ORDER", "3"))

    # --- Audio Settings ---
    AUDIO_TRIM_START = os.getenv("AUDIO_TRIM_START", "00:00:00")
    AUDIO_TRIM_END = os.getenv("AUDIO_TRIM_END", None)
    if not AUDIO_TRIM_END or AUDIO_TRIM_END.lower() == "optional":
        AUDIO_TRIM_END = None
    AUDIO_BITRATE = os.getenv("AUDIO_BITRATE", "128k")

    # --- Text/Font Settings ---
    FONT_FILE = Path(os.getenv("FONT_FILE", "./assets/fonts/Roboto-Bold.ttf"))
    FONT_SIZE = int(os.getenv("FONT_SIZE", "60"))
    
    # TEXT_COLOR format: R,G,B,A
    text_color_str = os.getenv("TEXT_COLOR", "255,255,255,255")
    TEXT_COLOR = tuple(map(int, text_color_str.split(",")))
    
    TEXT_POSITION_X = int(os.getenv("TEXT_POSITION_X", "10"))
    TEXT_POSITION_Y = int(os.getenv("TEXT_POSITION_Y", "220"))
    TEXT_MARGIN_BOTTOM = int(os.getenv("TEXT_MARGIN_BOTTOM", "10"))

    @classmethod
    def validate(cls):
        """Validate that essential directories and files exist."""
        cls.ASSETS_DIR.mkdir(parents=True, exist_ok=True)
        cls.INPUT_DIR.mkdir(parents=True, exist_ok=True)
        cls.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        cls.DONE_DIR.mkdir(parents=True, exist_ok=True)
        cls.LOGS_DIR.mkdir(parents=True, exist_ok=True)
        
        # Check assets subdirectories
        (cls.ASSETS_DIR / "fonts").mkdir(parents=True, exist_ok=True)
        (cls.ASSETS_DIR / "images").mkdir(parents=True, exist_ok=True)
        (cls.ASSETS_DIR / "samples").mkdir(parents=True, exist_ok=True)

        print("Configuration validated successfully.")

    @classmethod
    def check_ffmpeg(cls):
        """Kiểm tra xem FFmpeg có tồn tại trong hệ thống không."""
        import subprocess
        try:
            subprocess.run([cls.FFMPEG_PATH, "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            return True
        except (FileNotFoundError, subprocess.CalledProcessError):
            return False

    @classmethod
    def check_gpu_support(cls):
        """Kiểm tra xem Codec đã chọn (ví dụ nvenc) có được FFmpeg hỗ trợ không."""
        import subprocess
        try:
            result = subprocess.run([cls.FFMPEG_PATH, "-encoders"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
            return cls.VIDEO_CODEC in result.stdout
        except (FileNotFoundError, subprocess.CalledProcessError):
            return False

    @classmethod
    def get_video_resolution(cls):
        """Map quality string to resolution."""
        resolutions = {
            "720p": (1280, 720),
            "480p": (854, 480),
            "360p": (640, 360)
        }
        return resolutions.get(cls.VIDEO_QUALITY, (854, 480))

if __name__ == "__main__":
    Config.validate()
    print(f"Video Quality: {Config.VIDEO_QUALITY}")
    print(f"Resolution: {Config.get_video_resolution()}")
    print(f"Text Color: {Config.TEXT_COLOR}")
