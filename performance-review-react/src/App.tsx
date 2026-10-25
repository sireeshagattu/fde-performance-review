import { useState } from 'react'
import heroImg from './assets/hero.png'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import './App.css'
import EmployeeDropdown from './components/employee/EmployeeDropdown'
import ReviewPeriodDropdown from './components/review_period/ReviewPeriodDropdown'

function App() {
  const [employeeId, setEmployeeId] = useState<number | "">("");
  const [reviewPeriodId, setReviewPeriodId] = useState<number | "">("");

  return (
    <>
      <section id="center">
  
      <EmployeeDropdown
        value={employeeId}
        onChange={setEmployeeId}
      />
      <ReviewPeriodDropdown
        value={reviewPeriodId}
        onChange={setReviewPeriodId}
      />
       </section>
    </>
  )
}

export default App
