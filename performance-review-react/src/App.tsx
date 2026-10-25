import { useState } from "react";
import SideNav from "./components/navigation/SideNav";


export default function App() {
  const [page, setPage] = useState("dashboard");

  return (
    <div style={{ display: "flex", height: "100vh" }}>
      <SideNav setPage={setPage} />

      <div style={{ flex: 1, padding: "20px" }}>
        {page === "dashboard" && <h2>Dashboard</h2>}
        {page === "employees" && <h2>Employees</h2>}
        {page === "reviews" && <h2>Reviews</h2>}
        {page === "submit-review" && <h2>Submit Review</h2>}
      </div>
    </div>
  );
}