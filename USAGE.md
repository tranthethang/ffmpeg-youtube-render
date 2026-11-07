# Hướng dẫn sử dụng (USAGE)

Tài liệu này hướng dẫn cách sử dụng công cụ `ffmpeg-youtube-render` để tạo video từ các file âm thanh (MP3) với hiệu ứng hình ảnh chuyên nghiệp.

---

## 1. Chuẩn bị

Trước khi bắt đầu, hãy đảm bảo bạn đã hoàn thành các bước trong [SETUP.md](./SETUP.md):
1. Cài đặt **FFmpeg**.
2. Cài đặt **Python** và **uv**.
3. Chạy `uv sync` để cài đặt thư viện cần thiết.
4. Kiểm tra hỗ trợ GPU (NVIDIA NVENC hoặc Apple VideoToolbox).

## 2. Cấu hình hệ thống (`.env`)

Tạo file `.env` từ file mẫu `.env.example` và điều chỉnh các tham số sau:

### Cấu hình đường dẫn:
- `INPUT_DIR`: Thư mục chứa các file nhạc `.mp3` đầu vào (mặc định: `./input`).
- `OUTPUT_DIR`: Thư mục chứa video `.mp4` sau khi render (mặc định: `./output`).
- `FFMPEG_PATH`: Đường dẫn đến file thực thi ffmpeg (mặc định: `ffmpeg`).

### Cấu hình Video:
- `VIDEO_CODEC`: 
  - `hevc_nvenc`: Dành cho Card đồ họa NVIDIA (Windows/Linux).
  - `hevc_videotoolbox`: Dành cho Mac chip M1/M2/M3.
  - `libx264`: Sử dụng CPU (chậm hơn nhưng tương thích mọi máy).
- `VIDEO_QUALITY`: Chất lượng video (`720p`, `480p`, `360p`).
- `SELECTED_SAMPLE`: Tên file video nền trong thư mục `assets/samples/`.

### Cấu hình Văn bản (Text on Cover):
- `FONT_FILE`: Đường dẫn đến file font chữ `.ttf`.
- `TEXT_COLOR`: Màu chữ định dạng R,G,B,A (ví dụ: `255,255,255,255` cho màu trắng).
- `TEXT_POSITION_X` & `TEXT_POSITION_Y`: Tọa độ hiển thị tên bài hát trên ảnh bìa.

---

## 3. Quy trình sử dụng

### Bước 1: Chuẩn bị tài nguyên
1. Copy các file nhạc `.mp3` bạn muốn render vào thư mục `input/`.
2. Đảm bảo đã có file video nền trong `assets/samples/` và file overlay trong `assets/images/overlay.png`.

### Bước 2: Chạy chương trình
Mở Terminal/PowerShell tại thư mục gốc của dự án và chạy lệnh:

```bash
uv run python -m app.main
```

### Bước 3: Kiểm tra kết quả
- Chương trình sẽ quét toàn bộ file `.mp3` trong thư mục `input/`.
- Với mỗi file, nó sẽ tự động tạo một ảnh bìa tạm thời chứa tên file.
- Tiến trình render sẽ bắt đầu. Bạn có thể theo dõi tiến độ qua Terminal.
- Sau khi hoàn tất, video sẽ xuất hiện trong thư mục `output/`.

---

## 4. Các lỗi thường gặp

- **Lỗi không tìm thấy FFmpeg**: Đảm bảo bạn đã thêm FFmpeg vào PATH hoặc khai báo đúng đường dẫn trong `FFMPEG_PATH`.
- **Lỗi GPU (NVENC/VideoToolbox)**: 
  - Nếu máy không có GPU, hãy đổi `VIDEO_CODEC` thành `libx264`.
  - Nếu dùng Mac, đảm bảo dùng `hevc_videotoolbox`.
- **Lỗi Font chữ**: Đảm bảo đường dẫn `FONT_FILE` trong `.env` là chính xác.
- **Input trống**: Kiểm tra xem file nhạc có đúng định dạng `.mp3` và nằm trong thư mục `input/` hay không.

---

## 5. Mẹo tối ưu
- Sử dụng **NVENC** (GPU NVIDIA) sẽ giúp tốc độ render nhanh hơn gấp 5-10 lần so với CPU.
- Nếu bạn muốn render nhiều file cùng lúc, chỉ cần bỏ tất cả vào thư mục `input/`, tool sẽ xử lý lần lượt theo vòng lặp.
- Tên file `.mp3` nên đặt rõ ràng vì nó sẽ được dùng để in lên ảnh bìa video.
