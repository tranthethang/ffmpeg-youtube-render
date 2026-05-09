# Tài liệu Mô tả Dự án: ffmpeg-audio-to-video

## 1. Tổng quan

Dự án nhằm mục đích tự động hóa quy trình chuyển đổi tệp âm thanh (MP3) thành video (MP4) chất lượng cao bằng cách kết hợp nhiều lớp hình ảnh và video lặp lại (loop). Hệ thống được tối ưu hóa đặc biệt để tận dụng sức mạnh phần cứng của card đồ họa **NVIDIA RTX 3060 12GB** thông qua công nghệ NVENC.

## 2. Kiến trúc Hệ thống & Công nghệ

* **Ngôn ngữ lập trình:** Python.
* **Quản lý gói & Môi trường:** sử dụng **UV** và `pyproject.toml` để đảm bảo tốc độ cài đặt và tính nhất quán của môi trường.
* **Xử lý Media:** **FFmpeg** (với hỗ trợ CUDA và HEVC NVENC).
* **Xử lý hình ảnh:** **Pillow (PIL)** để tạo ảnh cover động.
* **Quản lý cấu hình:** **python-dotenv** để đọc thông số từ tệp `.env`.

## 3. Cấu trúc Thư mục Đề xuất

```text
ffmpeg-audio-to-video/
├── .env                # Lưu trữ các thông số cấu hình (Không commit file này)
├── pyproject.toml      # Cấu hình dự án và dependencies cho UV
├── main.py             # Script điều phối chính
├── assets/             # Chứa các tài nguyên tĩnh
│   ├── cover.png       # Template ảnh bìa
│   ├── overlay.png     # Lớp phủ (trong suốt)
│   └── samples/        # Chứa nhiều file video gốc (.m4v)
├── input/              # Chứa các tệp audio đầu vào (.mp3)
└── output/             # Kết quả video đầu ra (.mp4)

```

## 4. Quản lý Cấu hình (.env)

Dự án tuyệt đối không hardcode. Các thông số sau sẽ được đọc từ tệp `.env`:

```ini
# Hardware & Path
FFMPEG_PATH=ffmpeg
ASSETS_DIR=./assets
INPUT_DIR=./input
OUTPUT_DIR=./output

# Video Settings
VIDEO_RESOLUTION=640x480
VIDEO_BITRATE=1.5M
VIDEO_CODEC=hevc_nvenc
PRESET=p7

# Audio Settings
AUDIO_TRIM_START=00:01:10
AUDIO_BITRATE=96k

# Cover Text Settings
FONT_PATH=C:/Windows/Fonts/arial.ttf
FONT_SIZE=80
TEXT_COLOR=255,255,255,255
TEXT_POSITION=50,950

```

## 5. Quy trình xử lý (Workflow)

1. **Khởi tạo:** Quét thư mục `input/` để lấy danh sách các tệp MP3.
2. **Xử lý Ảnh bìa:** Với mỗi tệp audio, chương trình dùng Pillow để vẽ số Chapter (hoặc tên tệp) lên tệp `assets/cover.png` dựa trên tọa độ trong `.env`.
3. **Lựa chọn Sample:** Chương trình có thể chọn ngẫu nhiên hoặc theo thứ tự một tệp `.m4v` trong thư mục `assets/samples/`.
4. **Thực thi FFmpeg:** Gọi lệnh FFmpeg thông qua `subprocess` với các tham số tối ưu:
* Hạ độ phân giải xuống 480p để tiết kiệm dung lượng.
* Sử dụng `hevc_nvenc` để render nhanh bằng GPU 3060.
* Cắt bỏ đoạn đầu audio (`-ss`) theo thông số cấu hình.
* Lặp lại video đầu vào (`-stream_loop -1`) cho khớp với độ dài audio.
* Chồng 4 lớp theo thứ tự: Sample Video -> Overlay -> Cover -> Audio.


5. **Hoàn tất:** Xuất file MP4 vào thư mục `output/` với tên trùng với file audio gốc.

## 6. Lệnh FFmpeg Core (Tham khảo)

```powershell
ffmpeg -hwaccel cuda -stream_loop -1 -i assets/samples/sample_1.m4v -loop 1 -i assets/overlay.png -loop 1 -i cover_temp.png -ss 00:01:10 -i input/audio.mp3 -filter_complex "[0:v]scale=-2:480,setpts=PTS-STARTPTS[v]; [v][1:v]scale=-2:480[ov]; [2:v]scale=-2:480[cv]; [ov][cv]overlay=shortest=1[f]" -map "[f]" -map 3:a -c:v hevc_nvenc -preset p7 -cq 32 -b:v 1.5M -c:a aac -b:a 96k -shortest output/video.mp4

```
