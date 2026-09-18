/**
 * Cloudflare Worker for Kahaanist Customer Support Chatbot
 * Features:
 * - Brand policies injection (Shipping, Returns, Materials & Care, Guarantees)
 * - Anti-hallucination guardrail for out-of-scope queries
 * - Fallback response requesting user email for founder follow-up
 * - Structured email capture logging (console.log with EMAIL_CAPTURE)
 * - API Key robustness (GEMINI_API_KEY || GEMINI_OMNI_API_KEY)
 * - Multi-model fallback (gemini-3.5-flash, gemini-2.5-flash, gemini-1.5-flash, gemini-flash-latest)
 */

const FALLBACK_RESPONSE = "I can only assist with questions about Kahaanist jewelry, mythologies, and our policies. Please provide your email address so our founder can respond to you directly.";

const BRAND_POLICIES = {
  shipping: `Shipping & Delivery Policy:
- Domestic (India): Free Shipping on all orders above ₹2,899. For orders below ₹2,899, a standard shipping fee applies at checkout.
- International (Rest of World): Free International Shipping on all orders above US$65. For orders below US$65, international shipping rates are calculated at checkout based on destination.
- Dispatch & Processing: All orders are handcrafted and dispatched within 3-5 business days. A tracking link is emailed upon shipment.`,

  returns: `Returns & Exchanges Policy:
- All sales are final due to personal hygiene standards and our slow-fashion, handcrafted production model. Products are non-returnable.
- Manufacturing Defects: Free replacement for genuine manufacturing defects. The customer must email connect@kahaanist.com within 48 hours of delivery with their order number, description of the issue, and clear, unedited photos showing the defect.
- Natural brass tarnishing over time and minor hand-cast textural variations are authentic hallmarks of artisanal craft, not defects.`,

  materials: `Materials & Care Guide:
- Materials: Solid recycled brass, hand-cast by traditional Indian artisans. Select designs feature 18K gold-plated finishes, hypoallergenic posts for earrings, or hand-painted enamel details.
- Care Instructions: Keep jewelry dry and away from moisture, water, sweat, perfumes, lotions, hairsprays, and harsh chemicals. Store in an airtight pouch when not in use. Wipe gently with a soft dry cloth after wear.
- Patina: Yes, all our brass jewelry features a premium anti-tarnish coating to maintain its bright shine. However, we still recommend keeping it away from moisture and harsh chemicals for maximum longevity.`,

  guarantees: `Guarantees:
- 7-day hassle-free replacement for verified manufacturing defects.
- Authentic solid recycled brass quality guarantee.`
};

