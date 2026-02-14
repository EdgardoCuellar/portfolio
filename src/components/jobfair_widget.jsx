import React, { useState, useEffect } from "react";
import cvFunctional from "../assets/corpus/CV_2025_Edgardo_Cuellar_Functional_Analyst.txt";
import cvSoftware from "../assets/corpus/CV_2025_Edgardo_Cuellar_Software_Engineer.txt";
import informal from "../assets/corpus/informel.txt";
import profileTxt from "../assets/corpus/profile.txt";
import qaTxt from "../assets/corpus/question_reponse.txt";
import portfolioTxt from "../assets/corpus/website_project_extracted.txt";

// Make me a two value dict with file name as key, content one as value, and content two as importance (1-5) i'm going to fix it later
const fileDict = {
  "CV_2025_Edgardo_Cuellar_Functional_Analyst.txt": { content: cvFunctional, importance: 3 },
  "CV_2025_Edgardo_Cuellar_Software_Engineer.txt": { content: cvSoftware, importance: 3 },
  "informel.txt": { content: informal, importance: 4 },
  "profile.txt": { content: profileTxt, importance: 5 },
  "question_reponse.txt": { content: qaTxt, importance: 5 },
  "website_project_extracted.txt": { content: portfolioTxt, importance: 3 },
};

export default function JobFairWidget({ apiKey }) {
  const [q, setQ] = useState("");
  const [ans, setAns] = useState("");
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [context, setContext] = useState("");

  // Load and combine context on mount
  useEffect(() => {
    let combined = "";

    Object.entries(fileDict).forEach(([name, { content, importance }]) => {
      combined += `--- ${name} (importance: ${importance}) ---\n${content}\n\n`;
    });

    setContext(combined);
  }, []);

  // System prompt template (your rules)
  const systemPromptBase = `You are an assistant that uses only the provided CONTEXT chunks to answer.
RULES (strict):
1) Detect the user's language and answer in that language. If the language cannot be detected, default to French.
2) Be concise: -5 sentences for factual answers.
3) Do NOT mention, print or list any sources, filenames, or indices in the answer. Never output lines like "Source: [3]".
4) Use only information present in the provided context. Or try to find the answer by combining multiple pieces of information from different context chunks.
5) Do not invent facts or numbers. If asked for an opinion, prefix with "Opinion:".
6) Always talk as me, as "I am", "I did", ...  
7) Importance metric is provided for each context chunk, prioritize higher (5) importance ones when formulating the answer. Lower importance (1).

CONTEXT:
`;

  async function send() {
    if (!context) {
      setError("Context files not loaded yet.");
      return;
    }

    setError("");
    setAns("");
    setSources([]);
    setLoading(true);

    try {
      const res = await fetch("https://openrouter.ai/api/v1/chat/completions", {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${apiKey}`,
          "Content-Type": "application/json",
          "HTTP-Referer": window.location.origin, // Optional, helps rankings
          "X-Title": "Job Fair Widget",           // Optional, identifies your app
        },
        body: JSON.stringify({
          model: "openai/gpt-oss-120b:free",
          messages: [
            {
              role: "system",
              content: systemPromptBase + context,
            },
            {
              role: "user",
              content: q,
            },
          ],
        }),
      });

      if (!res.ok) {
        const text = await res.text();
        throw new Error(`OpenRouter error ${res.status}: ${text}`);
      }

      const j = await res.json();
      const answer = j.choices[0]?.message?.content || "No answer returned.";
      setAns(answer);
      // sources not available from OpenRouter directly, but you could keep this for future RAG
      setSources(["Personal files"]);
    } catch (e) {
      console.error(e);
      setError(e.message || "Unknown error");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="w-full min-h-[300px] flex flex-col items-center justify-center gap-4">
      <div className="max-w-xl w-full p-6 bg-secondary rounded-lg text-text">
        <h4 className="text-xl font-bold mb-3 text-accent">Any Question ? (FR/NL)</h4>

        <textarea
          value={q}
          onChange={(e) => setQ(e.target.value)}
          rows={3}
          placeholder="Type your question here... | Ecrivez votre question ici..."
          className="w-full p-3 rounded-md bg-primary text-gray-100 focus:outline-none focus:ring-2 focus:ring-accent"
        />

        <div className="w-full flex items-center gap-3 mt-3 justify-center">
          <button
            onClick={send}
            disabled={loading || !q || !context}
            className="px-5 py-2 bg-accent text-white font-semibold rounded hover:bg-accent-secondary transition"
          >
            {loading ? "Thinking...(1-2s)" : "Ask"}
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
            <pre className="whitespace-pre-wrap text-sm text-gray-100">{ans}</pre>
          </div>
        )}

        <div className="mt-3 text-xs text-gray-500">
          Run on Openrouter API using "openai/gpt-oss-120b:free".
        </div>
      </div>
    </div>
  );
}