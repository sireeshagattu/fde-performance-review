interface PaginationProps {
  currentPage: number
  hasNextPage: boolean
  onPageChange: (page: number) => void
  totalPages?: number                       // NEW: optional, enables numbered buttons
}

const Pagination = ({ currentPage, hasNextPage, onPageChange, totalPages }: PaginationProps) => {
  // NEW: turn totalPages (e.g. 4) into [1, 2, 3, 4]
  const pageNumbers = totalPages
    ? Array.from({ length: totalPages }, (_, index) => index + 1)
    : [];

  return (
    <div>
      <button
        onClick={() => onPageChange(currentPage - 1)}
        disabled={currentPage === 1}
        aria-label="Previous page"
      >
        ‹
      </button>

      {totalPages ? (
        // NEW: one button per page; the current one is bold
        pageNumbers.map((page) => (
          <button
            key={page}
            onClick={() => onPageChange(page)}
            aria-current={page === currentPage ? "page" : undefined}
            style={{ fontWeight: page === currentPage ? "bold" : "normal" }}
          >
            {page}
          </button>
        ))
      ) : (
        // Unchanged behaviour when totalPages isn't given
        <span>{currentPage}</span>
      )}

      <button
        onClick={() => onPageChange(currentPage + 1)}
        disabled={!hasNextPage}
        aria-label="Next page"
      >
        ›
      </button>
    </div>
  )
}

export default Pagination
