# Call Analyzer - Backend xử lý âm thanh cuộc gọi

Dự án xây dựng hệ thống backend để xử lý các file âm thanh cuộc gọi (.mp3, .wav, .m4a, .ogg, .flac), phục vụ mục đích quản lý và phân tích nội dung. 

## Chức năng chính

- Upload file âm thanh
- Chuyển âm thanh thành văn bản (transcript) bằng mô hình Whisper (`faster-whisper`)
- Phân tích transcript: đếm từ, đếm câu, cảm xúc (sentiment), từ khóa
- Chatbot phản hồi theo nội dung nói (rule-based)
- Thống kê tổng hợp từ tất cả các file
- Giao diện web đơn giản (HTML/JS) để sử dụng trực tiếp

## Công nghệ sử dụng

- Python 3.10+
- FastAPI
- faster-whisper (nhẹ, nhanh)
- TextBlob (phân tích cảm xúc)
- ffmpeg-python + pydub (xử lý âm thanh)
- Uvicorn (server)
- HTML, JavaScript (giao diện người dùng)

## Cài đặt và chạy

### 0. Cài đặt python
- Trên Ubuntu / Debian / Linux WSL:
    sudo apt update
    sudo apt install python3 python3-pip python3-venv -y

    - Rồi kiểm tra:
        python3 --version
        pip3 --version
- Trên Windows:
    1. Truy cập: https://www.python.org/downloads/

    2. Tải bản Python 3.10+
        Nhớ tick ô “Add Python to PATH” khi cài!

    3. Kiểm tra sau khi cài:
        python3 --version
        pip3 --version
### 1. Cài đặt môi trường ảo (virtual environment)
    python3 -m venv venv
    source venv/bin/activate        # Trên Linux/macOS
    venv\Scripts\activate           # Trên Windows

### 1. Cài đặt thư viện
    pip install -r requirements.txt
### 2. Tải dữ liệu cho TextBlob (chạy một lần duy nhất)
    python -m textblob.download_corpora
### 3. Chạy server
    uvicorn main:app --reload
### 4. Truy cập hệ thống
    Giao diện người dùng: http://localhost:8000/

    Swagger UI (dành cho dev): http://localhost:8000/docs

## Các trang giao diện
| Trang              | Đường dẫn               | Mô tả                                     |
| ------------------ | ----------------------- | ----------------------------------------- |
| Trang chính        | `/`                     | Menu chọn tính năng                       |
| Upload file        | `/upload.html`          | Gửi file âm thanh để xử lý                |
| Danh sách cuộc gọi | `/calls.html`           | Hiển thị các cuộc gọi đã upload           |
| Phân tích cụ thể   | `/analyze.html?id={id}` | Hiển thị transcript và phân tích nội dung |
| Chatbot            | `/chatbot.html`         | Nhập nội dung và nhận phản hồi tự động    |
| Thống kê tổng hợp  | `/stats.html`           | Tổng hợp dữ liệu của tất cả các cuộc gọi  |

## Hỗ trợ định dạng âm thanh
- Các định dạng được hỗ trợ bao gồm: .mp3, .wav, .m4a, .ogg, .flac

- Việc xử lý âm thanh sử dụng ffmpeg (qua pydub) nên có thể mở rộng thêm nếu cần

- Nếu upload định dạng không hỗ trợ, hệ thống sẽ báo lỗi

## Ghi chú
- Hệ thống hiện sử dụng danh sách giả lập calls_db thay cho cơ sở dữ liệu thật.

- Tất cả chức năng đã có giao diện trực quan, dễ sử dụng.

- Giao diện chạy thuần HTML/JS, không cần framework frontend.

## Tác giả
Mạnh Cao Duy – Ứng viên tham gia bài test vị trí TTS AI tại NextX.