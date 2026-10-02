# Nhật ký rà soát bộ câu hỏi

Nguồn: `public/lectures/08-cau-hoi-on-tap-da-to-dap-an.pdf` (19 trang, 210 câu, đáp án
đúng được tô vàng bằng Highlight annotation).

**Kết quả trích xuất:** 7 bài · 210 câu · số thứ tự liên tục 1–210, không trùng không
thiếu · 205 câu có đúng một đáp án được tô · 5 câu phải xử lý tay (xem bên dưới).

**Đã đối chiếu bằng mắt** 24 câu trên ba trang bất kỳ (trang 10 — câu 115–124, trang 17 —
câu 186–199, trang 3 — câu 27–41) cùng toàn bộ 10 câu đặc biệt liệt kê dưới đây: 100% khớp
với kết quả của `parse_pdf.py`.

---

## 1. Năm câu phải chốt đáp án bằng tay

Các chỉnh sửa này nằm ở `data/overrides.json`.

| Câu | Vấn đề trong đề gốc | Xử lý | Căn cứ |
|-----|---------------------|-------|--------|
| **30** | Tô vàng CẢ HAI đáp án A (*Màng tế bào*) và D (*Màng sinh chất*) | Chốt **A**, phần giải thích nói rõ D cũng đúng | Hai phương án là hai tên gọi của cùng một cấu trúc. Câu 31 ngay sau là bản lặp của câu này, đáp án là *Màng sinh chất* |
| **86** | Không tô đáp án nào | Chốt **B** — *Tế bào chất, không phụ thuộc oxy* | Slide bài 3 (*Quá trình đường phân*): "Là giai đoạn chung, không phụ thuộc oxy — Xảy ra ở bào tương" |
| **126** | Không tô đáp án nào | Chốt **B** — *…cao phân tử, …quá trình cơ bản của sự sống* | Slide bài 4 không có câu định nghĩa này. Chắc chắn loại được C, D, E vì acid nucleic là polymer ("cao phân tử"). Giữa A và B chỉ khác một từ (*phức tạp* / *cơ bản*); chọn B theo cách diễn đạt chuẩn của giáo trình. **Đây là câu còn độ chắc chắn thấp nhất** |
| **160** | Không tô đáp án nào | Chốt **D — 3** | Giải tay và kiểm tra lại bằng chương trình: chỉ 3 phép lai I, II, IV thoả "hoa hồng **thuần chủng** × hoa đỏ → F1 50% đỏ : 50% hồng". III cho 100% đỏ; V (*aaBb*) và VI (*Aabb*) có cây hoa hồng **không** thuần chủng |
| **207** | Không tô đáp án + có ghi chú viết tay **"bỏ"** (FreeText annotation) và vệt mực ở lề | Đánh dấu `flag: "dropped"` — hiện ở chế độ Học kèm cảnh báo, **không** vào bài kiểm tra | Theo slide bài 7, phôi mới thành lập chỉ có ba vùng (trước = đầu, giữa = bụng/lưng có rãnh thần kinh, sau = đuôi). Cả D (*vùng cuối là phần chân*) lẫn E (*vùng giữa là nơi hình thành tay*) đều sai → câu có hai đáp án |

## 2. Lỗi gõ trong đề gốc, đã sửa

| Câu | Đề gốc | Đã sửa thành |
|-----|--------|--------------|
| **168** | `E. A. B, C và D đúng` | `E. A, B, C và D đúng` (dấu chấm → dấu phẩy, không đổi nghĩa) |

## 3. Câu có vấn đề về nội dung — GIỮ NGUYÊN đáp án của đề, đã ghi chú trong phần giải thích

Những câu này đáp án tô vàng mâu thuẫn với kiến thức chuẩn hoặc với phép tính. Web vẫn chấm
theo **đáp án của đề** (để khớp với đáp án chính thức khi đi thi), nhưng phần *Giải thích*
nói rõ chỗ vênh để người học không bị học sai bản chất.

