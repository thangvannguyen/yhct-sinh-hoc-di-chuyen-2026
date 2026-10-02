# Nhật ký rà soát bộ câu hỏi

Nguồn: `public/lectures/08-cau-hoi-on-tap-da-to-dap-an.pdf` (19 trang, 210 câu, đáp án
đúng được tô vàng bằng Highlight annotation).

**Kết quả trích xuất:** 7 bài · 210 câu · số thứ tự liên tục 1–210, không trùng không
thiếu · 205 câu có đúng một đáp án được tô.

**Tổng kết chỉnh sửa:** 3 câu sửa đáp án khác tài liệu gốc · 3 câu tài liệu gốc không tô
đáp án · 1 câu tô hai đáp án · 1 câu đề gốc đánh dấu bỏ · 1 lỗi gõ.

**Đã đối chiếu bằng mắt** 24 câu trên ba trang bất kỳ (trang 10 — câu 115–124, trang 17 —
câu 186–199, trang 3 — câu 27–41) cùng tất cả các câu được nhắc tới trong tài liệu này:
100% khớp với kết quả của `parse_pdf.py`, tức mọi chỗ lệch dưới đây là lỗi của tài liệu gốc
chứ không phải lỗi đọc file.

---

## 1. Nguyên tắc chấm điểm

Khi đáp án tô trong tài liệu gốc **sai so với kiến thức hoặc phép tính**, bộ đề này chấm theo
**đáp án đúng thật sự**, đồng thời hiện một hộp ghi chú ngay dưới câu hỏi nói rõ tài liệu gốc
tô đáp án nào — để người học biết chính xác câu nào mình đang trả lời khác với tài liệu.

Trong web, mỗi câu như vậy mang một nhãn nhỏ hiện ngay từ trước khi trả lời:

| Nhãn | Nghĩa |
|------|-------|
| `≠ đáp án gốc` | đáp án đã sửa, khác với đáp án tô trong tài liệu |
| `đáp án bổ sung` | tài liệu gốc không tô đáp án nào, đáp án do tra cứu mà chốt |
| `gốc tô 2 đáp án` | tài liệu gốc tô nhiều hơn một đáp án |

Nội dung "tài liệu gốc tô …" trong hộp ghi chú được `build_questions.py` lấy thẳng từ
`questions.base.json`, nên luôn khớp với file PDF, không sợ chép sai.

## 2. Ba câu đã SỬA đáp án khác tài liệu gốc

| Câu | Tài liệu gốc tô | Đã sửa thành | Căn cứ |
|-----|-----------------|--------------|--------|
| **87** | B. *Gây chảy máu cơ, mõi cơ* | **A. *Gây đau cơ, mõi cơ*** | Lên men lactic làm ứ acid lactic → giảm pH trong cơ → mỏi cơ, đau cơ. "Chảy máu cơ" không phải hậu quả của lên men. Nhiều khả năng bút tô trượt sang cột bên cạnh |
| **111** | A. *Nucleotid* | **E. *Nucleosom*** | Đơn vị cấu trúc cơ bản của NST nhân chuẩn là nucleosom (146 cặp base quấn 7/4 vòng quanh 8 histon). Chữ "ở tế bào nhân chuẩn" trong đề chính là dấu hiệu: nucleotid là đơn vị của mọi DNA kể cả DNA vòng trần của vi khuẩn |
| **162** | B. *8 loại kiểu hình : 12 loại kiểu gen* | **A. *4 loại kiểu hình : 12 loại kiểu gen*** | `Aa × aa` → 2 kiểu hình; `BB × Bb` → đời con toàn B- nên **1** kiểu hình; `Dd × Dd` → 2 kiểu hình ⇒ 2 × 1 × 2 = **4** kiểu hình (số kiểu gen 12 thì đề ghi đúng) |

Cả ba đều đã mở ảnh trang PDF gốc đọc tận mắt để chắc chắn không phải parser đọc nhầm
(trang 8, trang 9, trang 14).

## 3. Bốn câu tài liệu gốc không tô / tô nhiều đáp án

| Câu | Vấn đề | Đã chốt | Căn cứ |
|-----|--------|---------|--------|
| **30** | Tô CẢ HAI đáp án A (*Màng tế bào*) và D (*Màng sinh chất*) | **A** | Hai phương án là hai tên gọi của cùng một cấu trúc nên đều đúng; chấm theo phương án đứng trước. Câu 31 ngay sau là bản lặp, đáp án là *Màng sinh chất* |
| **86** | Không tô đáp án nào | **B** — *Tế bào chất, không phụ thuộc oxy* | Slide bài 3: "Quá trình đường phân: là giai đoạn chung, không phụ thuộc oxy — Xảy ra ở bào tương" |
| **126** | Không tô đáp án nào | **B** — *…cao phân tử, …quá trình cơ bản của sự sống* | Slide bài 4 không có câu định nghĩa này. Chắc chắn loại được C, D, E vì acid nucleic là polymer. Giữa A và B chỉ khác một từ; chọn B theo cách diễn đạt chuẩn của giáo trình. **Đây là câu còn độ chắc chắn thấp nhất** |
| **160** | Không tô đáp án nào | **D — 3** | Giải tay và kiểm tra lại bằng chương trình: chỉ 3 phép lai I, II, IV thoả "hoa hồng **thuần chủng** × hoa đỏ → F1 50% đỏ : 50% hồng". III cho 100% đỏ; V (*aaBb*) và VI (*Aabb*) có cây hoa hồng **không** thuần chủng |