const SYSTEM_INSTRUCTION = `You are the Kahaanist Guide, the official AI concierge for Kahaanist (https://kahaanist.com), an artisanal slow-fashion jewelry brand creating handcrafted solid brass pieces inspired by global mythology, mysticism, and folklore.

CRITICAL RESPONSE STRUCTURE:
Always start your response with a crisp, direct, 1-sentence answer to the user's question. Then, add a blank line, followed by the more detailed explanation or policy.


AUTHENTIC BRAND POLICIES:
1. SHIPPING & DELIVERY:
   - Domestic (India): Free Shipping on orders above ₹2,899. Standard shipping fee applies below ₹2,899.
   - International (Rest of World): Free International Shipping on orders above US$65. For orders below US$65, shipping rates calculated at checkout.
   - Dispatch Processing: Handcrafted and dispatched within 3-5 business days. Tracking details emailed upon shipment.
2. RETURNS & EXCHANGES:
   - All sales are final due to personal hygiene and handcrafted slow-fashion production; strictly non-returnable.
   - Manufacturing Defects: Free replacement for genuine manufacturing defects. Customer must email connect@kahaanist.com within 48 hours of delivery with order number, description, and clear unedited photos.
   - Natural brass patina and hand-cast textural variations are hallmarks of craft, not defects.
3. MATERIALS & CARE:
   - Handcrafted from solid recycled brass, hand-cast by Indian artisans. Select pieces feature 18K gold-plated accents, hypoallergenic posts (earrings), or hand-painted enamel.
   - Care: Keep dry, avoid perfumes/moisture/sweat/chemicals, store in an airtight pouch, wipe with soft cloth. Yes, all our brass jewelry features a premium anti-tarnish coating to maintain its bright shine.
4. GUARANTEES:
   - 7-day replacement for verified manufacturing defects.
   - Authentic solid recycled brass quality guarantee.

CORE COLLECTIONS & MYTHOLOGY:
- Medusa (Earrings & Signet Ring): Greek mythology, protective talisman, fierce female empowerment.
- Tree of Life (Pendant & Drop Earrings): Roots below, branches above, Norse Yggdrasil & Celtic Crann Bethadh, interconnectedness.
- Ouroboros (Pendant & Band Ring): Serpent eating its tail, eternity, renewal, recreation.
- Mermen in Love & Mermaids in Love: Oceanic guardians, eternal devotion beneath the waves.

STRICT ANTI-HALLUCINATION & SCOPE RULES:
- You may ONLY assist with questions about Kahaanist jewelry, collections, mythologies, materials, care, and official brand policies.
- For ANY query outside these topics (including but not limited to general knowledge, coding, programming, math, science, politics, weather, recipes, external brands, translation, trivia, or general assistance) OR if you do not know the answer with certainty:
  DO NOT attempt to answer or explain the out-of-scope question.
  You MUST respond with EXACTLY and ONLY this sentence:
  "I can only assist with questions about Kahaanist jewelry, mythologies, and our policies. Please provide your email address so our founder can respond to you directly."`;

const EMAIL_REGEX = /([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})/i;

function extractUserMessage(fullPrompt) {
  if (!fullPrompt || typeof fullPrompt !== "string") return "";
  const parts = fullPrompt.split(/\nUser:\s*/i);
  if (parts.length > 1) {
    return parts[parts.length - 1].split(/\nGuide:/i)[0].trim();
  }
  return fullPrompt.trim();
}

function extractEmail(body, prompt) {
  if (body && typeof body.email === "string" && EMAIL_REGEX.test(body.email.trim())) {
    return body.email.trim();
  }
  if (typeof prompt === "string") {
    const match = prompt.match(EMAIL_REGEX);
    if (match) return match[1];
  }
  return null;
}

function logEmailCapture(email, prompt) {
  const captureLog = {
    event: "EMAIL_CAPTURE",
    email: email,
    prompt: prompt,
    timestamp: new Date().toISOString()
  };
  console.log(JSON.stringify(captureLog));
  console.log(`[EMAIL CAPTURED] Lead captured: ${email}`);
}

