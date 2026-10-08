# Nihongo Practice · Unit 9–12

Trang web tĩnh bằng HTML/CSS/JavaScript, không cần cài thư viện. Mở qua một HTTP server, không mở `index.html` trực tiếp với `file://` vì trình duyệt có thể chặn đọc JSON.

## Chạy tại máy

```powershell
cd E:\midterm_nihongo\nihongo
python -m http.server 8080 --directory dist
```

Mở `http://localhost:8080`.

## Ngân hàng câu hỏi

`dist/questions.json` chứa 320 câu: Unit 9–12, mỗi unit 40 từ vựng + 40 ngữ pháp.

- Từ vựng: 10 cách đọc, 8 chữ Hán, 10 điền từ, 6 gần nghĩa, 6 cách dùng.
- Ngữ pháp: 30 điền mẫu, 10 sắp xếp vị trí ★.
- `answer` là chỉ số **từ 0** trong mảng `options`.
- `orderedFragments` là thứ tự đúng của 4 mảnh; đáp án ★ ở vị trí thứ ba.
- Các câu có giải thích tiếng Việt.

Chạy `python build_questions.py` để biên soạn lại JSON từ nguồn có cấu trúc. Sửa trực tiếp JSON nếu không cần tái tạo; trình biên soạn sẽ ghi đè JSON khi chạy lại.

## Phạm vi tài liệu

Từ vựng và dạng bài theo bốn đề mẫu Unit 9–12 người dùng gửi trực tiếp. `exam_update.py` chứa dữ liệu cập nhật, được tích hợp bởi `build_questions.py`. Mỗi phần vẫn giữ 40 câu theo yêu cầu ban đầu. Các câu có ngữ cảnh, từ được gạch chân, hướng dẫn tiếng Nhật và lựa chọn 1–4. Một số phương án trùng hoặc gây nhiều đáp án trong đề mẫu đã được sửa. Không áp dụng giới hạn 10 phút của đề mẫu ngắn cho bài luyện 40 câu.

Bộ câu hỏi có câu mẫu và câu biên soạn thêm. Câu được chia theo dạng 問題1–5 (từ vựng) và 問題1–2 (ngữ pháp); lựa chọn đáp án được xáo trộn mỗi lần bắt đầu. Chọn đáp án 1–4 để chấm ngay, hiện đúng/sai và đáp án đúng trên câu hiện tại. Bấm **Câu tiếp** sau khi xem kết quả để chuyển câu. Sau khi hoàn thành 40 câu, tự mở lượt làm lại gồm những câu sai. Các câu vẫn sai tiếp tục được lặp lại theo lượt đến khi đúng hết. Tổng kết giữ điểm lượt đầu và hiển thị số lượt làm lại; xem đáp án cuối cùng cho toàn bộ 40 câu. Bài làm chỉ nằm trong bộ nhớ của trang, mất khi tải lại hoặc đóng trang.

## Từ vựng chung

`common_vocabulary.py` chứa 118 từ khác nhau trong bảng người dùng gửi. `対応する` bị lặp được gộp lại. `commonVocabulary` trong JSON có danh sách từ với cách đọc, nghĩa và ví dụ, cùng ngân hàng 347 câu hỏi. Mỗi lượt chọn 40 câu (10 cách đọc, 8 chữ Hán, 10 điền từ, 6 gần nghĩa, 6 cách dùng), ưu tiên các từ chưa chọn trong lượt đó. Các lượt có thể trùng nhau. Bốn unit và bộ 320 câu ban đầu không bị thay đổi.

## Thẻ học sau khi chấm

learning_data.py bổ sung thẻ học cho toàn bộ câu hỏi: furigana, âm Hán Việt cho chữ Hán, nghĩa, câu ví dụ có dịch, từ gần nghĩa và trái nghĩa hoặc đối chiếu. Có 22 thẻ mẫu ngữ pháp. Từ đối chiếu không được coi là trái nghĩa trực tiếp. Không gán cấp JLPT hoặc thống kê tần suất chính thức. Các thẻ nằm trong trường learning của questions.json.

Để biên soạn lại: cài requirements-learning.txt vào thư mục .libraries bằng pip install --target .libraries -r requirements-learning.txt, rồi chạy build_questions.py. Dữ liệu furigana được sinh bằng Janome, có sửa cách đọc các cụm như 九時, 仕入先 và 今日中.
