import React, { useState } from "react";

export default function JobFairWidget({ apiUrl, apiKey }) {
  const [q, setQ] = useState("");
  const [ans, setAns] = useState("");
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function send() {
    setError("");
    setAns("");
    setSources([]);
    setLoading(true);
    try {
      const res = await fetch(`${apiUrl}/qa`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "x-api-key": apiKey,
        },
        body: JSON.stringify({ question: q }),
      });
      if (!res.ok) {
        const text = await res.text();
        throw new Error(`Server error ${res.status}: ${text}`);
      }
      const j = await res.json();
      setAns(j.answer || "No answer returned.");
      setSources(j.used_contexts || []);
    } catch (e) {
      console.error(e);
      setError(e.message || "Unknown error");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-xl w-full p-6 bg-secondary border border-gray-700 rounded-lg shadow-lg text-text">
      <h4 className="text-xl font-bold mb-3 text-accent">Ask about my portfolio</h4>

      <textarea
        value={q}
        onChange={(e) => setQ(e.target.value)}
        rows={3}
        placeholder="Type your question here..."
        className="w-full p-3 border rounded-md bg-gray-900 text-gray-100 focus:outline-none focus:ring-2 focus:ring-accent"
      />

      <div className="flex items-center gap-3 mt-3">
        <button
          onClick={send}
          disabled={loading || !q}
          className="px-5 py-2 bg-accent text-white font-semibold rounded hover:bg-accent-secondary transition disabled:opacity-50"
        >
          {loading ? "Thinking..." : "Ask"}
        </button>

        <button
          onClick={() => {
            setQ("");
            setAns("");
            setSources([]);
            setError("");
          }}
          className="px-4 py-2 border border-gray-600 rounded text-sm hover:bg-gray-800 transition"
        >
          Clear
        </button>
      </div>

      {error && (
        <div className="mt-3 text-sm text-red-500 font-medium">
          ⚠️ {error}
        </div>
      )}

      {ans && (
        <div className="mt-5 bg-gray-800 p-4 rounded-md">
          <div className="text-sm font-semibold text-gray-300 mb-2">Answer</div>
          <pre className="whitespace-pre-wrap text-sm text-gray-100">{ans}</pre>
        </div>
      )}

      {sources && sources.length > 0 && (
        <div className="mt-4 bg-gray-900 p-3 rounded-md">
          <div className="text-sm font-semibold text-gray-300 mb-2">Sources</div>
          <ul className="text-xs list-disc list-inside text-gray-400">
            {sources.map((s, i) => (
              <li key={i}>
                <strong className="text-accent">{s.source}</strong>:{" "}
                <span>{s.chunk.slice(0, 150)}{s.chunk.length > 150 ? "…" : ""}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      <div className="mt-3 text-xs text-gray-500">
        ⚡ Powered by my local AI (LM Studio)
      </div>
    </div>
  );
}
