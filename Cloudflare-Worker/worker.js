export default {
  async fetch(request, env, ctx) {
    // Handle CORS preflight
    if (request.method === "OPTIONS") {
      return new Response(null, {
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Methods": "POST, OPTIONS",
          "Access-Control-Allow-Headers": "Content-Type"
        }
      });
    }

    if (request.method !== "POST") {
      return new Response("Method not allowed", { status: 405 });
    }

    const { prompt } = await request.json();
    if (!prompt) {
      return new Response("Missing prompt", { status: 400 });
    }

    const API_KEY = env.GEMINI_API_KEY;
    if (!API_KEY) {
      return new Response(JSON.stringify({ response: "API Key missing." }), { status: 500, headers: { "Access-Control-Allow-Origin": "*" }});
    }

    const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${API_KEY}`;

    const geminiPayload = {
      contents: [{ parts: [{ text: prompt }] }]
    };

    try {
      const apiResponse = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(geminiPayload)
      });
      
      const data = await apiResponse.json();
      let reply = "I'm sorry, the ancient realms are silent at the moment.";
      
      if (data.candidates && data.candidates.length > 0) {
        reply = data.candidates[0].content.parts[0].text;
      }

      return new Response(JSON.stringify({ response: reply }), {
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Content-Type": "application/json"
        }
      });
    } catch (err) {
      return new Response(JSON.stringify({ response: "I encountered an error reaching the oracle." }), {
        status: 500,
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Content-Type": "application/json"
        }
      });
    }
  }
};
