interface PaginationProps {
  currentPage: number
  hasNextPage: boolean
  onPageChange: (page: number) => void
}

    // prevent going to a page less than 1 and above totalPages
const Pagination = ( { currentPage, hasNextPage, onPageChange }: PaginationProps ) => {
  return (

    <div>
      <button 
        onClick={() => onPageChange(currentPage - 1)} 
        disabled={currentPage === 1}
      >
        Previous
      </button>
      <span>{currentPage}</span>
      <button 
        onClick={() => onPageChange(currentPage + 1)} 
        disabled={!hasNextPage}
      >
        Next
      </button>
    </div>
  )
}

export default Pagination