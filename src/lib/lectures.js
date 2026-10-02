// Tài liệu PDF, phục vụ tĩnh từ public/lectures/.
// `title` giữ đúng tên bài trong file gốc; tên file đã được đổi sang không dấu.
export const LECTURES = [
  {
    id: 'bai-1',
    title: 'Bài 1 — Sinh học, khoa học của sự sống',
    file: '01-sinh-hoc-khoa-hoc-cua-su-song.pdf',
    icon: '🔬',
    pages: 27,
  },
  {
    id: 'bai-2',
    title: 'Bài 2 — Sinh học tế bào',
    file: '02-sinh-hoc-te-bao.pdf',
    icon: '🧫',
    pages: 90,
  },
  {
    id: 'bai-3',
    title: 'Bài 3 — Năng lượng sinh học',
    file: '03-nang-luong-sinh-hoc.pdf',
    icon: '⚡',
    pages: 43,
  },
  {
    id: 'bai-4',
    title: 'Bài 4 — Cơ sở phân tử của di truyền học',
    file: '04-co-so-phan-tu-cua-di-truyen-hoc.pdf',
    icon: '🧬',
    pages: 79,
  },
  {
    id: 'bai-5',
    title: 'Bài 5 — Sự phân chia tế bào',
    file: '05-su-phan-chia-te-bao.pdf',
    icon: '🔄',
    pages: 46,
  },
  {
    id: 'bai-6',
    title: 'Bài 6 — Các quy luật di truyền',
    file: '06-cac-quy-luat-di-truyen.pdf',
    icon: '🫛',
    pages: 87,
  },
  {
    id: 'bai-7',
    title: 'Bài 7 — Sự phát sinh giao tử, thụ tinh và phát triển của phôi ở người',
    file: '07-phat-sinh-giao-tu-thu-tinh-phoi.pdf',
    icon: '👶',
    pages: 103,
  },
  {
    id: 'de-goc',
    title: 'Đề ôn tập gốc (đáp án tô vàng)',
    file: '08-cau-hoi-on-tap-da-to-dap-an.pdf',
    icon: '📝',
    pages: 19,
  },
]

export function lectureById(id) {
  return LECTURES.find((l) => l.id === id)
}

export function lectureUrl(lecture) {
  return import.meta.env.BASE_URL + 'lectures/' + lecture.file
}
