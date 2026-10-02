import { useParams } from 'react-router-dom'
import { BackLink, Button, Container } from '../components/ui.jsx'
import { LECTURES, lectureById, lectureUrl } from '../lib/lectures.js'

// Safari trên iOS và Chrome trên Android không nhúng được PDF: thẻ <object> chỉ cho
// ra một ô trắng rỗng. Trên các máy đó phải mời người dùng mở bằng trình xem của
// hệ điều hành thay vì bày ra một khung trống.
//
// Hỏi thẳng trình duyệt qua `pdfViewerEnabled` thay vì đoán theo user-agent: iPadOS
// khai báo user-agent giống hệt máy Mac nên cách đoán sẽ nhận nhầm. Chuỗi user-agent
// chỉ dùng làm phương án dự phòng cho trình duyệt cũ chưa có thuộc tính này.
function canEmbedPdf() {
  if (typeof navigator === 'undefined') return true
  if (typeof navigator.pdfViewerEnabled === 'boolean') return navigator.pdfViewerEnabled
  return !/Android|iPhone|iPad|iPod/i.test(navigator.userAgent || '')
}
const CAN_EMBED_PDF = canEmbedPdf()

function PdfList() {
  return (
    <Container>
      <BackLink to="/" />
      <h1 className="mb-1 text-[1.25rem] font-extrabold">📕 Tài liệu Sinh Học Di Truyền</h1>
      <p className="mb-4 text-[0.85rem] text-text-muted">
        {CAN_EMBED_PDF
          ? 'Chọn một mục để xem trực tiếp trong web, hoặc tải file về máy'
          : 'Chọn một mục để mở bằng trình đọc PDF của điện thoại, hoặc tải về máy'}
      </p>
      <div className="flex flex-col gap-2">
        {LECTURES.map((lec) => (
          <Button
            key={lec.id}
            to={`/pdf/${lec.id}`}
            className="!justify-start gap-3 px-3 py-3 text-left sm:gap-[15px] sm:px-3.5"
          >
            <span className="flex h-[42px] w-[42px] flex-shrink-0 items-center justify-center rounded-[12px] border border-border text-[1.35rem]" style={{ background: 'linear-gradient(135deg, var(--primary-soft), color-mix(in srgb, var(--primary-soft) 55%, var(--surface)))' }}>
              {lec.icon}
            </span>
            <span className="min-w-0 flex-1">
              <span className="block text-[0.92rem] font-semibold leading-snug">{lec.title}</span>
              <span className="block text-[0.78rem] font-normal text-text-muted">
                {lec.pages} trang
              </span>
            </span>
            <span className="text-[1.1rem] text-text-muted">›</span>
          </Button>
        ))}
      </div>
    </Container>
  )
}

/** Thẻ mời mở tài liệu — dùng cho máy không nhúng được PDF. */
function OpenPdfCard({ lecture, url }) {
  return (
    <div className="rounded-card border border-border bg-surface p-6 text-center shadow-soft">
      <div
        className="mx-auto mb-3 flex h-[64px] w-[64px] items-center justify-center rounded-[18px] border border-border text-[2rem]"
        style={{ background: 'linear-gradient(135deg, var(--primary-soft), color-mix(in srgb, var(--primary-soft) 55%, var(--surface)))' }}
      >
        {lecture.icon}
      </div>
      <p className="m-0 mb-1 text-[0.95rem] font-semibold">{lecture.title}</p>
      <p className="m-0 mb-5 text-[0.82rem] text-text-muted">
        {lecture.pages} trang · PDF
      </p>
      <Button as="a" href={url} target="_blank" rel="noopener" variant="primary" block>
        Mở tài liệu
      </Button>
      <Button as="a" href={url} download={lecture.file} block className="mt-2.5">
        ⬇ Tải về máy
      </Button>
      <p className="mt-4 mb-0 text-[0.78rem] leading-relaxed text-text-muted">
        Điện thoại không hiển thị PDF ngay trong trang web được, nên tài liệu sẽ mở bằng
        trình đọc sẵn có của máy. Tải về một lần thì lần sau xem được cả khi không có mạng.
      </p>
    </div>
  )
}

function PdfViewer({ lecture }) {
  const url = lectureUrl(lecture)

  return (
    <Container wide>
      <BackLink to="/pdf" />

      <div className="mb-3 flex flex-wrap items-center justify-between gap-3">
        <h1 className="text-[1.1rem] font-extrabold leading-snug sm:text-[1.25rem]">
          {lecture.icon} {lecture.title}
        </h1>
        {CAN_EMBED_PDF && (
          <div className="flex gap-2">
            <Button as="a" href={url} target="_blank" rel="noopener" className="px-3.5 py-2 text-[0.85rem]">
              ↗ Mở tab mới
            </Button>
            <Button
              as="a"
              href={url}
              download={lecture.file}
              variant="primary"
              className="px-3.5 py-2 text-[0.85rem]"
            >
              ⬇ Tải xuống
            </Button>
          </div>
        )}
      </div>

      {CAN_EMBED_PDF ? (
        <div className="h-[calc(100dvh-170px)] min-h-[420px] overflow-hidden rounded-card border border-border bg-surface shadow-soft">
          <object data={`${url}#view=FitH`} type="application/pdf" className="h-full w-full">
            <iframe src={`${url}#view=FitH`} title={lecture.title} className="h-full w-full border-0">
              <div className="p-6 text-center text-text-muted">
                Trình duyệt của bạn không hiển thị được PDF trực tiếp.
              </div>
            </iframe>
          </object>
        </div>
      ) : (
        <OpenPdfCard lecture={lecture} url={url} />
      )}
    </Container>
  )
}

export default function Pdf() {
  const { lectureId } = useParams()
  const lecture = lectureId ? lectureById(lectureId) : null

  if (lectureId && !lecture) {
    return (
      <Container>
        <BackLink to="/pdf" />
        <p className="text-center text-text-muted">Không tìm thấy tài liệu này.</p>
      </Container>
    )
  }

  return lecture ? <PdfViewer lecture={lecture} /> : <PdfList />
}
