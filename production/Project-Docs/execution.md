# Project Execution & Maintenance SOP (Standard Operating Procedure)

This document dictates how technical modifications are made to the Kahaanist website to ensure zero downtime and prevent "silent failures" (where a script fails to update code, but pushes successfully anyway).

## 1. The "Silent Failure" Rule
All Python or Node.js scripts used to modify `index.html` MUST include a strict validation check. If a string replacement or regex fails to find its target, the script MUST throw a fatal error (e.g., `sys.exit(1)`) to immediately halt the deployment pipeline.

## 2. The Test Suite Pipeline
Before any `git push` is executed, `node test_suite.js` must run. 
We have upgraded the test suite to not only check for syntax errors, but also to structurally validate that critical UI elements (like the Shopify Buy Button SDK and the Video Gallery logic) still exist in the DOM string.

## 3. The "Visual State" Rule
Because we are headless, any structural UI change (like injecting banners or moving buttons) CANNOT be tested "mentally." Before deployment, the agent MUST write and execute a temporary local script (using Puppeteer, Playwright, or Selenium + Chrome) to capture a screenshot of `index.html`. The agent must then use its `view_file` tool to physically look at the generated image and verify there are no overlapping elements (e.g., fixed headers covering content) before pushing live.

## 4. The "Customer Ready" Rule
NEVER publish or commit features that are not fully customer-ready. For example, do not embed client-side code that fetches from localhost (like local LLMs) as this will fail on a customer's device. If a feature has blockers preventing it from being customer-ready, it must be disabled or kept in a branch. You must explicitly list the blockers and resolve them with the user through direction and approvals before pushing to production.
