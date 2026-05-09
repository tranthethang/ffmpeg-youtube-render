from PIL import Image, ImageDraw, ImageFont
from .config import Config
from pathlib import Path

class ImageProcessor:
    @staticmethod
    def create_custom_cover(text: str, output_name: str):
        """
        Draw text on the cover template and save as a temporary image.
        """
        template_path = Config.ASSETS_DIR / "images" / "cover_template.png"
        output_path = Config.ASSETS_DIR / "images" / f"temp_{output_name}.png"

        if not template_path.exists():
            # Create a simple colored background if template doesn't exist for testing
            print(f"Warning: Template {template_path} not found. Creating a placeholder.")
            img = Image.new('RGBA', Config.get_video_resolution(), color=(73, 109, 137))
        else:
            print(f"Loading template from {template_path}")
            img = Image.open(template_path).convert("RGBA")

        # Ensure image is the correct resolution
        target_res = Config.get_video_resolution()
        if img.size != target_res:
            img = img.resize(target_res, Image.Resampling.LANCZOS)

        draw = ImageDraw.Draw(img)
        
        # Load font
        try:
            font = ImageFont.truetype(str(Config.FONT_FILE), Config.FONT_SIZE)
        except Exception as e:
            print(f"Error loading font {Config.FONT_FILE}: {e}. Falling back to default.")
            font = ImageFont.load_default()

        # Draw text
        # Calculate position based on margins and font metrics
        bbox = draw.textbbox((0, 0), text, font=font)
        # text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Bottom-left positioning
        # bbox is (left, top, right, bottom)
        # We want the visual left (x + bbox[0]) to be Config.TEXT_POSITION_X
        # We want the visual bottom (y + bbox[3]) to be target_res[1] - Config.TEXT_MARGIN_BOTTOM
        x = Config.TEXT_POSITION_X - bbox[0]
        y = target_res[1] - bbox[3] - Config.TEXT_MARGIN_BOTTOM
        
        # Log for debugging - using safe print for Windows console
        try:
            print(f"Drawing text at ({x}, {y}) [Visual bottom-left: ({Config.TEXT_POSITION_X}, {target_res[1] - Config.TEXT_MARGIN_BOTTOM})]")
        except:
            pass

        draw.text(
            (x, y),
            text,
            fill=Config.TEXT_COLOR,
            font=font
        )

        img.save(output_path)
        return output_path

if __name__ == "__main__":
    # Test the image processor
    test_text = "#467"
    ImageProcessor.create_custom_cover(test_text, "test")
    Config.validate()
    # Check if font exists, if not, this will use default
    result = ImageProcessor.create_custom_cover(test_text, "test")
    print(f"Test cover created at: {result}")
