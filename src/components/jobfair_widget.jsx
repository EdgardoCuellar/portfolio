import React, {useState} from "react";

export default function JobFairWidget({apiUrl, apiKey}) {
  const [q, setQ] = useState("");
  const [ans, setAns] = useState("");
  const [loading, setLoading] = useState(false);

  async function send() {
    setLoading(true);
    try {
      const res = await fetch(apiUrl + "/qa", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "x-api-key": apiKey
        },
        body: JSON.stringify({question: q})
      });
      const j = await res.json();
      setAns(j.answer || JSON.stringify(j));
    } catch (e) {
      setAns("Error: " + e.toString());
    }
    setLoading(false);
  }

  return (
    <div style={{border:"1px solid #ddd", padding:12, borderRadius:6, maxWidth:520}}>
      <h4>Ask about my portfolio</h4>
      <textarea value={q} onChange={e=>setQ(e.target.value)} rows={4} style={{width:"100%"}} />
      <div style={{marginTop:8}}>
        <button onClick={send} disabled={loading || !q}>Ask</button>
      </div>
      <pre style={{whiteSpace:"pre-wrap", marginTop:12, background:"#f8f8f8", padding:10}}>{ans}</pre>
      <small>Powered by local LM Studio (demo)</small>
    </div>
  );
}