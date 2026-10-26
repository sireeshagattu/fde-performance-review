import './StarRating.css';

interface StarRatingProps {
  value: number;                      // 0 = not rated yet, 1-5 = rating
  onChange: (rating: number) => void;
}

const STARS = [1, 2, 3, 4, 5];

export default function StarRating({ value, onChange }: StarRatingProps) {
  return (
    <div className="star-rating">
      {STARS.map((star) => (
        <button
          key={star}
          type="button"
          className={star <= value ? "star filled" : "star"}
          onClick={() => onChange(star)}
          aria-label={`${star} star${star > 1 ? "s" : ""}`}
        >
          ★
        </button>
      ))}
    </div>
  );
}
