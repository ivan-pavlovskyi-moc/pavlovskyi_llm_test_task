import React, { useState } from 'react';
import axios from 'axios';
import './styles.css'; // Імпорт CSS-файлу

const App = () => {
  const [query, setQuery] = useState('');
  const [result, setResult] = useState({ data: [] }); // Початкове значення — об'єкт з data
  const [isLoading, setIsLoading] = useState(false);
  const [expandedRestaurants, setExpandedRestaurants] = useState({});

  const handleQuery = async () => {
    if (isLoading) return;
    setIsLoading(true);

    const requestData = { text: query };
    console.log("📤 Sending request:", JSON.stringify(requestData));

    try {
      const response = await axios.post("http://localhost:8000/query/", requestData, {
        headers: { "Content-Type": "application/json" },
      });

      console.log("✅ Response from backend:", response.data);
      setResult(response.data); // Оновлюємо result з відповіддю від бекенду
    } catch (error) {
      if (error.response) {
        console.error("❌ Response error:", error.response.status, error.response.data);
      } else {
        console.error("❌ Axios Error:", error.message);
      }
      setResult({ data: [] }); // Встановлюємо пустий масив у випадку помилки
    } finally {
      setIsLoading(false);
    }
  };

  const toggleExpand = (restaurantName) => {
    setExpandedRestaurants((prev) => ({
      ...prev,
      [restaurantName]: !prev[restaurantName],
    }));
  };

  // Групування страв за ресторанами
  const groupedResults = result.data.reduce((acc, dish) => {
    const restaurantName = dish.restaurant_name;
    if (!acc[restaurantName]) {
      acc[restaurantName] = [];
    }
    acc[restaurantName].push(dish);
    return acc;
  }, {});

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>Fast Food Dish Aggregator</h1>
      <div style={styles.inputContainer}>
        <label htmlFor="queryInput" style={styles.label}>
          Enter dish name, dish type, price range, calories, or restaurant:
        </label>
        <input
          id="queryInput"
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Type your query here..."
          style={styles.input}
        />
        <button
          onClick={handleQuery}
          style={isLoading ? { ...styles.button, ...styles.buttonLoading } : styles.button}
          disabled={isLoading}
        >
          {isLoading ? (
            <div className="loading-spinner"></div>
          ) : (
            "Search"
          )}
        </button>
      </div>

      {Object.keys(groupedResults).length > 0 ? (
        <div style={styles.tableContainer}>
          <h2 style={styles.subtitle}>Search Results:</h2>
          {Object.entries(groupedResults).map(([restaurantName, dishes]) => (
            <div key={restaurantName} style={styles.restaurantContainer}>
              <h3 style={styles.restaurantName}>{restaurantName}</h3>
              <table style={styles.table}>
                <thead>
                  <tr>
                    <th style={styles.th}>Name</th>
                    <th style={styles.th}>Type</th>
                    <th style={styles.th}>Price ($)</th>
                    <th style={styles.th}>Calories</th>
                    <th style={styles.th}>Meal Time</th>
                  </tr>
                </thead>
                <tbody>
                  {dishes.slice(0, expandedRestaurants[restaurantName] ? dishes.length : 5).map((dish, index) => (
                    <tr key={index} style={styles.tr}>
                      <td style={styles.td}>{dish.name}</td>
                      <td style={styles.td}>{dish.type}</td>
                      <td style={styles.td}>{dish.price}</td>
                      <td style={styles.td}>{dish.calories}</td>
                      <td style={styles.td}>{dish.recommended_meal_time}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
              {dishes.length > 5 && (
                <button
                  onClick={() => toggleExpand(restaurantName)}
                  style={styles.seeMoreButton}
                >
                  {expandedRestaurants[restaurantName] ? "See less" : "See more"}
                </button>
              )}
            </div>
          ))}
        </div>
      ) : (
        <p style={styles.noResults}>No results to display.</p>
      )}
    </div>
  );
};

export default App;

// Стилі
const styles = {
  container: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    padding: "20px",
    fontFamily: "Arial, sans-serif",
    backgroundColor: "#f5f5f5",
    minHeight: "100vh",
  },
  title: {
    fontSize: "2rem",
    marginBottom: "20px",
    color: "#333",
  },
  inputContainer: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    gap: "10px",
    marginBottom: "20px",
  },
  label: {
    fontSize: "1rem",
    color: "#555",
  },
  input: {
    padding: "10px",
    fontSize: "1rem",
    width: "300px",
    borderRadius: "5px",
    border: "1px solid #ccc",
  },
  button: {
    padding: "10px 20px",
    fontSize: "1rem",
    backgroundColor: "#007bff",
    color: "#fff",
    border: "none",
    borderRadius: "5px",
    cursor: "pointer",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
  },
  buttonLoading: {
    backgroundColor: "#007bff",
    cursor: "not-allowed",
  },
  tableContainer: {
    marginTop: "20px",
    width: "80%",
    maxWidth: "800px",
  },
  restaurantContainer: {
    marginBottom: "20px",
  },
  restaurantName: {
    fontSize: "1.5rem",
    marginBottom: "10px",
    color: "#333",
  },
  subtitle: {
    fontSize: "1.5rem",
    marginBottom: "10px",
    color: "#333",
  },
  table: {
    width: "100%",
    borderCollapse: "collapse",
    backgroundColor: "#fff",
    boxShadow: "0 0 10px rgba(0, 0, 0, 0.1)",
  },
  th: {
    padding: "12px",
    backgroundColor: "#007bff",
    color: "#fff",
    textAlign: "left",
  },
  tr: {
    borderBottom: "1px solid #ddd",
  },
  td: {
    padding: "12px",
    textAlign: "left",
  },
  noResults: {
    fontSize: "1.2rem",
    color: "#777",
    marginTop: "20px",
  },
  seeMoreButton: {
    padding: "5px 10px",
    fontSize: "0.9rem",
    backgroundColor: "#007bff",
    color: "#fff",
    border: "none",
    borderRadius: "5px",
    cursor: "pointer",
    marginTop: "10px",
  },
};