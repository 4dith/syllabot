// netlify/functions/query-llm.js
export async function handler(event) {
  // Handle CORS preflight
  if (event.httpMethod === "OPTIONS") {
    return {
      statusCode: 204,
      headers: {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type"
      }
    };
  }

  if (event.httpMethod !== "POST") {
    return {
      statusCode: 405,
      body: "Method Not Allowed"
    };
  }

  let body;
  try {
    body = JSON.parse(event.body);
  } catch {
    return {
      statusCode: 400,
      body: JSON.stringify({ error: "Invalid JSON" })
    };
  }

  const promptText = (body.promptText || "").trim();
  if (!promptText) {
    return {
      statusCode: 400,
      body: JSON.stringify({ error: "Missing promptText" })
    };
  }

  const apiKey = process.env.GITHUB_MODEL_KEY;  // stored privately in Netlify
  if (!apiKey) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: "Server not configured" })
    };
  }

  const endpoint = "https://models.inference.ai.azure.com/chat/completions";

  const payload = {
    model: "gpt-4o-mini",
    messages: [
      { role: "user", content: promptText }
    ]
  };

  try {
    const res = await fetch(endpoint, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${apiKey}`
      },
      body: JSON.stringify(payload)
    });

    const json = await res.json();

    const reply =
      json?.choices?.[0]?.message?.content ??
      json?.choices?.[0]?.text ??
      "No reply produced";

    return {
      statusCode: 200,
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*"
      },
      body: JSON.stringify({ reply })
    };

  } catch (err) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: "LLM error", details: err.message })
    };
  }
}
