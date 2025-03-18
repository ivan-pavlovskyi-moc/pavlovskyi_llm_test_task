import React, { useState } from 'react';
import axios from 'axios';

const App = () => {
  const [query, setQuery] = useState('');
  const [result, setResult] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleQuery = async () => {
    if (isLoading) return; // Якщо завантаження вже триває, нічого не робимо
    setIsLoading(true); // Початок завантаження
    const requestData = { text: query }; // Формуємо тіло запиту
    console.log("📤 Відправка запиту:", JSON.stringify(requestData)); // Лог перед запитом

    try {
      const response = await axios.post("http://localhost:8000/query/", requestData, {
        headers: { "Content-Type": "application/json" },
      });

      console.log("✅ Відповідь від бекенду:", response.data); // Лог відповіді
      setResult(response.data.data || []); // Оновлюємо результат
    } catch (error) {
      if (error.response) {
        console.error("❌ Помилка відповіді:", error.response.status, error.response.data);
      } else {
        console.error("❌ Axios Error:", error.message);
      }
      setResult([]); // Очищаємо результат у разі помилки
    } finally {
      setIsLoading(false); // Завершення завантаження
    }
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>Ivan Pavlovskyi Test LLM Task</h1> {/* Змінено тут */}
      <div style={styles.inputContainer}>
        <label htmlFor="queryInput" style={styles.label}>
          Введіть назву страви, діапазон цін, калорійність чи тип страви:
        </label>
        <input
          id="queryInput"
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Напишіть ваш запит тут..."
          style={styles.input}
        />
        <button onClick={handleQuery} style={styles.button} disabled={isLoading}>
          {isLoading ? "Завантаження..." : "Пошук"}
        </button>
      </div>

      {result.length > 0 ? (
        <div style={styles.tableContainer}>
          <h2 style={styles.subtitle}>Результати пошуку:</h2>
          <table style={styles.table}>
            <thead>
              <tr>
                <th style={styles.th}>Назва</th>
                <th style={styles.th}>Тип</th>
                <th style={styles.th}>Ціна ($)</th>
                <th style={styles.th}>Калорії</th>
                <th style={styles.th}>Час прийому</th>
              </tr>
            </thead>
            <tbody>
              {result.map((item, index) => (
                <tr key={index} style={styles.tr}>
                  <td style={styles.td}>{item.name}</td>
                  <td style={styles.td}>{item.type}</td>
                  <td style={styles.td}>{item.price}</td>
                  <td style={styles.td}>{item.calories}</td>
                  <td style={styles.td}>{item.recommended_meal_time}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <p style={styles.noResults}>Немає результатів для відображення.</p>
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
  },
  buttonDisabled: {
    backgroundColor: "#ccc",
    cursor: "not-allowed",
  },
  tableContainer: {
    marginTop: "20px",
    width: "80%",
    maxWidth: "800px",
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
};