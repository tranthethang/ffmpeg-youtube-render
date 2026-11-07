# Hướng dẫn Cài đặt Môi trường Render

Tài liệu này hướng dẫn cách cài đặt FFmpeg và cấu hình tăng tốc phần cứng (GPU) cho dự án `ffmpeg-youtube-render` trên các hệ điều hành khác nhau.

---

## 1. Windows (Dành cho NVIDIA GPU - RTX 3060...)

### Bước 1: Cài đặt FFmpeg
1. Truy cập [gyan.dev](https://www.gyan.dev/ffmpeg/builds/).
2. Tải bản **ffmpeg-git-full.7z** (hoặc bản Release full).
3. Giải nén vào một thư mục (ví dụ: `C:\ffmpeg`).
4. Thêm thư mục `bin` vào biến môi trường **PATH** của hệ thống:
   - Tìm kiếm "Environment Variables" -> "Edit the system environment variables".
   - Chọn "Environment Variables" -> Tìm "Path" trong "System variables" -> "Edit" -> "New" -> Dán đường dẫn `C:\ffmpeg\bin`.

### Bước 2: Cài đặt Driver & CUDA
1. Cài đặt Driver NVIDIA mới nhất từ [NVIDIA Website](https://www.nvidia.com/Download/index.aspx).
2. Tải và cài đặt [CUDA Toolkit](https://developer.nvidia.com/cuda-downloads).

### Bước 3: Kiểm tra
Mở Terminal/PowerShell và chạy:
```bash
ffmpeg -encoders | findstr nvenc
```
Nếu hiện ra `hevc_nvenc` và `h264_nvenc` là thành công.

---

## 2. Linux (Ubuntu/Debian)

### Bước 1: Cài đặt FFmpeg và Driver NVIDIA
Chạy các lệnh sau:
```bash
sudo apt update
sudo apt install ffmpeg nvidia-driver-535 nvidia-cuda-toolkit
```

### Bước 2: Kiểm tra
```bash
ffmpeg -encoders | grep nvenc
```

---

## 3. macOS (Chip Apple Silicon M1/M2/M3)

**Lưu ý:** Chip M của Apple không có NVIDIA GPU nên **không sử dụng được NVENC/CUDA**. Thay vào đó, chúng ta sử dụng **VideoToolbox** (bộ tăng tốc phần cứng của Apple).

### Bước 1: Cài đặt FFmpeg qua Homebrew
Nếu chưa có Homebrew, cài tại [brew.sh](https://brew.sh/). Sau đó chạy:
```bash
brew install ffmpeg
```

### Bước 2: Cấu hình lại dự án cho Mac
Bạn cần thay đổi codec trong file `.env`:
- Thay `VIDEO_CODEC=hevc_nvenc` bằng `VIDEO_CODEC=hevc_videotoolbox`.
- Thay `PRESET=p7` bằng `PRESET=quality` (hoặc xóa đi vì VideoToolbox có hệ thống tham số khác).

### Bước 3: Kiểm tra
```bash
ffmpeg -encoders | grep videotoolbox
```

---

## 4. Kiểm tra FFmpeg trong Python
Sau khi cài đặt xong, bạn có thể chạy script kiểm tra nhanh để đảm bảo FFmpeg đã có trong PATH:

```python
import subprocess
try:
    version = subprocess.check_output(["ffmpeg", "-version"])
    print("FFmpeg đã được cài đặt thành công!")
except FileNotFoundError:
    print("Lỗi: Không tìm thấy FFmpeg trong hệ thống.")
```

## 5. Cấu hình Project
Sau khi cài đặt xong phần cứng, hãy quay lại thư mục dự án và chạy:
1. `uv sync` (để cài đặt dependencies python).
2. Kiểm tra lại file `.env` để đảm bảo `FFMPEG_PATH=ffmpeg` (nếu bạn đã thêm vào PATH) hoặc trỏ trực tiếp đến file thực thi.
