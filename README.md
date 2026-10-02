# Ôn tập Sinh Học Di Truyền 10-2026

Web ôn tập trắc nghiệm Sinh Học Di Truyền — **210 câu hỏi, 7 bài**, trích tự động từ đề ôn
tập gốc (đáp án tô vàng trong PDF), kèm **giải thích & mẹo ghi nhớ cho từng câu** bám theo
slide bài giảng. Xây bằng **React + Vite + TailwindCSS**.

| Bài | Nội dung | Số câu |
|-----|----------|--------|
| 1 | Sinh học, khoa học của sự sống | 16 |
| 2 | Sinh học tế bào | 48 |
| 3 | Năng lượng sinh học | 25 |
| 4 | Cơ sở phân tử của di truyền học | 37 |
| 5 | Sự phân chia tế bào | 8 |
| 6 | Các quy luật di truyền | 43 |
| 7 | Sự phát sinh giao tử, thụ tinh và phát triển của phôi ở người | 33 |

## Tính năng
- **Kiểm tra thử** — làm bài có chấm điểm, chọn bài & số câu, xáo trộn câu và đáp án
- **Học tuần tự** — học theo bài, có nút *Trộn câu hỏi* để tránh học vẹt theo thứ tự
- **Ôn tập câu sai** — tự gom lại các câu từng trả lời sai
- **Đọc tài liệu** — xem trực tiếp 7 PDF bài giảng + đề ôn tập gốc ngay trong web
- **Giải thích + mẹo ghi nhớ** cho cả 210 câu — có nút 💡 trên thanh trên để bật/tắt:
  bật thì tự hiện sau khi trả lời, tắt thì ẩn hoàn toàn
- **Đánh dấu câu lệch so với tài liệu gốc** — những câu mà đáp án tô trong tài liệu sai (hoặc
  không có) đều mang nhãn riêng và một hộp ghi chú nói rõ tài liệu gốc tô đáp án nào, vì sao
  bộ đề này chấm khác. Xem `data/review_needed.md`
- 2 chế độ hiển thị: **Đơn giản** (thẻ từng câu) và **Đầy đủ** (dạng đề giấy)
- Giao diện sáng/tối, responsive cho điện thoại, lưu tiến trình bằng `localStorage`

## Phát triển tại máy
```bash
npm install
npm run dev       # server dev tại http://localhost:5173
```

## Build & xem thử bản production
```bash
npm run build     # xuất ra thư mục dist/
npm run preview   # xem thử bản đã build
```

## Deploy
Đã cấu hình **GitHub Actions** (`.github/workflows/deploy.yml`): mỗi lần push lên nhánh
`main` sẽ tự build và deploy lên GitHub Pages.

GitHub Pages đã được bật sẵn (Source = GitHub Actions), nên từ giờ chỉ cần `git push` là
site tự cập nhật: <https://thangvannguyen.github.io/yhct-sinh-hoc-di-chuyen-2026/>

## Dữ liệu câu hỏi

Bộ câu hỏi được sinh ra bằng hai bước, tách riêng để chạy lại parser không xoá mất phần
viết tay:

```bash
python3 data/parse_pdf.py        # PDF → data/questions.base.json  (thuần máy)
python3 data/build_questions.py  # base + overrides + explanations → data/questions.json
```

- `data/parse_pdf.py` — đọc `public/lectures/08-cau-hoi-on-tap-da-to-dap-an.pdf` bằng
  PyMuPDF. Đáp án đúng nằm ở **Highlight annotation** chứ không phải màu chữ, nên script
  đọc annotation và đối chiếu với toạ độ từng chữ. Script **tự kiểm tra và dừng** nếu số
  câu, số phương án hay số đáp án lệch khỏi mong đợi.
- `data/overrides.json` — chốt tay đáp án cho những câu tài liệu gốc không tô, tô hai đáp án,
  hoặc tô sai; kèm lý do hiện thẳng cho người học đọc. `build_questions.py` tự lấy đáp án gốc
  từ `questions.base.json` ghép vào ghi chú nên phần trích dẫn luôn khớp với file PDF.
- `data/explanations/bai1.json … bai7.json` — phần giải thích + mẹo ghi nhớ viết tay.
- `data/review_needed.md` — nhật ký rà soát: căn cứ của từng chỉnh sửa, các câu đề gốc có
  vấn đề, các câu in trùng phương án và các câu bị lặp.

Yêu cầu để chạy lại parser: `python3 -m pip install pymupdf`.

## Cấu trúc
- `src/` — mã nguồn React
  - `src/lib/` — dữ liệu, `localStorage`, context (theme / chế độ / phiên thi)
  - `src/components/` — thành phần dùng chung (Layout, câu hỏi, navigator…)
  - `src/pages/` — các trang (Home, Study, ReviewWrong, QuizSetup/Play/Result, Pdf)
- `data/` — script trích xuất + dữ liệu câu hỏi
- `public/lectures/` — 7 PDF bài giảng và đề ôn tập gốc

## Ghi chú
- Khóa `localStorage` dùng tiền tố `shdt_` (không phải `hs_` như web Hóa Sinh): hai site
  cùng chạy trên `thangvannguyen.github.io` nên dùng chung localStorage, trùng khóa là tiến
  trình hai môn đè lên nhau.
- Google Analytics (GA4) đã gắn trong `index.html`, Measurement ID `G-81QFZVV8W0`.
