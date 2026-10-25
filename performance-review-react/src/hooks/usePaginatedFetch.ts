import { useState, useEffect } from 'react'


/*curl -X 'GET' \
  'http://127.0.0.1:8000/api/employees?limit=10&offset=5' \
  -H 'accept: */
export function usePaginatedFetch<T>(url: string, initialPage: number = 1, limit: number = 10, refresh: boolean = false) {
  const [data, setData] = useState<T[]>([])
  const [loading, setLoading] = useState<boolean>(true)
  const [error, setError] = useState<string | null>(null)
  const[currentPage, setCurrentPage] = useState<number>(initialPage)

  useEffect(() => {
    setLoading(true)
    setError(null)
    const offset = (currentPage-1) * limit
    fetch(`${url}?limit=${limit}&offset=${offset}`)
      .then((response) => {
        if (!response.ok) {
          throw new Error('Network response was not ok')
        }
        return response.json()
      })
      .then((data) => {
        setData(data)
        setLoading(false)
      })
      .catch((error) => {
        setError(error.message)
        setLoading(false)
      })
  }, [url, currentPage, limit, refresh])

  return { data, loading, error, currentPage, setCurrentPage, hasNextPage: data.length === limit }
}


