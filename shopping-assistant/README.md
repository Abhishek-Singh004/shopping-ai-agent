# 🚀 Vibecoded: Shopping Assistant AI Agent

> **"Built on pure vibes, guided by intelligence, secured by default."**
>
> This agent project was crafted as part of **Kaggle's 5-Day AI Agents: Intensive Vibe Coding Course with Google**. It represents the future of rapid, agentic software engineering—where developer intent meets powerful AI-driven orchestration to build secure, modular applications in record time.

---

Welcome to the **Vibecoded Shopping Assistant**, a state-of-the-art AI retail companion engineered with the **Agent Development Kit (ADK) 2.0** framework. This intelligent agent is designed to navigate customer inquiries, assist with shopping, and securely process single-use promotional codes using a hardened, secure-by-default execution pipeline.

---

## 🗺️ Agent Structure Graph

The diagram below outlines the runtime architecture, session boundaries, and data flow of the `shopping-assistant` agent:

```mermaid
graph TD
    User([User Client / Browser]) <-->|Chat API (REST / SSE)| FastAPI[FastAPI Server / Playground]

    subgraph ADK App Container [App Runtime: 'app']
        FastAPI <-->|Session State & History| Runner[App Runner]
        Runner <-->|Inference Payload| Agent[LlmAgent: 'retail_shopping_assistant']

        subgraph Model Connection
            Agent <-->|Cached Property Client| CustomGemini[CustomGemini Model Class]
            CustomGemini <-->|HTTP / Websocket| API[Gemini Developer API / AI Studio]
        end

        subgraph Tool Execution
            Agent <-->|Execute Function| Tool[Tool: 'redeem_discount_code']
            Tool <-->|Validate & Mutate| Store[(In-Memory Database)]
        end
    end

    subgraph Custom Guardrails
        ShellHook[PreToolUse Hook] -.->|Intercepts run_command| Validator[validate_tool_call.py]
    end
```

---

## 🌟 Key Features & Implementation Details

### 🛒 1. AI Retail Shopping Assistant
* **Agent Definition**: Declared as `retail_shopping_assistant` (`LlmAgent`) in [agent.py](file:///d:/Download%20Manager/Antigravity/AI%20shopping%20assistant/secure-agent-lab/shopping-assistant/app/agent.py).
* **System Instructions**: Configured with a detailed prompt defining its persona. It helps customers browse products, answer questions, and directs them to supply their **registered User ID** alongside their code for discount redemptions.

### 🛡️ 2. Secure Discount Code Redemption Tool
* **Function Definition**: Implemented in [tools.py](file:///d:/Download%20Manager/Antigravity/AI%20shopping%20assistant/secure-agent-lab/shopping-assistant/app/tools.py) as `redeem_discount_code(user_id: str, code: str)`.
* **State Verification**:
  * **User Authentication**: Compares the input `user_id` against a set of registered users (`REGISTERED_USERS = {"user123", "user_abhishek", "customer_prime", "retail_buyer"}`).
  * **Code Validity Check**: Ensures the code matches recognized variants (`WELCOME50`, `SUMMER20`).
  * **Single-Use Guard**: Evaluates the `redeemed` boolean in the global database dictionary `DISCOUNT_CODES`. If already `True`, the tool rejects the redemption, returning an error payload describing who redeemed it and when.
  * **Normalization**: The code argument is automatically stripped of whitespaces and capitalized (case-insensitive checking).

### 🔒 3. Simulated API Key & Gating
* **Subclassed model**: `CustomGemini` subclasses the base `Gemini` ADK model class. It overrides `api_client` and `_live_api_client` to inject the simulated hardcoded API key:
  ```python
  api_key = os.environ.get("GEMINI_API_KEY") or "AIzaSyD-mock-key-value-12345"
  ```
* **Purpose**: This creates a deliberate secret signature `"AIzaSyD..."` in the codebase to test pre-commit/Semgrep secret rules.
* **Fallback**: When the playground starts, it checks for a real `GEMINI_API_KEY` environment variable. If found, it uses the real key for inference calls, ensuring the playground operates correctly.

---

## 🔐 Custom Security Policies & Hooks

### 📜 I. Secure Coding Standards (`.agents/CONTEXT.md`)
Defines the local paved roads for developers:
1. **Tool Input Validation**: All parameters must use type hints and Pydantic schemas.
2. **No Shell Execution**: Explicitly forbids executing raw shell commands (`run_command`) unless audited and allowed.
3. **Pre-Commit Remediation Loop**: Mandates fixing any secret scans or formatting warnings immediately before committing.
4. **TDD Planning Gate**: Mandates designing a **Security Boundaries & Assertions** section outlining edge cases for every implementation phase.

### 🛠️ II. Pre-Tool Interceptor Hook (`.agents/hooks.json`)
Registers a `PreToolUse` hook targeting the `run_command` tool. When the model attempts to invoke a shell command, the ADK runner intercepts it, redirects execution to `validate_tool_call.py`, and enforces a **10-second timeout**.

### 🛑 III. Command Validator Script (`.agents/scripts/validate_tool_call.py`)
Parses execution arguments from stdin (supporting raw text and JSON formats). It runs regex matching against destructive command patterns:
* Blocks forced recursive removals (`rm -rf` / `rm -fr`).
* Blocks command if matching patterns are found and exits with status code `1`, preventing tool execution.

### 🤖 IV. Git Pre-Commit Security Checks (`.pre-commit-config.yaml`)
Automates static analysis checking on git commit:
* **Pre-commit-hooks**: Fixes trailing whitespaces and missing end-of-files.
* **Semgrep**: Runs a local scan referencing [rules.yaml](file:///d:/Download%20Manager/Antigravity/AI%20shopping%20assistant/secure-agent-lab/shopping-assistant/.semgrep/rules.yaml) which uses regex matching (`AIzaSy[A-Za-z0-9_\-]*`) to block code commits containing hardcoded Google API keys.

---

## 🚀 Development & Test Commands

### Dependencies & Setup
Install packages:
```bash
agents-cli install
```

### Run Security Test Suite
```bash
uv run pytest tests/test_agent.py
```
This tests:
1. Successful code redemption.
2. Double-redemption blocks.
3. Unregistered user rejection.
4. Invalid code rejection.
5. Case-insensitivity and whitespace stripping.

### Start local playground
```bash
agents-cli playground
```
Interface URL: [http://127.0.0.1:8080/dev-ui/?app=app](http://127.0.0.1:8080/dev-ui/?app=app)
