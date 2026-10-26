
import type ReviewPeriod from '../../interfaces/ReviewPeriod';
import React,{useState, useEffect } from 'react';   
interface ReviewPeriodDropdownProps {
  value: number | "";
  onChange: (reviewPeriodId: number |"") => void;
}

export default function ReviewPeriodDropdown({
  value,
  onChange,
}: ReviewPeriodDropdownProps) {
  const [reviewPeriods, setReviewPeriods] = useState<ReviewPeriod[]>([]);

  useEffect(() => {
    fetch("http://localhost:8000/api/review-periods")
      .then((res) => res.json())
      .then((data) => {  setReviewPeriods(data.review_periods); });
  }, []);

  return (
    <select
      value={value}
      onChange={(e) =>     onChange(e.target.value === "" ? "" : Number(e.target.value))}
    >
      <option value="">Select Review Period</option>

      {reviewPeriods.map((reviewPeriod) => (
        reviewPeriod.status.toUpperCase() === "OPEN" && (
        <option key={reviewPeriod.id} value={reviewPeriod.id}>
          {reviewPeriod.name}
        </option>
      )
      ))}
    </select>
  );
}


