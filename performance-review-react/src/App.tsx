
import { useState } from "react";
import SideNav from "./components/navigation/SideNav";
import EmployeeDropdown from './components/employee/EmployeeDropdown'
import ReviewPeriodDropdown from './components/review_period/ReviewPeriodDropdown'

export default function App() {
  const [page, setPage] = useState("dashboard");
   const [employeeId, setEmployeeId] = useState<number | "">("");
  const [reviewPeriodId, setReviewPeriodId] = useState<number | "">("");

  return (
    <div style={{ display: "flex", height: "100vh" }}>
      <SideNav setPage={setPage} />

      <div style={{ flex: 1, padding: "20px" }}>
        {page === "dashboard" && <h2>Dashboard</h2>}
        {page === "employees" &&   <EmployeeDropdown
        value={employeeId}
        onChange={setEmployeeId}
      />}
        {page === "reviews" && <ReviewPeriodDropdown
        value={reviewPeriodId}
        onChange={setReviewPeriodId}
      />}
        {page === "submit-review" && <h2>Submit Review</h2>}
      </div>
    </div>
  );
}

