import subprocess
import os
from pathlib import Path
from .config import Config
from .audio_processor import AudioProcessor

class RenderEngine:
    def __init__(self):
        self.ffmpeg_path = Config.FFMPEG_PATH
        Config.validate()

    def build_filter_complex(self, has_overlay=True, has_cover=True):
        """
        Xây dựng chuỗi filter_complex dựa trên thứ tự lớp trong .env
        Thứ tự: 0:v (Sample Video), 1:v (Overlay), 2:v (Cover)
        """
        # Mapping index và order
        layers = []
        layers.append({'idx': '0:v', 'order': Config.LAYER_VIDEO_ORDER, 'label': 'vid'})
        
        if has_overlay:
            layers.append({'idx': '1:v', 'order': Config.LAYER_OVERLAY_ORDER, 'label': 'ovl'})
        
        if has_cover:
            # Lưu ý: Cover thường là ảnh thứ 2 nếu có overlay, hoặc thứ 1 nếu không
            cover_idx = '2:v' if has_overlay else '1:v'
            layers.append({'idx': cover_idx, 'order': Config.LAYER_COVER_ORDER, 'label': 'cvr'})

        # Sắp xếp các lớp theo order tăng dần (lớp nào order thấp sẽ được vẽ trước)
        layers.sort(key=lambda x: x['order'])

        filters = []
        res = Config.get_video_resolution()
        res_str = f"{res[0]}:{res[1]}"

        # Bước 1: Scale lớp nền đầu tiên
        first = layers[0]
        filters.append(f"[{first['idx']}]scale={res_str},setpts=PTS-STARTPTS[l0]")

        # Bước 2: Chồng các lớp tiếp theo
        current_label = "l0"
        for i in range(1, len(layers)):
            layer = layers[i]
            next_label = f"l{i}"
            # Scale lớp sắp chồng lên
            filters.append(f"[{layer['idx']}]scale={res_str}[temp{i}]")
            # Overlay
            filters.append(f"[{current_label}][temp{i}]overlay=shortest=1[{next_label}]")
            current_label = next_label

        return ";".join(filters), current_label

    def render(self, audio_path, cover_path, output_path):
        """Thực thi lệnh FFmpeg để render video."""
        sample_path = Config.ASSETS_DIR / "samples" / Config.SELECTED_SAMPLE
        overlay_path = Config.ASSETS_DIR / "images" / "overlay.png"

        if not sample_path.exists():
            raise FileNotFoundError(f"Không tìm thấy sample video: {sample_path}")

        # Chuẩn bị inputs
        inputs = [
            "-hwaccel", "cuda",
            "-stream_loop", "-1", "-i", str(sample_path)  # 0:v
        ]
        
        has_overlay = overlay_path.exists()
        if has_overlay:
            inputs.extend(["-loop", "1", "-i", str(overlay_path)]) # 1:v
        
        inputs.extend(["-loop", "1", "-i", str(cover_path)]) # 2:v (nếu có overlay)

        # Thêm audio input với trim
        trim_args = AudioProcessor.get_ffmpeg_trim_args()
        inputs.extend(trim_args)
        inputs.extend(["-i", str(audio_path)]) # audio index sẽ là 2 hoặc 3

        audio_idx = "3:a" if has_overlay else "2:a"

        # Build filter
        filter_str, final_label = self.build_filter_complex(has_overlay=has_overlay)

        # Lệnh FFmpeg tổng thể
        cmd = [
            self.ffmpeg_path,
            *inputs,
            "-filter_complex", filter_str,
            "-map", f"[{final_label}]",
            "-map", audio_idx,
            "-c:v", Config.VIDEO_CODEC,
            "-preset", "p7",
            "-cq", "32",
            "-b:v", Config.VIDEO_BITRATE,
            "-c:a", "aac",
            "-b:a", Config.AUDIO_BITRATE,
            "-shortest",
            "-y", # Ghi đè file nếu tồn tại
            str(output_path)
        ]

        print(f"Đang thực thi lệnh FFmpeg cho: {audio_path.name}")
        
        log_file = Config.LOGS_DIR / f"{output_path.stem}.log"
        with open(log_file, "w") as f:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                encoding='utf-8'
            )
            for line in process.stdout:
                f.write(line)
            
            process.wait()
            if process.returncode != 0:
                print(f"Lỗi render: Kiểm tra log tại {log_file}")
                return False
            
            print(f"Hoàn tất: {output_path}")
            return True

if __name__ == "__main__":
    # Test cấu trúc filter
    engine = RenderEngine()
    f_str, label = engine.build_filter_complex()
    print(f"Filter string: {f_str}")
    print(f"Final label: {label}")
