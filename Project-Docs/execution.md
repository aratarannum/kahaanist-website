# Project Execution & Maintenance SOP (Standard Operating Procedure)

This document dictates how technical modifications are made to the Kahaanist website to ensure zero downtime and prevent "silent failures" (where a script fails to update code, but pushes successfully anyway).

## 1. The "Silent Failure" Rule
All Python or Node.js scripts used to modify `index.html` MUST include a strict validation check. If a string replacement or regex fails to find its target, the script MUST throw a fatal error (e.g., `sys.exit(1)`) to immediately halt the deployment pipeline.

## 2. The Test Suite Pipeline
Before any `git push` is executed, `node test_suite.js` must run. 
We have upgraded the test suite to not only check for syntax errors, but also to structurally validate that critical UI elements (like the Shopify Buy Button SDK and the Video Gallery logic) still exist in the DOM string.

## 3. The "Visual State" Rule
Because we are headless, any structural UI change (like moving the Add to Cart button or altering the video gallery) must be tested on both Mobile and Desktop viewports mentally by the AI before deployment. Mobile-first stacking (where videos push buttons below the fold) must always be accounted for.
