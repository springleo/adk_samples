# Gmail Assistant Agent

This is a secure agent built using the **Google Agent Development Kit (ADK)** that connects to your Gmail account to fetch, list, and summarize emails. It uses official Google OAuth2 authentication and the Gmail API.

Note: Educational use only, not built for production use

## Features

- **Fetch Emails:** Search by day range, sender, or keyword.
- **Summarize:** Intelligently summarize email content using Gemini 2.0 Flash.
- **Secure:** Uses `AuthenticatedFunctionTool` for official OAuth2 flows.

---

## 1. Prerequisites (Google Cloud Setup)

Before running the agent, you must set up an OAuth2 Client in the Google Cloud Console.

1.  **Create a Project:** Go to the [Google Cloud Console](https://console.cloud.google.com/) and create a new project.
2.  **Enable Gmail API:** Search for "Gmail API" in the Library and click **Enable**.
3.  **Configure OAuth Consent Screen:**
    - Set User Type to **External**.
    - Add your email as a **Test User**.
    - Add the scope: `https://www.googleapis.com/auth/gmail.readonly`.
4.  **Create Credentials:**
    - Go to **Credentials** > **Create Credentials** > **OAuth client ID**.
    - Select **Web Application**.
    - Add `http://localhost:8000/auth/callback` to the **Authorized redirect URIs**.
5.  **Save Credentials:** Copy your **Client ID** and **Client Secret**.

---

## 2. Local Setup

### macOS / Linux

1.  **Clone the repository** (or navigate to the directory).
2.  **Create a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configure Environment Variables:**
    - Copy `.env.example` to `.env`.
    - Fill in your `OAUTH_CLIENT_ID` and `OAUTH_CLIENT_SECRET`.

### Windows

1.  **Open PowerShell.**
2.  **Create a virtual environment:**
    ```powershell
    python -m venv venv
    .\venv\Scripts\Activate.ps1
    ```
3.  **Install dependencies:**
    ```powershell
    pip install -r requirements.txt
    ```
4.  **Configure Environment Variables:**
    - Copy `.env.example` to `.env`.
    - Fill in your `OAUTH_CLIENT_ID` and `OAUTH_CLIENT_SECRET`.

---

## 3. Running the Agent

You can run the agent using the ADK CLI:

```bash
adk web agents/gmail_bot/agent.py
```

- This will start a local web server at `http://localhost:8000`.
- Open your browser to that address.
- When you first try to use a Gmail tool, the agent will redirect you to the official Google login screen to authorize access.

---

## 4. Usage Examples

- "What emails did I receive yesterday?"
- "Find emails from 'john.doe@example.com' about the project."
- "Summarize the last 5 emails I received today."
- "Show me emails containing the keyword 'invoice' from the last 7 days."

---

## 5. Security Note

This agent uses the official Google Python Client and ADK's secure credential handling. Your access tokens are stored locally and are never shared with any third party. Only the `gmail.readonly` scope is used, ensuring the agent cannot send or delete emails.
