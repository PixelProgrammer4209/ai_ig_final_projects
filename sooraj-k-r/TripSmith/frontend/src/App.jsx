// frontend/src/App.jsx
import { useState } from 'react'
import './App.css'

function App() {
  // 1. State for the form inputs
  const [formData, setFormData] = useState({
    starting_location: '',
    destination: '',
    travel_days: 1,
    travelers: 1,
    total_budget: 1000
  });

  // 2. State for the UI feedback
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  // 3. Handle user typing in the form
  const handleChange = (e) => {
    const { name, value } = e.target;
    
    // Pydantic expects numbers for these fields, not strings, so we convert them
    const isNumberField = ['travel_days', 'travelers', 'total_budget'].includes(name);
    const parsedValue = isNumberField ? Number(value) : value;
    
    setFormData({ ...formData, [name]: parsedValue });
  };

  // 4. Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault(); // Prevents the page from refreshing
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch("http://localhost:8000/api/plan-trip", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData)
      });

      const data = await response.json();

      // If the backend returns an error (400, 422, 500)
      if (!response.ok) {
        // FastAPI returns validation errors in an array, and custom errors as a string
        const errorMsg = Array.isArray(data.detail) 
          ? data.detail[0].msg // Pydantic error
          : data.detail;       // Our custom exception
        throw new Error(errorMsg || "An error occurred");
      }

      // If successful, save the result to display it
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>TripSmith</h1>
      <h2>Plan Your Kerala Trip</h2>

      <form onSubmit={handleSubmit} className="trip-form">
        <div className="form-group">
          <label>Starting Location:</label>
          <input type="text" name="starting_location" value={formData.starting_location} onChange={handleChange} required placeholder="e.g. Mumbai" />
        </div>

        <div className="form-group">
          <label>Destination (in Kerala):</label>
          <input type="text" name="destination" value={formData.destination} onChange={handleChange} required placeholder="e.g. Munnar, Kerala" />
        </div>

        <div className="form-group">
          <label>Travel Days:</label>
          <input type="number" name="travel_days" min="1" max="30" value={formData.travel_days} onChange={handleChange} required />
        </div>

        <div className="form-group">
          <label>Number of Travelers:</label>
          <input type="number" name="travelers" min="1" max="20" value={formData.travelers} onChange={handleChange} required />
        </div>

        <div className="form-group">
          <label>Total Budget (INR):</label>
          <input type="number" name="total_budget" min="1" value={formData.total_budget} onChange={handleChange} required />
        </div>

        <button type="submit" disabled={loading}>
          {loading ? "Planning..." : "Plan My Trip"}
        </button>
      </form>

      {/* Display Errors */}
      {error && (
        <div className="error-box">
          <strong>Error:</strong> {error}
        </div>
      )}

      {/* Display Success Response */}
      {result && (
        <div className="success-box">
          <h3>{result.status.toUpperCase()}</h3>
          <p>{result.message}</p>
          <pre>{JSON.stringify(result.received_data, null, 2)}</pre>
        </div>
      )}
    </div>
  )
}

export default App