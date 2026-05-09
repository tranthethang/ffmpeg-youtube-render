import os
from pathlib import Path
from .config import Config
from .image_processor import ImageProcessor
from .render_engine import RenderEngine

def main():
    # 1. Khởi tạo và kiểm tra cấu hình
    print("--- Khởi tạo hệ thống Render YouTube ---")
    Config.validate()

    # Kiểm tra FFmpeg
    if not Config.check_ffmpeg():
        print(f"LỖI: Không tìm thấy FFmpeg tại '{Config.FFMPEG_PATH}'.")
        print("Vui lòng cài đặt FFmpeg và thêm vào PATH hoặc cấu hình FFMPEG_PATH trong .env.")
        return

    # Kiểm tra GPU Support
    if not Config.check_gpu_support():
        print(f"LỖI: GPU hoặc Codec '{Config.VIDEO_CODEC}' không được hỗ trợ bởi bản FFmpeg này.")
        print("Nếu bạn dùng Mac chip M, hãy đổi VIDEO_CODEC thành 'hevc_videotoolbox' trong .env.")
        print("Nếu không có GPU NVIDIA, hãy đổi VIDEO_CODEC thành 'libx264'.")
        return

    print(f"Hệ thống sẵn sàng: FFmpeg và Codec '{Config.VIDEO_CODEC}' hợp lệ.")
    engine = RenderEngine()

    # 2. Quét danh sách file audio
    audio_files = list(Config.INPUT_DIR.glob("*.mp3"))
    if not audio_files:
        print(f"Không tìm thấy file .mp3 nào trong {Config.INPUT_DIR}")
        return

    print(f"Tìm thấy {len(audio_files)} file để xử lý.")

    # 3. Vòng lặp xử lý từng file
    for audio_path in audio_files:
        print(f"\n>>> Đang xử lý: {audio_path.name}")
        
        # Tạo tên output
        output_path = Config.OUTPUT_DIR / f"{audio_path.stem}.mp4"
        
        # Kiểm tra nếu file đã tồn tại (optional)
        if output_path.exists():
            print(f"Bỏ qua: {output_path.name} đã tồn tại.")
            continue

        try:
            # Tạo ảnh bìa tạm thời (thêm dấu # vào trước tên file)
            cover_text = f"#{audio_path.stem}"
            temp_cover = ImageProcessor.create_custom_cover(cover_text, audio_path.stem)
            
            # Thực hiện render
            success = engine.render(audio_path, temp_cover, output_path)
            
            # Dọn dẹp ảnh tạm
            if temp_cover.exists():
                os.remove(temp_cover)
                
            if success:
                print(f"Thành công: {audio_path.name}")
            else:
                print(f"Thất bại: {audio_path.name}")

        except Exception as e:
            print(f"Lỗi khi xử lý {audio_path.name}: {e}")

    print("\n--- Tất cả tác vụ đã hoàn thành ---")

if __name__ == "__main__":
    main()
