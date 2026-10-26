export default interface PerformanceReviewCreate {
  employee_id: number;      // numeric key (24), NOT the EMP code
  period_id: number;        // numeric key of review_periods (2 = H2 2026)
  quality_rating: number;   // 1–5
  delivery_rating: number;  // 1–5
  teamwork_rating: number;  // 1–5
  comments: string;
}
