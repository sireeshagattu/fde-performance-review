
import { useState } from "react";
import SideNav from "./components/navigation/SideNav";
import EmployeeDropdown from './components/employee/EmployeeDropdown'
import ReviewListPage from './components/review_list/reviewListPage'
import ReviewFormPage from './components/review_form/ReviewFormPage'
import ReviewDetailsPage from './components/review_details/ReviewDetailsPage'



export default function App() {
  const [page, setPage] = useState("dashboard");
  const [employeeId, setEmployeeId] = useState<number | "">("");
  const [selectedReviewId, setSelectedReviewId] = useState<number | null>(null);

  return (
    <div style={{ display: "flex", height: "100vh" }}>
      <SideNav page={page === "review-details" ? "reviews" : page} setPage={setPage} />

      <div style={{ flex: 1, padding: "20px" }}>
        {page === "dashboard" && <h2>Dashboard</h2>}
        {page === "reviews" && (
          <ReviewListPage
            onViewReview={(reviewId) => {
              setSelectedReviewId(reviewId);
              setPage("review-details");
            }}
          />
        )}
        {page === "review-details" && selectedReviewId !== null && (
          <ReviewDetailsPage
            reviewId={selectedReviewId}
            onBack={() => setPage("reviews")}
          />
        )}
        {page === "employees" && <EmployeeDropdown
          value={employeeId}
          onChange={setEmployeeId}
        />}
        {page === "submit-review" && <ReviewFormPage />}
      </div>
    </div>
  );
}
