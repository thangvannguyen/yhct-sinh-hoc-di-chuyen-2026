#!/usr/bin/env python3
"""Trộn dữ liệu máy + phần viết tay thành data/questions.json (file web dùng).

Chạy:  python3 data/build_questions.py

    questions.base.json   ← máy trích từ PDF (data/parse_pdf.py), đừng sửa tay
  + overrides.json        ← chốt tay đáp án / sửa lỗi gõ
  + explanations/bai*.json← giải thích + mẹo ghi nhớ
  = questions.json        ← src/lib/data.js import file này

Tách làm nhiều file để chạy lại parser không xoá mất phần viết tay.
"""

import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BASE = os.path.join(HERE, 'questions.base.json')
OVERRIDES = os.path.join(HERE, 'overrides.json')
EXPLAIN_DIR = os.path.join(HERE, 'explanations')
OUT = os.path.join(HERE, 'questions.json')

LETTERS = 'ABCDE'

# Tên hiển thị + icon của từng bài. `title` dùng ở tiêu đề trang dạng đề giấy,
# `short` dùng ở tab / chip / danh sách (tiêu đề bài 7 quá dài nên phải rút gọn).
CHAPTER_META = {
    1: dict(title='Sinh học, khoa học của sự sống', short='Sinh học & sự sống', icon='🔬'),
    2: dict(title='Sinh học tế bào', short='Sinh học tế bào', icon='🧫'),
    3: dict(title='Năng lượng sinh học', short='Năng lượng sinh học', icon='⚡'),
    4: dict(title='Cơ sở phân tử của di truyền học', short='Cơ sở phân tử', icon='🧬'),
    5: dict(title='Sự phân chia tế bào', short='Phân chia tế bào', icon='🔄'),
    6: dict(title='Các quy luật di truyền', short='Quy luật di truyền', icon='🫛'),
    7: dict(title='Sự phát sinh giao tử, thụ tinh và phát triển của phôi ở người',
            short='Giao tử & phôi thai', icon='👶'),
}


def load_json(path, default=None):
    if not os.path.exists(path):
        return default
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def main():
    base = load_json(BASE)
    if base is None:
        sys.exit('✗ Chưa có questions.base.json — chạy data/parse_pdf.py trước.')
    overrides = {k: v for k, v in (load_json(OVERRIDES, {}) or {}).items()
                 if not k.startswith('_')}

    explanations = {}
    for path in sorted(glob.glob(os.path.join(EXPLAIN_DIR, 'bai*.json'))):
        for qid, entry in (load_json(path, {}) or {}).items():
            if qid.startswith('_'):
                continue
            explanations[qid] = entry

    chapters = []
    used_overrides = set()
    missing_explain = []
    problems = []

    for ch in base['chapters']:
        meta = CHAPTER_META[ch['num']]
        questions = []
        for q in ch['questions']:
            qid = f"bai-{ch['num']}-{q['num']}"
            options = list(q['options'])
            text = q['text']
            correct = q['correct']
            flag = None

            ov = overrides.get(qid)
            if ov:
                used_overrides.add(qid)
                for idx, value in (ov.get('options') or {}).items():
                    options[int(idx)] = value
                if 'text' in ov:
                    text = ov['text']
                if 'correct' in ov:
                    letter = ov['correct']
                    if letter is None:
                        correct = None
                    elif letter in LETTERS:
                        correct = options[LETTERS.index(letter)]
                    else:
                        problems.append(f'{qid}: correct "{letter}" không phải A–E')
                elif correct is not None:
                    # Đáp án cũ có thể trỏ vào nội dung đã bị override sửa lại.
                    correct = options[q['options'].index(correct)]
                flag = ov.get('flag')

            if correct is not None and correct not in options:
                problems.append(f'{qid}: đáp án không nằm trong danh sách lựa chọn')

            ex = explanations.get(qid) or {}
            if not ex.get('explain'):
                missing_explain.append(qid)

            questions.append(dict(
                id=qid,
                text=text,
                options=options,
                correct=correct,
                explain=ex.get('explain'),
                tip=ex.get('tip'),
                image=ex.get('image'),
                flag=flag,
            ))

        chapters.append(dict(
            id=f"bai-{ch['num']}",
            num=ch['num'],
            title=meta['title'],
            short=meta['short'],
            icon=meta['icon'],
            questions=questions,
        ))

    stale = set(overrides) - used_overrides
    if stale:
        problems.append(f'override trỏ vào câu không tồn tại: {sorted(stale)}')

    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(dict(chapters=chapters), f, ensure_ascii=False, indent=1)

    total = sum(len(c['questions']) for c in chapters)
    graded = sum(1 for c in chapters for q in c['questions'] if q['correct'])
    with_explain = total - len(missing_explain)
    print(f"{len(chapters)} bài · {total} câu")
    print(f"  {graded} câu chấm điểm được, {total - graded} câu không chấm điểm")
    print(f"  {with_explain}/{total} câu đã có giải thích")
    if missing_explain:
        by_chapter = {}
        for qid in missing_explain:
            by_chapter.setdefault(qid.rsplit('-', 1)[0], []).append(qid)
        for key in sorted(by_chapter, key=lambda k: int(k.split('-')[1])):
            print(f"    · thiếu giải thích {key}: {len(by_chapter[key])} câu")
    print(f"→ {os.path.relpath(OUT, ROOT)}")

    if problems:
        print('\n✗ Lỗi:')
        for p in problems:
            print('   ', p)
        sys.exit(1)


if __name__ == '__main__':
    main()
