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
# Trên Ubuntu / Debian / Linux WSL:
    sudo apt update
    sudo apt install python3 python3-pip python3-venv -y
## Rồi kiểm tra:
    python3 --version
    pip3 --version

# Trên Windows:
    1. Truy cập: https://www.python.org/downloads/

    2. Tải bản Python 3.10+
        Nhớ tick ô “Add Python to PATH” khi cài!

## Kiểm tra sau khi cài:
        python3 --version
        pip3 --version

### 1. Cài đặt môi trường ảo (virtual environment)
    python3 -m venv venv
    source venv/bin/activate        # Trên Linux/macOS
    venv\Scripts\activate           # Trên Windows

### 2. Cài đặt thư viện
    pip install -r requirements.txt
### 3. Tải dữ liệu cho TextBlob (chạy một lần duy nhất)
    python -m textblob.download_corpora
### 4. Chạy server
    uvicorn main:app --reload
### 5. Truy cập hệ thống
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

## Câu hỏi mở rộng
1. Vấn đề khi nhiều người POST /analyze cùng lúc
- Vấn đề: Endpoint POST /analyze hiện tại xử lý đồng bộ (synchronous) – tức là upload xong thì server chờ chuyển đổi file bằng Whisper luôn.
        Với các file lớn, việc xử lý này rất tốn thời gian CPU.
        Nếu nhiều người upload cùng lúc, server sẽ bị tắc nghẽn, response chậm hoặc thậm chí treo/delay hàng loạt request.

- Giải pháp: Chuyển sang xử lý bất đồng bộ (asynchronous) bằng cách:
    * Khi user upload file -> hệ thống xếp hàng (queue) file để xử lý sau -> trả về call_id hoặc status: processing.
    * Một background worker (ví dụ dùng Celery, hoặc ThreadPool + asyncio) sẽ xử lý lần lượt các file trong queue.
    * Người dùng có thể truy vấn trạng thái xử lý qua endpoint GET /calls/{call_id}.
  => Lý do chọn giải pháp này: giúp hệ thống chịu tải tốt hơn, không block request, mở rộng dễ (scalable).

2. Làm sao để đánh giá cảm xúc (sentiment) chính xác hơn từ transcript?
- Hướng tiếp cận: 
    * Dùng thư viện NLP có sẵn: như TextBlob, VADER (cho tiếng Anh), hoặc underthesea/pyvi cho tiếng Việt để phân tích sentiment dựa trên từ ngữ tích cực/tiêu cực.
    * Fine-tune mô hình ML/AI: như BERT hoặc DistilBERT trên tập dữ liệu tiếng nói khách hàng (có label cảm xúc).
    * Sử dụng dịch vụ AI của bên thứ ba: như Google Cloud Natural Language API, AWS Comprehend, OpenAI API (nếu được phép dùng).
  => Có thể lưu trường sentiment: "positive" | "neutral" | "negative" trong Call để hiển thị/thống kê sau.

3. Tách /analyze thành microservice – nên dùng gì?
- Giải pháp:
    Tách /analyze thành 1 microservice riêng, và giao tiếp với backend chính qua Message Queue (ví dụ: RabbitMQ, Redis Queue, Kafka).

- Lý do dùng message queue?
    - Decouple: Tách biệt giữa việc nhận request và xử lý nặng.
    - Retry + Load Balancing: Có thể retry task fail, scale worker xử lý.
    - Không block API chính: /upload vẫn response nhanh, còn xử lý Whisper là việc của service khác.
      #### Có thể dùng REST API nội bộ gọi qua requests.post(...) sang container analyze, nhưng message queue vẫn tốt hơn về hiệu năng và ổn định.

## Ghi chú
- Hệ thống hiện sử dụng danh sách giả lập calls_db thay cho cơ sở dữ liệu thật.
- Tất cả chức năng đã có giao diện trực quan, dễ sử dụng.
- Giao diện chạy thuần HTML/JS, không cần framework frontend.

## Tác giả
Mạnh Cao Duy – Ứng viên tham gia bài test vị trí TTS AI tại NextX.