| Câu | Đáp án đề | Vấn đề |
|-----|-----------|--------|
| **87** | B — *Gây chảy máu cơ, mõi cơ* | Về sinh lý, hậu quả của lên men lactic là ứ acid lactic gây **mỏi cơ, đau cơ**; phương án A (*gây đau cơ, mỏi cơ*) nghe hợp lý hơn. Đã kiểm tra lại ảnh trang 8: đề đúng là tô B |
| **162** | B — *8 loại kiểu hình : 12 loại kiểu gen* | Tính ra: `Aa×aa` → 2 kiểu hình; `BB×Bb` → **1** kiểu hình; `Dd×Dd` → 2 kiểu hình ⇒ **4** kiểu hình : 12 kiểu gen, tức phương án **A** mới đúng. Nhiều khả năng đáp án của đề sai. Đã kiểm tra lại ảnh trang 14: đề đúng là tô B |
| **111** | A — *Nucleotid* | Nhiều tài liệu lấy **nucleosom** (phương án E) làm "đơn vị cơ bản cấu tạo NST". Đề này hiểu "cơ bản" theo nghĩa đơn vị hóa học nên chọn nucleotid. Đã kiểm tra lại ảnh trang 9 |
| **176** | D — *Vận chuyển các chất hoà tan, phân tử nhỏ* | Hai phương án A (*cần tiêu tốn năng lượng*) và C (*màng tạo túi*) cũng đúng với ẩm/thực bào, nên đề diễn đạt chưa chặt. D là đặc điểm riêng của ẩm bào. Đã kiểm tra lại ảnh trang 16 |
| **159** | A — *2* | **Đề gốc bị mất danh sách các phép lai**: câu hỏi ghi "có bao nhiêu phép lai sau đây…" nhưng không có phép lai nào được liệt kê, nhảy thẳng xuống các phương án số. Không thể tự giải lại; giữ đáp án của đề. Đã kiểm tra lại ảnh trang 13 |

## 4. Đề gốc in trùng phương án (không ảnh hưởng đáp án)

Những câu dưới đây có hai phương án giống hệt nhau trong đề gốc — giữ nguyên để trung thành
với bản in:

- **Câu 92**: A và C cùng là *Adenin TriPhosphat*
- **Câu 119**: A và D cùng là *Vận chuyển acid amin*
- **Câu 121**: A và E cùng là *Kì giữa, kì sau*
- **Câu 152**: C và E cùng là *16*

## 5. Câu lặp lại trong đề (giữ nguyên cả hai)

Đề gốc có một số câu hỏi xuất hiện hai lần, đôi khi với bộ phương án hơi khác:

- Câu **28** và **34** — *Bào quan cần cho phân bào* (cùng đáp án: Trung thể)
- Câu **30** và **31** — *Cấu trúc đảm nhận trao đổi chất với môi trường*
- Câu **68** và **76** — *Chuỗi truyền điện tử xảy ra ở đâu*
- Câu **74** và **75** — *Chất nhận điện tử cuối cùng*
- Câu **90** và **108** — *Đường kính sợi cơ bản*
- Câu **107** và **110** — *Sợi nhiễm sắc / mức xoắn 30 nm*
- Câu **137** và **139** — *AA và Aa cùng kiểu hình khi nào*
- Câu **192** và **210** — *Hoạt hóa trứng xảy ra khi nào*
- Câu **66** (bài 3) và **92** (bài 4) — *ATP là viết tắt của*

---

## Cách chạy lại

```bash
python3 data/parse_pdf.py        # PDF → data/questions.base.json (có tự kiểm tra)
python3 data/build_questions.py  # base + overrides + explanations → data/questions.json
```

`parse_pdf.py` sẽ **báo lỗi và dừng** nếu số câu mỗi bài lệch khỏi 16/48/25/37/8/43/33, nếu
có câu không đủ 5 phương án, hoặc nếu xuất hiện câu lệch đáp án ngoài 5 câu đã biết ở mục 1.
