# Tenexity Email Agent Setup

This agent allows you to create topics by forwarding emails and receive daily summaries.

## Prerequisites
- Python 3.8+
- An email account (Gmail with App Password recommended)
- An AI API Key (Anthropic or OpenAI)
- Supabase Project credentials

## Setup

1. **Install Dependencies**:
   ```bash
   pip install supabase
   # If you use OpenAI: pip install openai
   # If you use Anthropic: pip install anthropic
   ```

2. **Configure Credentials**:
   Edit `agent_config.py` in this directory:
   - Fill in your `EMAIL_USER` and `EMAIL_PASSWORD`.
   - Set your `AI_API_KEY`.
   - Set your `SUPABASE_URL` and `SUPABASE_KEY`.

3. **Run the Agent**:
   ```bash
   python3 tenexity_agent.py
   ```
   Keep this script running (e.g., in a terminal window or screen session). It checks for emails every minute.

## Usage

### Inbound (Create Topic)
Forward an email to the account you configured. The agent will:
1.  Read the email.
2.  Use AI to extract the Title, Facts, and Opinions.
3.  Create a "Suggested" topic on your board.
4.  You can then "Approve" or "Reject" it in the app.

### Outbound (Daily Summary)
The agent is configured to send summaries. (Currently stubbed in the script, customize `send_summary()` in `tenexity_agent.py` to set the exact schedule).
