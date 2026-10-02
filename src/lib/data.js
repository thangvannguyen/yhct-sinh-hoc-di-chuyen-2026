import rawData from '../../data/questions.json'

// ---- source data -----------------------------------------------------------
export const CHAPTERS = (rawData && rawData.chapters) || []

/** id -> { question, chapterId, chapterTitle, chapterShort } */
export const QUESTION_INDEX = {}
/** chapterId -> [questionId] in source order */
export const CHAPTER_QUESTIONS = {}
/** every question id in source order */
export const ALL_IDS = []

CHAPTERS.forEach((ch) => {
  CHAPTER_QUESTIONS[ch.id] = []
  ch.questions.forEach((q) => {
    // Data stores the answer as the exact option text in `correct`; derive the
    // numeric index the UI works with.
    const idx =
      q.correct === null || q.correct === undefined ? -1 : q.options.indexOf(q.correct)
    q.correctIndex = idx === -1 ? null : idx
    QUESTION_INDEX[q.id] = {
      question: q,
      chapterId: ch.id,
      chapterTitle: ch.title,
      chapterShort: ch.short,
    }
    CHAPTER_QUESTIONS[ch.id].push(q.id)
    ALL_IDS.push(q.id)
  })
})

export const TOTAL_QUESTIONS = ALL_IDS.length

// ---- helpers ----------------------------------------------------------------
export function chapterById(id) {
  return CHAPTERS.find((c) => c.id === id)
}

/** Tên đầy đủ của bài — dùng ở tiêu đề trang dạng đề giấy. */
export function chapterTitleOf(id) {
  return (chapterById(id) || {}).title || ''
}

/** Tên rút gọn — dùng ở tab, chip, nhãn chương (tên bài 7 quá dài). */
export function chapterShortOf(id) {
  const ch = chapterById(id)
  return ch ? ch.short || ch.title : ''
}

export function chapterIcon(id) {
  return (chapterById(id) || {}).icon || '📘'
}

/** Câu bị đề gốc đánh dấu "bỏ" — chỉ xem tham khảo, không chấm điểm. */
export function isDropped(q) {
  return q.flag === 'dropped'
}

export function isGraded(q) {
  return q.correctIndex !== null && q.correctIndex !== undefined
}

/** Only questions with a confirmed answer are eligible for graded quizzes. */
export function getEligibleIds(chapterIds) {
  const ids = []
  chapterIds.forEach((cid) => {
    ;(CHAPTER_QUESTIONS[cid] || []).forEach((id) => {
      if (isGraded(QUESTION_INDEX[id].question)) ids.push(id)
    })
  })
  return ids
}

export function letterFor(i) {
  return String.fromCharCode(65 + i)
}

// Options carry their original "A. ", "B. " ... prefix so the answer key can
// reference full option text. The UI derives its own letter from display
// position (which changes after shuffling), so strip the source prefix.
export function optionLabel(opt) {
  return String(opt).replace(/^[A-Za-z]\.\s*/, '')
}

export function shuffle(arr) {
  const a = arr.slice()
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[a[i], a[j]] = [a[j], a[i]]
  }
  return a
}

// Question images are either "images/xx.png" (served from public/) or a full
// external URL (kept as-is).
export function imageSrc(image) {
  if (!image) return null
  if (/^https?:\/\//i.test(image)) return image
  return import.meta.env.BASE_URL + image.replace(/^\.?\/?/, '')
}
