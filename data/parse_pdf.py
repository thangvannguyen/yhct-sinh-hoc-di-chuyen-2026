#!/usr/bin/env python3
"""Trích bộ câu hỏi + đáp án từ PDF gốc ra data/questions.base.json.

Chạy:  python3 data/parse_pdf.py

Nguồn: public/lectures/08-cau-hoi-on-tap-da-to-dap-an.pdf

Đáp án đúng trong file gốc được đánh dấu bằng *Highlight annotation* (tô vàng), chứ
không phải bằng màu chữ — nên phải đọc annotation chứ không chỉ đọc text.

Layout của PDF rất đều:
  - dòng câu hỏi bắt đầu ở x ~ 58
  - 5 đáp án xếp lưới 3 cột (x ~ 76/87, ~256, ~433), hàng 1 = A B C, hàng 2 = D E

Script gom chữ theo *hàng ngang* (cùng toạ độ y) rồi tách đáp án theo marker A.–E.
Cách này xử lý được cả những câu mà cả 5 đáp án bị dồn vào chung một dòng text.

Output là dữ liệu thuần máy — KHÔNG chứa giải thích / mẹo ghi nhớ. Phần viết tay nằm ở
data/explanations.json và data/overrides.json, được trộn vào bởi data/build_questions.py.
"""

import json
import os
import re
import sys
from collections import defaultdict

import fitz  # PyMuPDF

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, 'public', 'lectures', '08-cau-hoi-on-tap-da-to-dap-an.pdf')
OUT = os.path.join(HERE, 'questions.base.json')

# Số câu mong đợi ở mỗi bài — dùng để tự kiểm tra, nếu lệch là parser sai.
EXPECTED_COUNTS = {1: 16, 2: 48, 3: 25, 4: 37, 5: 8, 6: 43, 7: 33}
EXPECTED_TOTAL = 210

# Các câu (theo số thứ tự gốc trong PDF) đã biết là không có đúng 1 highlight.
# Đáp án của chúng được chốt tay trong data/overrides.json.
KNOWN_ANSWER_EXCEPTIONS = {30, 86, 126, 160, 207}

BAI_RE = re.compile(r'^Bài\s*(\d+)\s*[:.]\s*(.+)$')
QUESTION_RE = re.compile(r'^(\d{1,3})\s*[.)]\s*(.*)$', re.DOTALL)
OPTION_RE = re.compile(r'^([A-E])\s*[.)]\s*(.*)$', re.DOTALL)

QUESTION_X_MAX = 70   # dòng câu hỏi nằm sát lề trái hơn mọi thứ khác
ROW_TOLERANCE = 5.0   # chênh lệch y tối đa để coi 2 chữ là cùng một hàng
LETTERS = 'ABCDE'
# Ranh giới 3 cột đáp án (cột 0 bắt đầu ~x76, cột 1 ~x256, cột 2 ~x433).
COLUMN_EDGES = (250.0, 420.0)


def column_of(x0):
    """Đáp án nằm ở cột nào (0, 1 hay 2)."""
    if x0 < COLUMN_EDGES[0]:
        return 0
    if x0 < COLUMN_EDGES[1]:
        return 1
    return 2


def quad_rects(annot):
    """Cắt vertices của annotation thành từng ô chữ nhật (mỗi dòng 1 quad).

    Dùng quad thay vì annot.rect: rect là hợp của mọi quad nên khi một highlight
    trải qua 2 dòng, nó phình ra và trùm cả sang cột đáp án bên cạnh.
    """
    verts = annot.vertices or []
    out = []
    for i in range(0, len(verts) - 3, 4):
        quad = verts[i:i + 4]
        xs = [p[0] for p in quad]
        ys = [p[1] for p in quad]
        out.append(fitz.Rect(min(xs), min(ys), max(xs), max(ys)))
    return out


def overlap_ratio(word_rect, rect):
    """Phần diện tích của word_rect bị rect phủ (0..1)."""
    inter = word_rect & rect
    if inter.is_empty:
        return 0.0
    area = word_rect.get_area()
    return inter.get_area() / area if area else 0.0


