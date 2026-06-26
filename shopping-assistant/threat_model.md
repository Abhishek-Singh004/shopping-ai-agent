# STRIDE Threat Model Assessment - Shopping Assistant Agent

This document presents a systematic threat modeling assessment of the `shopping-assistant` agent's codebase and architecture based on the **STRIDE** methodology.

---

## 1. System Boundaries & Data Flow

* **Entry Points**:
  * **FastAPI App (`app/fast_api_app.py`)**: Exposes REST API endpoints for clients to interact with the agent.
  * **User Prompt Interface**: Standard chat session interface via the ADK `App` container.
* **Core Logic**:
  * **`LlmAgent` (`retail_shopping_assistant`)**: Orchestrates responses and routes tasks.
  * **`CustomGemini` Model**: Custom LLM client powered by Google AI Studio (configured with a simulated API key).
* **Data Storage Layer**:
  * **In-Memory Store (`app/tools.py`)**: Tracks registered user IDs (`REGISTERED_USERS`) and discount redemption states (`DISCOUNT_CODES`).

---

## 2. STRIDE Evaluation

### 👤 Spoofing (Identity Spoofing)
* **Risk**: The `redeem_discount_code` tool receives `user_id` as an input parameter supplied by the model based on user chat input.
* **Vulnerability**: There is no validation or cryptographic check verifying that the user interacting with the chat session actually owns or is authenticated as the supplied `user_id`. A user can type *"Redeem WELCOME50 for user_abhishek"* and impersonate another customer.
* **Mitigation**: Bind the authenticated user ID directly to the connection session metadata or context, rather than extracting it from the model's natural language parameters.

### ✍️ Tampering (Data Tampering)
* **Risk**: Modifying application configuration or the discount code database.
* **Vulnerability**:
  * **In-Memory State Reset**: Since the redemption status is stored in a mutable Python dictionary, restarting the application process clears all redemption logs, allowing codes to be re-redeemed.
  * **Unauthorized Redemption**: Due to spoofing, users can arbitrarily mark other customers' codes as redeemed.
* **Mitigation**: Move the database of discount codes and redemptions to a persistent, secure data store (e.g., Cloud SQL or Firestore) with row-level access controls.

### 📝 Repudiation
* **Risk**: A user claims they did not redeem a code, or a code is marked as redeemed but there is no audit log.
* **Vulnerability**: The current tool only updates an in-memory dictionary. There is no immutable transaction log, audit trail, or external logging system recording the timestamp, caller IP, and authentication token of the redemption.
* **Mitigation**: Log all successful and failed redemptions to a secure, write-only audit trail (e.g., Cloud Logging) with structured log payloads.

### 🔓 Information Disclosure (Privacy & Data Leakage)
* **Risk**: Leakage of API keys, internal credentials, or user information.
* **Vulnerability**:
  * **Hardcoded API Key**: The simulated API key `AIzaSyD-mock-key-value-12345` is hardcoded directly inside `app/agent.py`. This is easily discoverable in source code repositories.
  * **User Leakage**: When a code has already been redeemed, the tool returns the message `f"Discount code '{code_upper}' has already been redeemed by user '{code_data['user_id']}'"`. This discloses the user ID of other customers.
* **Mitigation**:
  * Store secrets in a secure manager (e.g., Google Cloud Secret Manager) and load them via environment variables.
  * Sanitize error and success messages returned to the user to prevent disclosing user IDs or system internals.

### 💥 Denial of Service (DoS)
* **Risk**: Exhausting LLM quotas, API keys, or web server capacity.
* **Vulnerability**: There is no rate-limiting or query cost estimation on the FastAPI endpoints or tool invocations. A malicious actor could spam requests to the agent, exhausting the Gemini API quota and locking out legitimate users.
* **Mitigation**: Implement rate limiters on the FastAPI endpoints (e.g., slowapi) and restrict tool executions per user session.

### 🔑 Elevation of Privilege
* **Risk**: Unauthenticated callers executing privileged actions.
* **Vulnerability**: The FastAPI endpoints are currently unprotected and accept requests from any caller. Any client can trigger the LLM to invoke the `redeem_discount_code` tool.
* **Mitigation**: Implement authentication (e.g., OAuth 2.0 or JWT validation) on the FastAPI endpoints and restrict tool access based on user roles.
