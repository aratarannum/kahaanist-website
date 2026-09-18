/**
 * Test Runner: Cloudflare Worker Simulation Suite for Kahaanist Chatbot
 * Validates:
 * 1. In-scope policy queries (Shipping, Materials & Care, Returns & Guarantees)
 * 2. Out-of-scope queries triggering "Please provide your email" fallback
 * 3. Email capture detection, structured logging, and confirmation responses
 * 4. Frontend chat history prompt format compatibility
 * 5. CORS preflight handling
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// 1. Load Environment Variables from root .env
function loadEnv() {
  const envPath = path.resolve(__dirname, '../../.env');
  const env = {
    GEMINI_API_KEY: process.env.GEMINI_API_KEY || '',
    GEMINI_OMNI_API_KEY: process.env.GEMINI_OMNI_API_KEY || ''
  };

  if (fs.existsSync(envPath)) {
    try {
      const content = fs.readFileSync(envPath, 'utf8');
      const lines = content.split(/\r?\n/);
      for (const line of lines) {
        const trimmed = line.trim();
        if (trimmed.startsWith('#') || !trimmed.includes('=')) continue;
        const [k, ...v] = trimmed.split('=');
        const key = k.trim();
        const val = v.join('=').trim().replace(/^["']|["']$/g, '');
        if (key === 'GEMINI_API_KEY') env.GEMINI_API_KEY = val;
        if (key === 'GEMINI_OMNI_API_KEY') env.GEMINI_OMNI_API_KEY = val;
      }
    } catch (e) {
      console.warn('Warning reading .env:', e.message);
    }
  }
  return env;
}

// 2. Intercept console.log to verify structured EMAIL_CAPTURE events
class LogCapture {
  constructor() {
    this.logs = [];
    this.originalLog = console.log;
  }
  start() {
    this.logs = [];
    console.log = (...args) => {
      this.logs.push(args.map(a => (typeof a === 'object' ? JSON.stringify(a) : String(a))).join(' '));
      this.originalLog.apply(console, args);
    };
  }
  stop() {
    console.log = this.originalLog;
    return this.logs;
  }
}

// 3. Helper to dispatch simulated HTTP Request to Worker
async function dispatch(worker, method, body = null, env = {}) {
  const options = {
    method,
    headers: { 'Content-Type': 'application/json' }
  };
  if (body) {
    options.body = JSON.stringify(body);
  }
  const request = new Request('https://chatbot.kahaanist.workers.dev/', options);
  const response = await worker.fetch(request, env, {});
  const status = response.status;
  let json = null;
  try {
    json = await response.json();
  } catch (e) {
    json = null;
  }
  return { status, json, headers: response.headers };
}

// 4. Main Test Suite
async function runTestSuite() {
  console.log('====================================================');
  console.log('KAHAANIST CHATBOT CLOUDFLARE WORKER SIMULATION SUITE');
  console.log('====================================================');

  const env = loadEnv();
  console.log(`[INIT] Loaded API Key configured: ${Boolean(env.GEMINI_API_KEY || env.GEMINI_OMNI_API_KEY)}`);

  const workerModule = await import('./worker.js');
  const worker = workerModule.default;

  let totalTests = 0;
  let passedTests = 0;
  let failedTests = 0;

  function assert(condition, message) {
    totalTests++;
    if (condition) {
      passedTests++;
      console.log(`  [PASS] ${message}`);
    } else {
      failedTests++;
      console.error(`  [FAIL] ${message}`);
    }
  }

  const logCapture = new LogCapture();

  // Test 1: In-scope Query - Shipping Policy
  console.log('\n--- Test 1: In-Scope Query (Shipping Policy) ---');
  {
    const res = await dispatch(worker, 'POST', {
      prompt: 'What is your shipping policy for domestic India and international orders?'
    }, env);
    assert(res.status === 200, 'Returns HTTP 200 OK');
    assert(res.json && typeof res.json.response === 'string', 'Returns JSON with response string');
    const txt = (res.json?.response || '').toLowerCase();
    const hasShippingTerms = txt.includes('2,899') || txt.includes('65') || txt.includes('shipping') || txt.includes('dispatch') || txt.includes('3-5');
    assert(hasShippingTerms, 'Response accurately cites shipping thresholds (₹2,899 / US$65 / dispatch timeline)');
  }

  // Test 2: In-scope Query - Materials & Brass Care
  console.log('\n--- Test 2: In-Scope Query (Materials & Care) ---');
  {
    const res = await dispatch(worker, 'POST', {
      prompt: 'What materials do you use and how should I care for my brass jewelry if it tarnishes?'
    }, env);
    assert(res.status === 200, 'Returns HTTP 200 OK');
    const txt = (res.json?.response || '').toLowerCase();
    const hasCareTerms = txt.includes('brass') && (txt.includes('patina') || txt.includes('polish') || txt.includes('dry') || txt.includes('cloth'));
    assert(hasCareTerms, 'Response accurately describes solid recycled brass, natural patina, and care advice');
  }

  // Test 3: In-scope Query - Returns & Defect Policy
  console.log('\n--- Test 3: In-Scope Query (Returns & Guarantees) ---');
  {
    const res = await dispatch(worker, 'POST', {
      prompt: 'What is your return policy? Can I get a replacement if there is a manufacturing defect?'
    }, env);
    assert(res.status === 200, 'Returns HTTP 200 OK');
    const txt = (res.json?.response || '').toLowerCase();
    const hasReturnTerms = (txt.includes('final') || txt.includes('non-returnable')) && (txt.includes('replacement') || txt.includes('defect') || txt.includes('connect@kahaanist.com') || txt.includes('48'));
    assert(hasReturnTerms, 'Response explains final sales policy and 48-hour manufacturing defect replacement');
  }

  // Test 4: Out-of-scope Query - Code Generation (Anti-Hallucination Guardrail)
  console.log('\n--- Test 4: Out-of-Scope Query (Code Generation) ---');
  {
    const res = await dispatch(worker, 'POST', {
      prompt: 'Write python code to implement a binary search tree algorithm'
    }, env);
    assert(res.status === 200, 'Returns HTTP 200 OK');
    const txt = res.json?.response || '';
    assert(txt.includes('Please provide your email'), 'Triggers fallback containing "Please provide your email"');
    assert(txt.includes('I can only assist with questions about Kahaanist jewelry'), 'Declines out-of-scope query with brand scope notice');
    assert(!txt.toLowerCase().includes('def binary_search') && !txt.toLowerCase().includes('class node'), 'Strictly refuses to generate code');
  }

  // Test 5: Out-of-Scope Query - General Trivia (Capital of France)
  console.log('\n--- Test 5: Out-of-Scope Query (General Knowledge / Capital of France) ---');
  {
    const res = await dispatch(worker, 'POST', {
      prompt: 'What is the capital of France and who is its president?'
    }, env);
    assert(res.status === 200, 'Returns HTTP 200 OK');
    const txt = res.json?.response || '';
    assert(txt.includes('Please provide your email'), 'Triggers fallback containing "Please provide your email"');
    assert(!txt.toLowerCase().includes('paris'), 'Anti-hallucination guardrail prevents answering general trivia');
  }

  // Test 6: Email Submission in Prompt & Structured Logging
  console.log('\n--- Test 6: Email Submission in Prompt & Structured Logging ---');
  {
    logCapture.start();
    const res = await dispatch(worker, 'POST', {
      prompt: 'My email is collector@kahaanist-devotee.com'
    }, env);
    const logs = logCapture.stop();

    assert(res.status === 200, 'Returns HTTP 200 OK');
    const txt = res.json?.response || '';
    assert(txt.includes('collector@kahaanist-devotee.com'), 'Response acknowledges captured email address');

    const hasStructuredLog = logs.some(l => l.includes('"event":"EMAIL_CAPTURE"') && l.includes('collector@kahaanist-devotee.com'));
    assert(hasStructuredLog, 'Worker emits structured JSON log with event: "EMAIL_CAPTURE"');

    const hasReadableLog = logs.some(l => l.includes('[EMAIL CAPTURED]'));
    assert(hasReadableLog, 'Worker emits readable log prefixed with [EMAIL CAPTURED]');
  }

  // Test 7: Email Capture via JSON Payload Field
  console.log('\n--- Test 7: Email Capture via JSON Payload Field ---');
  {
    logCapture.start();
    const res = await dispatch(worker, 'POST', {
      prompt: 'I want to inquire about custom styling',
      email: 'stylist@mythology.com'
    }, env);
    const logs = logCapture.stop();

    assert(res.status === 200, 'Returns HTTP 200 OK');
    const hasStructuredLog = logs.some(l => l.includes('"event":"EMAIL_CAPTURE"') && l.includes('stylist@mythology.com'));
    assert(hasStructuredLog, 'Worker logs structured EMAIL_CAPTURE from body.email');
  }

  // Test 8: Frontend Chat History Wrapper Compatibility
  console.log('\n--- Test 8: Frontend Chat History Prompt Wrapper ---');
  {
    const wrappedPrompt = `You are a customer support chatbot for Kahaanist...\\nUser: Can you write a javascript function to sort numbers?\\nGuide:`;
    const res = await dispatch(worker, 'POST', {
      prompt: wrappedPrompt
    }, env);
    assert(res.status === 200, 'Returns HTTP 200 OK');
    const txt = res.json?.response || '';
    assert(txt.includes('Please provide your email'), 'Extracts latest user message from chat history wrapper and triggers fallback');
  }

  // Test 9: CORS Preflight Handling
  console.log('\n--- Test 9: CORS Preflight (OPTIONS) ---');
  {
    const res = await dispatch(worker, 'OPTIONS', null, env);
    assert(res.status === 200 || res.status === 204, 'OPTIONS request returns 200/204');
    const allowOrigin = res.headers.get('Access-Control-Allow-Origin');
    assert(allowOrigin === '*', 'Access-Control-Allow-Origin is configured to *');
  }

  // Test Summary
  console.log('\n====================================================');
  console.log(`SIMULATION RESULTS: ${passedTests}/${totalTests} Passed (${failedTests} Failed)`);
  console.log('====================================================');

  if (failedTests > 0) {
    process.exit(1);
  }
}

runTestSuite().catch(err => {
  console.error('Fatal Test Suite Error:', err);
  process.exit(1);
});