def collect_rows(doc):
    """Trả về danh sách hàng ngang, mỗi hàng là list chữ đã sắp theo x.

    Mỗi chữ là dict(text, x0, hl).
    """
    rows = []
    for pno, page in enumerate(doc):
        highlights = []
        freetext_rects = []
        for annot in (page.annots() or []):
            kind = annot.type[1]
            if kind == 'Highlight':
                highlights.extend(quad_rects(annot))
            elif kind == 'FreeText':
                # FreeText là chữ do người đọc viết thêm (ví dụ chữ "bỏ" ở trang 19)
                # và bị get_text() trộn vào nội dung đề — phải loại ra.
                # Annotation Ink thì KHÔNG loại: nó chỉ khoanh lên chữ có sẵn.
                freetext_rects.append(annot.rect)

        words = []
        for x0, y0, x1, y1, text, *_ in page.get_text('words'):
            if not text.strip():
                continue
            wrect = fitz.Rect(x0, y0, x1, y1)
            if any(overlap_ratio(wrect, r) > 0.5 for r in freetext_rects):
                continue
            hl = any(overlap_ratio(wrect, r) > 0.4 for r in highlights)
            words.append(dict(text=text, x0=x0, y0=y0, yc=(y0 + y1) / 2, hl=hl))

        # Gom theo hàng ngang: cùng y => cùng hàng, bất kể nằm ở cột nào.
        words.sort(key=lambda w: (w['yc'], w['x0']))
        current = []
        for w in words:
            if current and abs(w['yc'] - current[0]['yc']) > ROW_TOLERANCE:
                rows.append(sorted(current, key=lambda x: x['x0']))
                current = []
            current.append(w)
        if current:
            rows.append(sorted(current, key=lambda x: x['x0']))
    return rows


def parse(doc):
    rows = collect_rows(doc)

    chapters = []
    chapter = None
    question = None
    expected_letter_idx = 0  # chữ cái đáp án tiếp theo đang chờ
    problems = []

    def flush_question():
        nonlocal question
        if question is not None:
            chapter['questions'].append(question)
            question = None

    for row in rows:
        row_text = ' '.join(w['text'] for w in row).strip()
        if not row_text or row_text.startswith('CÂU HỎI ÔN TẬP'):
            continue

        m = BAI_RE.match(row_text)
        if m:
            flush_question()
            chapter = dict(num=int(m.group(1)), title=m.group(2).strip(), questions=[])
            chapters.append(chapter)
            continue

        first_x = row[0]['x0']
        m = QUESTION_RE.match(row_text)
        if m and first_x < QUESTION_X_MAX:
            if chapter is None:
                problems.append(f'câu {m.group(1)} xuất hiện trước khi có "Bài N"')
                continue
            flush_question()
            question = dict(num=int(m.group(1)), text=m.group(2).strip(), options=[])
            expected_letter_idx = 0
            continue

        if question is None:
            problems.append(f'dòng mồ côi (không thuộc câu nào): {row_text[:70]!r}')
            continue

        # Đi từ trái sang phải, mở đáp án mới khi gặp đúng chữ cái đang chờ.
        # Ràng buộc "đúng chữ cái tiếp theo" giúp tách được những dòng bị dồn
        # nhiều đáp án, mà không nhận nhầm nội dung kiểu "D. A, B và C đúng".
        open_in_row = None  # đáp án vừa được mở trong CHÍNH hàng này
        for w in row:
            m = OPTION_RE.match(w['text'])
            if (
                m
                and expected_letter_idx < len(LETTERS)
                and m.group(1) == LETTERS[expected_letter_idx]
                and w['x0'] >= QUESTION_X_MAX
            ):
                opt = dict(letter=m.group(1), words=[], hl=False,
                           col=column_of(w['x0']))
                question['options'].append(opt)
                open_in_row = opt
                expected_letter_idx += 1
                rest = m.group(2).strip()
                if rest:
                    opt['words'].append(rest)
                if w['hl']:
                    opt['hl'] = True
                continue

            if open_in_row is not None:
                # Chữ nằm sau một marker trong cùng hàng → thuộc đáp án đó, bất kể
                # nó trôi sang toạ độ x của cột bên cạnh (đáp án dài ở lưới 2 cột).
                target = open_in_row
            elif question['options']:
                # Hàng không có marker = chữ xuống dòng. Nó thuộc đáp án gần nhất
                # *cùng cột*, không phải đáp án mở sau cùng — vì với lưới nhiều cột
                # thì đáp án mở sau cùng thường ở cột khác (vd chữ "chiều" của đáp
                # án A câu 11 nằm dưới cột 0, trong khi đáp án vừa đọc là C ở cột 2).
                col = column_of(w['x0'])
                target = next(
                    (o for o in reversed(question['options']) if o['col'] == col),
                    question['options'][-1],
                )
            else:
                # Dòng tiếp nối của phần đề bài (câu hỏi dài, xuống dòng).
                question['text'] += ' ' + w['text']
                continue

            target['words'].append(w['text'])
            if w['hl']:
                target['hl'] = True

    flush_question()

    # ---- hậu xử lý: nối chữ thành câu, chọn đáp án ----
    for ch in chapters:
        for q in ch['questions']:
            opts = []
            correct = None
            for o in q['options']:
                text = re.sub(r'\s+', ' ', ' '.join(o['words'])).strip()
                full = f"{o['letter']}. {text}"
                opts.append(full)
                if o['hl']:
                    correct = full if correct is None else correct
            q['n_highlighted'] = sum(1 for o in q['options'] if o['hl'])
            q['options'] = opts
            q['correct'] = correct if q['n_highlighted'] == 1 else None
            q['text'] = re.sub(r'\s+', ' ', q['text']).strip()

    return chapters, problems


