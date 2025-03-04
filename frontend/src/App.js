import React, { useState } from "react";
import axios from "axios";

function App() {
  const [query, setQuery] = useState("");
  const [result, setResult] = useState([]);

  const handleQuery = async () => {
    const response = await axios.post("http://localhost:8000/query/", { nl_query: query });
    setResult(response.data);
  };

  return (
    <div>
      <h1>SQL Query Generator</h1>
      <input type="text" value={query} onChange={(e) => setQuery(e.target.value)} />
      <button onClick={handleQuery}>Submit</button>
      <pre>{JSON.stringify(result, null, 2)}</pre>
    </div>
  );
}

export default App;