function isClearlyOutOfScope(userMessage) {
  if (!userMessage) return false;
  const lower = userMessage.toLowerCase().trim();

  // Explicit out-of-scope keywords & patterns
  const outOfScopePatterns = [
    /\b(python|javascript|typescript|c\+\+|java|html|css|sql|php|rust|golang|bash|powershell|c#)\b/i,
    /\b(write|create|generate|show)\s+(code|script|function|program|algorithm|class|regex|component)\b/i,
    /\b(capital of|president of|prime minister of|who is the current|population of)\b/i,
    /\b(solve|calculate|derivative|integral|\d+\s*[\+\*\/\^\-]\s*\d+)\b/i,
    /\b(weather in|forecast for|stock price|crypto|bitcoin|ethereum|nasdaq)\b/i,
    /\b(recipe for|how to cook|bake a cake|ingredients for)\b/i,
    /\b(movie review|tv show|football score|world cup|olympics|nba|ipl)\b/i,
    /\b(who won the|election|politics|democrat|republican|parliament)\b/i,
    /\b(tell me a joke|write a song|write an essay|translate this)\b/i
  ];

  for (const pattern of outOfScopePatterns) {
    if (pattern.test(lower)) {
      return true;
    }
  }
  return false;
}

function isFallbackResponse(reply) {
  if (!reply) return true;
  const lower = reply.toLowerCase();
  return (
    lower.includes("only assist with questions about kahaanist") ||
    lower.includes("provide your email") ||
    lower.includes("founder can respond") ||
    lower.includes("cannot assist with questions outside") ||
    lower.includes("out of scope")
  );
}

function getDirectPolicyMatch(userMessage) {
  if (!userMessage) return null;
  const lower = userMessage.toLowerCase();
  
  if (lower.includes("shipping") || lower.includes("delivery") || lower.includes("dispatch") || lower.includes("transit")) {
    return BRAND_POLICIES.shipping;
  }
  if (lower.includes("return") || lower.includes("exchange") || lower.includes("refund") || lower.includes("defect")) {
    return BRAND_POLICIES.returns;
  }
  if (lower.includes("material") || lower.includes("brass") || lower.includes("care") || lower.includes("tarnish") || lower.includes("clean") || lower.includes("patina")) {
    return BRAND_POLICIES.materials;
  }
  if (lower.includes("guarantee") || lower.includes("warranty")) {
    return BRAND_POLICIES.guarantees;
  }
  return null;
}

export default {
  async fetch(request, env, ctx) {
    const corsHeaders = {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
      "Content-Type": "application/json"
    };

    // Handle CORS preflight requests
    if (request.method === "OPTIONS") {
      return new Response(null, { headers: corsHeaders });
    }

    const url = new URL(request.url);

    // ----------------------------------------------------
    // NEW: Cloudflare Native Geo-IP Endpoint
    // ----------------------------------------------------
    if (request.method === "GET" && url.pathname === "/geo") {
      // CF-IPCountry is automatically injected by Cloudflare's network
      const countryCode = request.headers.get("CF-IPCountry") || "IN";
      return new Response(JSON.stringify({ country_code: countryCode }), { 
        headers: { ...corsHeaders, "Content-Type": "application/json", "Cache-Control": "no-store" } 
      });
    }

    // ----------------------------------------------------
    // NEW: Newsletter / Leads Subscribe Endpoint
    // ----------------------------------------------------
    if (request.method === "POST" && url.pathname === "/subscribe") {
      try {
        const body = await request.json();
        const email = body.email || "no-email";
        const phone = body.phone || "no-phone";
        
        // Save to KV Store with timestamp
        const timestamp = new Date().toISOString();
        const key = `lead_${timestamp}_${email}`;
        
        await env.KAHAANIST_LEADS.put(key, JSON.stringify({
          email: email,
          phone: phone,
          timestamp: timestamp,
          source: "join_modal"
        }));

        console.log(`[LEAD_CAPTURE] Saved new lead to KV database: ${email} | ${phone}`);

        // --- KLAVIYO INTEGRATION ---
        if (email !== "no-email") {
          ctx.waitUntil(
            fetch('https://a.klaviyo.com/client/subscriptions/?company_id=Vxi4aX', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json', 'revision': '2024-02-15' },
              body: JSON.stringify({
                data: {
                  type: "subscription",
                  attributes: { 
                    custom_source: "Website_Join_Modal", 
                    profile: { 
                      data: { 
                        type: "profile", 
                        attributes: { 
                          email: email,
                          ...(phone !== "no-phone" && { phone_number: phone })
                        } 
                      } 
                    } 
                  },
                  relationships: { list: { data: { type: "list", id: "XtyGg5" } } }
                }
              })
            }).catch(e => console.error("Klaviyo push failed:", e))
          );
        }

        return new Response(JSON.stringify({ success: true, message: "Welcome to the lore." }), { 
          headers: { ...corsHeaders, "Content-Type": "application/json" } 
        });
      } catch (err) {
        return new Response(JSON.stringify({ error: err.message }), { status: 500, headers: corsHeaders });
      }
    }

    if (request.method !== "POST") {
      return new Response(JSON.stringify({ error: "Method not allowed. Use GET /geo, or POST /chat or /subscribe" }), {
        status: 405,
        headers: corsHeaders
      });
    }

    let body = {};
    try {
      body = await request.json();
    } catch (e) {
      body = {};
    }

    const prompt = typeof body.prompt === "string" ? body.prompt : "";
    const userMessage = extractUserMessage(prompt);
    const capturedEmail = extractEmail(body, prompt);

    // 1. Email Capture & Structured Logging
    if (capturedEmail) {
      logEmailCapture(capturedEmail, prompt);

      // If the message is primarily submitting an email address, return confirmation immediately
      const strippedPrompt = prompt.replace(EMAIL_REGEX, "").trim().toLowerCase();
      const isEmailSubmissionOnly = 
        !prompt ||
        userMessage.trim() === capturedEmail ||
        strippedPrompt === "" ||
        strippedPrompt.includes("my email is") ||
        strippedPrompt.includes("here is my email") ||
        strippedPrompt.includes("email:");

      if (isEmailSubmissionOnly) {
        return new Response(JSON.stringify({
          response: `Thank you! We have captured your email (${capturedEmail}). Our founder will respond to you directly.`
        }), { headers: corsHeaders });
      }
    }

    if (!prompt && !capturedEmail) {
      return new Response(JSON.stringify({ error: "Missing prompt" }), {
        status: 400,
        headers: corsHeaders
      });
    }

    // 2. Pre-Check Anti-Hallucination Guardrail
    if (isClearlyOutOfScope(userMessage)) {
      return new Response(JSON.stringify({
        response: FALLBACK_RESPONSE
      }), { headers: corsHeaders });
    }

    // 3. Retrieve API Key
    const API_KEY = (env && (env.GEMINI_API_KEY || env.GEMINI_OMNI_API_KEY)) || "";
    
    // If no API key is available in environment, fallback to deterministic brand policy matching
    if (!API_KEY) {
      const directMatch = getDirectPolicyMatch(userMessage);
      if (directMatch) {
        return new Response(JSON.stringify({ response: directMatch }), { headers: corsHeaders });
      }
      return new Response(JSON.stringify({ response: FALLBACK_RESPONSE }), { headers: corsHeaders });
    }

    // 4. Query Gemini API with Candidate Models
    const CANDIDATE_MODELS = [
      "gemini-3.5-flash",
      "gemini-2.5-flash",
      "gemini-1.5-flash",
      "gemini-flash-latest"
    ];

    
      const userCountry = request.headers.get("CF-IPCountry") || "IN";
      const geminiPayload = {

      system_instruction: {
        parts: [{ text: SYSTEM_INSTRUCTION + "\n\nCRITICAL GEO-LOCATION INSTRUCTION:\nThe user's detected country code is: " + userCountry + ".\nIf country is 'IN', ONLY mention Domestic India Shipping (Free above Rs 2899) and NEVER mention International shipping or USD.\nIf country is NOT 'IN', ONLY mention International Shipping (Free above US $65) and NEVER mention India domestic shipping or INR." }]
      },
      contents: [
        {
          role: "user",
          parts: [{ text: prompt }]
        }
      ],
      generationConfig: {
        temperature: 0.2
      }
    };

    let reply = null;

    for (const model of CANDIDATE_MODELS) {
      try {
        const url = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${API_KEY}`;
        const apiResponse = await fetch(url, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(geminiPayload)
        });

        if (apiResponse.ok) {
          const data = await apiResponse.json();
          if (data.candidates && data.candidates.length > 0) {
            const rawText = data.candidates[0].content?.parts?.[0]?.text;
            if (rawText) {
              reply = rawText.trim();
              break; // Success
            }
          }
        }
      } catch (err) {
        // Try next candidate model
        continue;
      }
    }

    // 5. Post-Guardrail & Fallback Handling
    if (!reply) {
      // If Gemini was unreachable or failed, check deterministic policy match
      const directMatch = getDirectPolicyMatch(userMessage);
      reply = directMatch || FALLBACK_RESPONSE;
    } else if (isFallbackResponse(reply) || isClearlyOutOfScope(userMessage)) {
      reply = FALLBACK_RESPONSE;
    }

    return new Response(JSON.stringify({ response: reply }), {
      headers: corsHeaders
    });
  }
};