def validate(chapters, problems):
    """In báo cáo, trả về True nếu dữ liệu đạt yêu cầu."""
    ok = True
    total = 0
    print(f'{len(chapters)} bài\n')
    for ch in chapters:
        n = len(ch['questions'])
        total += n
        bad_opts = [
            (q['num'], len(q['options']))
            for q in ch['questions']
            if len(q['options']) != 5
        ]
        no_answer = [q['num'] for q in ch['questions'] if q['n_highlighted'] == 0]
        multi = [q['num'] for q in ch['questions'] if q['n_highlighted'] > 1]
        expected = EXPECTED_COUNTS.get(ch['num'])
        mark = '✓' if n == expected else '✗'
        if n != expected:
            ok = False
        print(f"  {mark} Bài {ch['num']}: {ch['title'][:46]:<46} {n:>3} câu "
              f"(mong đợi {expected})")
        if bad_opts:
            ok = False
            print(f"      ✗ số đáp án ≠ 5: {bad_opts}")
        if no_answer:
            print(f"      · chưa tô đáp án: {no_answer}")
        if multi:
            print(f"      · tô nhiều đáp án: {multi}")

    print(f'\nTổng: {total} câu (mong đợi {EXPECTED_TOTAL})')
    if total != EXPECTED_TOTAL:
        ok = False
        print('  ✗ tổng số câu không khớp')

    nums = [q['num'] for ch in chapters for q in ch['questions']]
    missing = [i for i in range(1, EXPECTED_TOTAL + 1) if i not in nums]
    dups = sorted({n for n in nums if nums.count(n) > 1})
    if missing or dups:
        ok = False
        print(f'  ✗ thiếu số câu: {missing} · trùng: {dups}')
    elif nums != sorted(nums):
        ok = False
        print('  ✗ số câu không tăng dần')
    else:
        print('  ✓ số thứ tự liên tục 1..210, không trùng không thiếu')

    exceptions = {
        q['num']
        for ch in chapters
        for q in ch['questions']
        if q['n_highlighted'] != 1
    }
    graded = EXPECTED_TOTAL - len(exceptions)
    print(f'  {graded} câu có đúng 1 đáp án được tô')
    unexpected = exceptions - KNOWN_ANSWER_EXCEPTIONS
    resolved = KNOWN_ANSWER_EXCEPTIONS - exceptions
    if unexpected:
        ok = False
        print(f'  ✗ ngoại lệ đáp án ngoài dự kiến: {sorted(unexpected)}')
    if resolved:
        print(f'  · ngoại lệ đã biết nhưng giờ hết lệch (xem lại overrides): '
              f'{sorted(resolved)}')
    if exceptions & KNOWN_ANSWER_EXCEPTIONS:
        print(f'  · ngoại lệ đã biết, chốt tay ở overrides.json: '
              f'{sorted(exceptions & KNOWN_ANSWER_EXCEPTIONS)}')

    if problems:
        ok = False
        print(f'\n✗ {len(problems)} dòng không phân loại được:')
        for p in problems[:20]:
            print('   ', p)

    return ok


def main():
    doc = fitz.open(SRC)
    chapters, problems = parse(doc)
    ok = validate(chapters, problems)

    out = dict(chapters=[
        dict(
            num=ch['num'],
            title=ch['title'],
            questions=[
                dict(num=q['num'], text=q['text'], options=q['options'],
                     correct=q['correct'])
                for q in ch['questions']
            ],
        )
        for ch in chapters
    ])
    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(f'\n→ {os.path.relpath(OUT, ROOT)}')

    if not ok:
        print('\n✗ Dữ liệu CHƯA đạt — sửa parser trước khi build.')
        sys.exit(1)
    print('✓ Dữ liệu đạt yêu cầu.')


if __name__ == '__main__':
    main()
