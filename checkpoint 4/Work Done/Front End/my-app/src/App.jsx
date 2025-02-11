import { useState } from "react";
import axios from "axios";
import "./App.css"; // Ensure CSS is imported

function App() {
  const [productId, setProductId] = useState("");
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setReviews([]);

    if (!productId.trim()) {
      setError("Please enter a valid Product ID (ASIN).");
      setLoading(false);
      return;
    }

    // ✅ Construct the Amazon URL from the Product ID
    const productUrl = `https://www.amazon.com/dp/${productId}`;

    try {
      // ✅ Send POST request to Flask backend with the constructed URL
      const response = await axios.post("http://localhost:5000/scrape", { url: productUrl });
      setReviews(response.data.reviews);
    } catch (err) {
      setError("Failed to fetch reviews. Ensure the backend is running.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <div className="card">
        <h2 className="title">
          <span role="img" aria-label="search">🔍</span> Fake Review Detection
        </h2>

        {/* ✅ Input & Button Section */}
        <form onSubmit={handleSubmit} className="form">
          <input
            type="text"
            value={productId}
            onChange={(e) => setProductId(e.target.value)}
            placeholder="Enter Product ID (ASIN) e.g. B06Y1YD5W7"
            className="input"
          />
          <button type="submit" className="button">Check</button>
        </form>

        {/* ✅ Loading Message */}
        {loading && <p className="loading">Processing...</p>}

        {/* ✅ Error Message */}
        {error && <p className="error">{error}</p>}

        {/* ✅ Table Section */}
        {reviews.length > 0 && (
          <div className="table-container">
            <table className="table">
              <thead>
                <tr>
                  <th>Review</th>
                  <th>Classification</th>
                </tr>
              </thead>
              <tbody>
                {reviews.map((review, index) => (
                  <tr key={index} className={index % 2 === 0 ? "row-light" : "row-dark"}>
                    <td>{review.Review}</td>
                    <td className={review.label === "Computer-generated" ? "fake" : "real"}>
                      {review.label}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
