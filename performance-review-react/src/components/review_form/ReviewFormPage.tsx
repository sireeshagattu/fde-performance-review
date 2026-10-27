import { useState } from 'react';
import EmployeeDropdown from '../employee/EmployeeDropdown';
import ReviewPeriodDropdown from '../review_period/ReviewPeriodDropdown';
import StarRating from '../star_rating/StarRating';
import type PerformanceReviewCreate from '../../interfaces/PerformanceReviewCreate';
import './ReviewForm.css';

// One optional message per field. A missing key means that field is OK.
interface FormErrors {
    employee?: string;
    period?: string;
    quality?: string;
    delivery?: string;
    teamwork?: string;
    comments?: string;
}

// One place that knows how to send a new review to the API.
// It sits outside the component because it doesn't need any state.
function submitReview(payload: PerformanceReviewCreate): Promise<void> {
    return fetch("http://localhost:8000/api/performance-reviews", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
    })
        .then(async (res) => {
            // Treat 4xx/5xx answers as errors.
            // The API sends { code, message } on known errors (e.g. duplicate review).
            if (!res.ok) {
                const body = await res.json().catch(() => null);
                throw new Error(body?.message ?? `Server responded ${res.status}`);
            }
        })
        .catch((err) => {
            // fetch itself rejects with a TypeError when the server can't be reached
            if (err instanceof TypeError) {
                throw new Error("Cannot reach the server. Check your connection and try again.");
            }
            throw err;
        });
}



export default function ReviewFormPage() {
    // "" means "nothing selected yet"
    const [employeeId, setEmployeeId] = useState<number | "">("");
    const [periodId, setPeriodId] = useState<number | "">("");
    const [qualityRating, setQualityRating] = useState(0);
    const [deliveryRating, setDeliveryRating] = useState(0);
    const [teamworkRating, setTeamworkRating] = useState(0);
    const [comments, setComments] = useState("");
    const [errors, setErrors] = useState<FormErrors>({});
    const [submitting, setSubmitting] = useState(false);
    const [submitError, setSubmitError] = useState<string | null>(null);
    const [successMessage, setSuccessMessage] = useState<string | null>(null);



    // Put every field back to its starting value
    function handleReset() {
        setEmployeeId("");
        setPeriodId("");
        setQualityRating(0);
        setDeliveryRating(0);
        setTeamworkRating(0);
        setComments("");
        setErrors({});
        setSubmitError(null);
        setSuccessMessage(null);


    }

    // Check every field and collect a message for each problem
    function validate(): FormErrors {
        const found: FormErrors = {};

        if (employeeId === "") found.employee = "Please select an employee";
        if (periodId === "") found.period = "Please select a review period";
        if (qualityRating < 1) found.quality = "Please rate Quality of Work";
        if (deliveryRating < 1) found.delivery = "Please rate Delivery & Ownership";
        if (teamworkRating < 1) found.teamwork = "Please rate Teamwork & Collaboration";
        if (comments.trim() === "") found.comments = "Please enter overall comments";

        return found;
    }

    function handleSubmit() {
        setSubmitError(null);
        setSuccessMessage(null);

        const found = validate();
        setErrors(found);
        if (Object.keys(found).length > 0) return;   // stop: something is missing

        // Build the JSON body exactly as the API expects
        const payload: PerformanceReviewCreate = {
            employee_id: Number(employeeId),   // validation made sure this isn't ""
            period_id: Number(periodId),
            quality_rating: qualityRating,
            delivery_rating: deliveryRating,
            teamwork_rating: teamworkRating,
            comments: comments.trim(),
        };

        setSubmitting(true);
        submitReview(payload)
            .then(() => {
                handleReset();                                   // empty the form for the next review
                setSuccessMessage("Review submitted successfully.");
            })
            .catch((err: Error) => setSubmitError(err.message))
            .finally(() => setSubmitting(false));
    }


    return (
        <form
            className="review-form"
            onSubmit={(e) => {
                e.preventDefault();   // stop the browser from reloading the page
                handleSubmit();
            }}
        >
            <h2>Submit Performance Review</h2>

            <div className="form-row">
                <label className="form-field">
                    Employee *
                    <EmployeeDropdown
                        value={employeeId}
                        onChange={setEmployeeId}
                        onlyActive
                    />
                    {errors.employee && <span className="field-error">{errors.employee}</span>}
                </label>

                <label className="form-field">
                    Review Period *
                    <ReviewPeriodDropdown
                        value={periodId}
                        onChange={setPeriodId}
                    />
                    {errors.period && <span className="field-error">{errors.period}</span>}
                </label>
            </div>

            <h3>Performance Ratings (1 - 5)</h3>

            <div className="rating-row">
                <span>Quality of Work *</span>
                <StarRating value={qualityRating} onChange={setQualityRating} />
                {errors.quality && <span className="field-error">{errors.quality}</span>}
            </div>

            <div className="rating-row">
                <span>Delivery &amp; Ownership *</span>
                <StarRating value={deliveryRating} onChange={setDeliveryRating} />
                {errors.delivery && <span className="field-error">{errors.delivery}</span>}
            </div>

            <div className="rating-row">
                <span>Teamwork &amp; Collaboration *</span>
                <StarRating value={teamworkRating} onChange={setTeamworkRating} />
                {errors.teamwork && <span className="field-error">{errors.teamwork}</span>}
            </div>

            <label className="form-field">
                Overall Comments *
                <textarea
                    rows={5}
                    placeholder="Enter your feedback, strengths, areas of improvement..."
                    value={comments}
                    onChange={(e) => setComments(e.target.value)}
                />
                {errors.comments && <span className="field-error">{errors.comments}</span>}
            </label>

            {successMessage && <p className="form-message success">{successMessage}</p>}
            {submitError && <p className="form-message error">{submitError}</p>}

            <div className="form-actions">
                <button type="button" className="reset-button" onClick={handleReset} disabled={submitting}>
                    Reset
                </button>
                <button type="submit" className="submit-button" disabled={submitting}>
                    {submitting ? "Submitting…" : "Submit Review"}
                </button>
            </div>
        </form>
    );
}
