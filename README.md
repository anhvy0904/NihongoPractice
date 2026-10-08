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

Ngữ pháp dựa trên bốn PDF 文型リスト Unit 9–12 do người dùng cung cấp. Dạng bài dựa trên Google Docs “Thao khảo”. Google Docs chỉ có đề mẫu, không có danh sách từ vựng riêng từng unit. Các từ vựng được bổ sung và phân bổ theo chủ đề từ đề mẫu và ví dụ PDF, không phải danh sách chính thức theo unit.

Mọi câu hỏi được biên soạn mới. Câu được xáo trộn và lựa chọn đáp án được xáo trộn mỗi lần bắt đầu. Đáp án hiện sau nộp bài; có thể xem lại và làm lại những câu chưa đúng. Bài làm chỉ nằm trong bộ nhớ của trang, mất khi tải lại hoặc đóng trang.
