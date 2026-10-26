import type ReviewPeriod from '../../interfaces/ReviewPeriod';
import React,{useState, useEffect } from 'react';   
interface ReviewPeriodDropdownProps {
  value: number | "";
  onChange: (reviewPeriodId: number |"") => void;
  placeholder?: string;
   onlyOpen?: boolean; 
}

export default function ReviewPeriodDropdown({
  value,
  onChange,
   placeholder = "Select Review Period", 
   onlyOpen = true,
}: ReviewPeriodDropdownProps) {
  const [reviewPeriods, setReviewPeriods] = useState<ReviewPeriod[]>([]);

  useEffect(() => {
    fetch("http://localhost:8000/api/review-periods")
      .then((res) => {
        // Treat 4xx/5xx answers (e.g. 503 database down) as errors
        if (!res.ok) throw new Error(`Server responded ${res.status}`);
        return res.json();
      })
      .then((data) => {  setReviewPeriods(data.review_periods ?? []); })
      .catch(() => setReviewPeriods([]));   // keep an empty list so .map below never sees undefined
  }, []);

  return (
    <select
      value={value}
      onChange={(e) =>     onChange(e.target.value === "" ? "" : Number(e.target.value))}
    >
      <option value="">{placeholder}</option>

      {reviewPeriods.map((reviewPeriod) => (
        (!onlyOpen || reviewPeriod.status.toUpperCase() === "OPEN") && (
        <option key={reviewPeriod.id} value={reviewPeriod.id}>
          {reviewPeriod.name}
        </option>
      )
      ))}
    </select>
  );
}

