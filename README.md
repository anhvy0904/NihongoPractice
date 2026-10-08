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

Bộ câu hỏi có câu mẫu và câu biên soạn thêm. Câu được chia theo dạng 問題1–5 (từ vựng) và 問題1–2 (ngữ pháp); lựa chọn đáp án được xáo trộn mỗi lần bắt đầu. Đáp án hiện sau nộp bài; có thể xem lại và làm lại những câu chưa đúng. Bài làm chỉ nằm trong bộ nhớ của trang, mất khi tải lại hoặc đóng trang.