## 4. Một câu đề gốc đã bỏ

**Câu 207** không tô đáp án và có ghi chú viết tay **"bỏ"** (FreeText annotation) kèm vệt mực
ở lề. Đã đánh dấu `flag: "dropped"`: vẫn xem được ở chế độ Học kèm cảnh báo, nhưng **không**
vào bài kiểm tra. Lý do đề bỏ: theo slide bài 7 phôi mới thành lập chỉ có ba vùng (trước =
đầu, giữa = bụng/lưng có rãnh thần kinh, sau = đuôi), nên cả D (*vùng cuối là phần chân*) lẫn
E (*vùng giữa là nơi hình thành tay*) đều sai → câu có hai đáp án.

## 5. Lỗi gõ trong đề gốc, đã sửa

| Câu | Đề gốc | Đã sửa thành |
|-----|--------|--------------|
| **168** | `E. A. B, C và D đúng` | `E. A, B, C và D đúng` (dấu chấm → dấu phẩy, không đổi nghĩa, không đổi đáp án) |

## 6. Câu đề ra chưa chặt — GIỮ NGUYÊN đáp án của đề

Những câu này đáp án của đề không sai, nhưng câu hỏi có nhiều hơn một phương án đúng hoặc
thiếu dữ kiện. Giữ nguyên đáp án gốc và đã ghi chú trong phần *Giải thích*.

| Câu | Đáp án đề | Vấn đề |
|-----|-----------|--------|
| **176** | D — *Vận chuyển các chất hoà tan, phân tử nhỏ* | Hai phương án A (*cần tiêu tốn năng lượng*) và C (*màng tạo túi*) cũng đúng với ẩm/thực bào. D là đặc điểm riêng của ẩm bào nên vẫn là phương án hợp lý nhất |
| **159** | A — *2* | **Đề gốc bị mất danh sách các phép lai**: câu hỏi ghi "có bao nhiêu phép lai sau đây…" nhưng không liệt kê phép lai nào, nhảy thẳng xuống các phương án số. Không thể tự giải lại nên giữ đáp án của đề |
| **106** | C — *Cấu trúc bậc IV* | Câu dẫn có vế "biểu thị thứ tự sắp xếp các acid amin… và vị trí của liên kết disulfide" — đúng là định nghĩa chuẩn của **cấu trúc bậc I**; bậc IV nói về cách lắp ghép các tiểu đơn vị trong không gian. Nhưng slide bài 4 lại mô tả bậc 4 là "nhiều hơn 1 chuỗi polypeptid" được bình ổn bằng "liên kết disulfide", nên đáp án của đề có cơ sở trong chính bài giảng. **Giữ đáp án của đề, đã ghi chú trong phần Giải thích để người học hỏi lại giảng viên** |
| **10** | C — *Sự sống* | Phương án E (*Sinh trưởng*) cũng không nằm trong ba tính chất đặc trưng theo slide; tuy nhiên "sự sống" là phương án lạc loài rõ ràng nhất |

## 7. Đã kiểm tra lại toàn bộ câu tính toán

Mười lăm câu tính toán của bài 6 (140, 141, 142, 143, 146, 149, 150, 151, 152, 153, 154, 156,
162, 164, 165) đã được **giải lại bằng chương trình** (liệt kê giao tử, lai, đếm kiểu gen và
kiểu hình bằng phân số chính xác). Kết quả: **chỉ câu 162 lệch**, 14 câu còn lại khớp đúng
đáp án của đề.

## 8. Đề gốc in trùng phương án (không ảnh hưởng đáp án)

Những câu dưới đây có hai phương án giống hệt nhau trong đề gốc — giữ nguyên để trung thành
với bản in:

- **Câu 92**: A và C cùng là *Adenin TriPhosphat*
- **Câu 119**: A và D cùng là *Vận chuyển acid amin*
- **Câu 121**: A và E cùng là *Kì giữa, kì sau*
- **Câu 152**: C và E cùng là *16*

## 9. Câu lặp lại trong đề (giữ nguyên cả hai)

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
có câu không đủ 5 phương án, hoặc nếu xuất hiện câu không-đúng-một-đáp-án ngoài 5 câu đã biết
(30, 86, 126, 160, 207 — xem mục 3 và 4).

`build_questions.py` cũng tự kiểm tra tính nhất quán của `overrides.json`: báo lỗi nếu khai
`noteKind: "corrected"` mà đáp án không hề đổi, hoặc khai `"missing"` / `"ambiguous"` mà tài
liệu gốc thật ra có tô đáp án. Nhờ vậy ghi chú hiện cho người học không bao giờ nói sai về
tài liệu gốc.
