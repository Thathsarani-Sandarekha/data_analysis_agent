import React, { useState } from "react";
import axios from "axios";
import "./ChatInterface.css";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

function ChatInterface() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!query.trim()) return;
    setLoading(true);
    try {
      const res = await axios.post(`${BACKEND_URL}/query`, { query });
      setResponse(res.data);
    } catch (error) {
      console.error("API Error:", error);
      setResponse({ summary: "Something went wrong.", table: [], chart_path: null });
    }
    setLoading(false);
  };

    return (
      <div className="chat-container">
        <h1>🌿 Air Quality Data Assistant</h1>
        <div className="input-box">
          <textarea
            placeholder="Ask a question about air quality data..."
            value={query}
            rows={3}
            onChange={(e) => setQuery(e.target.value)}
          />
          <button onClick={handleSubmit} disabled={loading}>
            {loading ? "Analyzing..." : "Submit"}
          </button>
        </div>
    
        {response && (
          <div className="response-box fade-in">
            <h3>🧠 Summary</h3>
            <p>{response.summary}</p>
    
            {response.table?.length > 0 && (
              <>
                <h3>📋 Table</h3>
                <div className="table-wrapper">
                  <table>
                    <thead>
                      <tr>
                        {Object.keys(response.table[0]).map((col) => (
                          <th key={col}>{col}</th>
                        ))}
                      </tr>
                    </thead>
                    <tbody>
                      {response.table.map((row, idx) => (
                        <tr key={idx}>
                          {Object.values(row).map((val, i) => (
                            <td key={i}>{val}</td>
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </>
            )}
    
            {response.chart_path && (
              <>
                <h3>📈 Chart</h3>
                <img
                  src={`${BACKEND_URL}/${response.chart_path}`}
                  alt="Chart"
                  className="chart-img"
                />
              </>
            )}
          </div>
        )}
      </div>
    );    
}

export default ChatInterface;
