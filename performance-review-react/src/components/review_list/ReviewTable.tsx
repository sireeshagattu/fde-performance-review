import type Review from '../../interfaces/Review';
import StatusBadge from './StatusBadge';

interface ReviewTableProps {
  reviews: Review[];
}

export default function ReviewTable({ reviews }: ReviewTableProps) {
  return (
    <table>
      <thead>
        <tr>
          <th>Employee ID</th>
          <th>Employee Name</th>
          <th>Period</th>
          <th>Ratings</th>
          <th>Average</th>
          <th>Status</th>
          <th>Action</th>
        </tr>
      </thead>

      <tbody>
        {reviews.map((review) => (
          <tr key={review.id}>
            <td>{review.employee_code}</td>
            <td>{review.employee_name}</td>
            <td>{review.period_name}</td>
            <td>
              {review.quality_rating}, {review.delivery_rating}, {review.teamwork_rating}
            </td>
            <td>{review.average_rating.toFixed(1)}</td>
            <td>
              <StatusBadge status={review.status} />
            </td>
            <td>
              <button>View</button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
