import { useState } from "react";
import "./App.css";

function App() {
  const [code, setCode] = useState("");
  const [language, setLanguage] = useState("Python");
  const [review, setReview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [fileNames, setFileNames] = useState([]);

  const parseReview = (text) => {
    const sections = {
      bugs: "",
      security: "",
      improvements: "",
      severity: "",
      score: "",
    };

    const lines = text.split("\n");
    let current = "";

    lines.forEach((line) => {
      if (line.includes("BUGS")) current = "bugs";
      else if (line.includes("SECURITY")) current = "security";
      else if (line.includes("IMPROVEMENTS")) current = "improvements";
      else if (line.includes("SEVERITY")) {
        sections.severity = line.replace("SEVERITY:", "").trim();
        current = "";
      } else if (line.includes("SCORE")) {
        sections.score = line.replace("SCORE:", "").trim();
        current = "";
      } else if (current) {
        sections[current] += line + "\n";
      }
    });

    return sections;
  };

  const handleFilesChange = async (e) => {
    const files = Array.from(e.target.files || []);
    if (!files.length) return;

    setFileNames(files.map((file) => file.name));

    try {
      const fileContents = await Promise.all(
        files.map(async (file) => {
          const text = await file.text();
          return `// FILE: ${file.name}\n${text}`;
        })
      );

      const combinedCode = fileContents.join("\n\n");
      setCode(combinedCode);
    } catch (error) {
      setCode("");
      setFileNames([]);
      setReview({
        bugs: "",
        security: "",
        improvements: "Failed to read uploaded files",
        severity: "Unknown",
        score: "N/A",
      });
    }
  };

  const handleReview = async () => {
    try {
      if (!code.trim()) {
        setReview({
          bugs: "",
          security: "",
          improvements: "Code cannot be empty",
          severity: "Unknown",
          score: "N/A",
        });
        return;
      }

      setLoading(true);
      setReview(null);

      const response = await fetch("http://127.0.0.1:8000/review", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ code, language }),
      });

      const data = await response.json();

      if (data.error) {
        setReview({
          bugs: "",
          security: "",
          improvements: data.error,
          severity: "Unknown",
          score: "N/A",
        });
      } else {
        setReview(parseReview(data.review));
      }
    } catch (error) {
      setReview({
        bugs: "",
        security: "",
        improvements: "Error connecting to backend",
        severity: "Unknown",
        score: "N/A",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <h1 className="title">CodeSense 🚀</h1>
      <p className="subtitle">AI Code Review Platform</p>

      <div className="card">
        <input
          type="file"
          multiple
          accept=".py,.js,.java,.cpp,.txt"
          onChange={handleFilesChange}
        />

        {fileNames.length > 0 && (
          <div className="file-list">
            <strong>Selected Files:</strong>
            <ul>
              {fileNames.map((name, index) => (
                <li key={index}>{name}</li>
              ))}
            </ul>
          </div>
        )}

        <select
          value={language}
          onChange={(e) => setLanguage(e.target.value)}
        >
          <option>Python</option>
          <option>JavaScript</option>
          <option>Java</option>
          <option>C++</option>
        </select>

        <textarea
          placeholder="Paste your code here or upload files..."
          value={code}
          onChange={(e) => setCode(e.target.value)}
        />

        <button onClick={handleReview}>
          {loading ? "Analyzing..." : "Review Code"}
        </button>
      </div>

      {review && (
        <div className="output-card">
          <h2>Review Output</h2>

          <div className="grid">
            <div className="card-box">
              <h3>🐞 Bugs</h3>
              <pre>{review.bugs || "None found"}</pre>
            </div>

            <div className="card-box">
              <h3>🔐 Security</h3>
              <pre>{review.security || "None found"}</pre>
            </div>

            <div className="card-box">
              <h3>⚡ Improvements</h3>
              <pre>{review.improvements || "None found"}</pre>
            </div>

            <div className="card-box">
              <h3>⚠️ Severity</h3>
              <p>{review.severity || "N/A"}</p>
            </div>

            <div className="card-box">
              <h3>📊 Score</h3>
              <p>{review.score || "N/A"}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;