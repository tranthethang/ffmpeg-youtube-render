# ffmpeg-youtube-render

Hệ thống tự động hóa render video từ audio tối ưu cho YouTube, hỗ trợ tăng tốc phần cứng (NVIDIA NVENC/Apple VideoToolbox).

## Cấu trúc dự án
```text
ffmpeg-youtube-render/
├── app/                # Code logic chính
│   ├── main.py         # Entry point
│   ├── config.py       # Cấu hình
│   ├── render_engine.py # Xử lý FFmpeg
│   └── ...
├── tests/              # Unit tests
├── assets/             # Tài nguyên (fonts, images, samples)
├── input/              # Audio đầu vào (.mp3)
├── output/             # Video kết quả (.mp4)
└── .env                # Cấu hình môi trường
```

## Cách chạy
Để chạy ứng dụng từ thư mục gốc:
```bash
uv run python -m app.main
```

## Chạy Tests
```bash
uv run python -m unittest discover tests
```

Xem chi tiết cài đặt tại [SETUP.md](./SETUP.md).
