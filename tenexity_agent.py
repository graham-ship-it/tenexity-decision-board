import time
import imaplib
import smtplib
import email
import json
import logging
from email.header import decode_header
import agent_config

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class TenexityAgent:
    def __init__(self):
        self.imap = None
        self.ai_client = None
        self.supabase = None
        
        # Load config
        self.email_user = agent_config.EMAIL_USER
        self.email_pass = agent_config.EMAIL_PASSWORD
        self.imap_host = agent_config.EMAIL_HOST
        
        self.setup_ai()
        self.setup_supabase()

    def setup_ai(self):
        """Initialize AI client (Anthropic or OpenAI)"""
        try:
            if agent_config.AI_PROVIDER == 'anthropic':
                # import anthropic
                # self.ai_client = anthropic.Anthropic(api_key=agent_config.AI_API_KEY)
                logging.info("Anthropic client stub initialized")
            else:
                # import openai
                # self.ai_client = openai.OpenAI(api_key=agent_config.AI_API_KEY)
                logging.info("OpenAI client stub initialized")
        except Exception as e:
            logging.error(f"Failed to setup AI client: {e}")

    def setup_supabase(self):
        """Initialize Supabase client"""
        try:
            from supabase import create_client, Client
            self.supabase: Client = create_client(
                agent_config.SUPABASE_URL, 
                agent_config.SUPABASE_KEY
            )
            logging.info("Supabase client initialized")
        except ImportError:
            logging.warning("supabase-py not installed. Run `pip install supabase`")
        except Exception as e:
            logging.error(f"Failed to setup Supabase: {e}")

    def connect_imap(self):
        """Connect to IMAP server"""
        try:
            self.imap = imaplib.IMAP4_SSL(self.imap_host)
            self.imap.login(self.email_user, self.email_pass)
            logging.info(f"Connected to IMAP as {self.email_user}")
        except Exception as e:
            logging.error(f"IMAP connection failed: {e}")
            self.imap = None

    def parse_email_with_ai(self, subject, body):
        """
        Uses LLM to extract structured data from email.
        Expected JSON output:
        {
            "title": "Topic Title",
            "description": "Topic Description",
            "facts": ["Fact 1", "Fact 2"],
            "opinions": ["Opinion 1"],
            "preferences": ["Preference 1"]
        }
        """
        prompt = f"""
        You are an AI assistant for a Decision Board. 
        Parse the following email into a new Topic request.
        
        Email Subject: {subject}
        Email Body: 
        {body}
        
        Return strictly valid JSON with the following fields:
        - title (string): A concise title for the topic
        - description (string): A summary of the issue
        - facts (array of strings): Objection facts mentioned
        - opinions (array of strings): Subjective opinions mentioned
        - preferences (array of strings): Stated preferences

        JSON:
        """
        
        # MOCK RESPONSE FOR TESTING
        logging.info("Simulating AI extraction...")
        import uuid
        mock_id = str(uuid.uuid4())[:8]
        return {
            "title": f"New Topic from Email {mock_id}",
            "description": f"Extracted from subject: {subject}",
            "facts": ["Extracted fact 1", "Extracted fact 2"],
            "opinions": ["Extracted opinion 1"],
            "preferences": []
        }
        
        # REAL IMPLEMENTATION WOULD CALL API HERE
        # response = self.ai_client.messages.create(...)
        # return json.loads(response.content)

    def process_inbox(self):
        """Check for new emails and process them"""
        if not self.imap:
            self.connect_imap()
            if not self.imap: return

        try:
            self.imap.select(agent_config.EMAIL_FOLDER)
            # Search for UNSEEN emails
            status, messages = self.imap.search(None, 'UNSEEN')
            
            if status != 'OK':
                return

            email_ids = messages[0].split()
            if not email_ids:
                return

            logging.info(f"Found {len(email_ids)} new emails")

            for e_id in email_ids:
                # Fetch email
                _, msg_data = self.imap.fetch(e_id, '(RFC822)')
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        subject, encoding = decode_header(msg["Subject"])[0]
                        if isinstance(subject, bytes):
                            subject = subject.decode(encoding or 'utf-8')
                        
                        sender = msg.get("From")
                        logging.info(f"Processing email from {sender}: {subject}")

                        # Get body
                        if msg.is_multipart():
                            for part in msg.walk():
                                if part.get_content_type() == "text/plain":
                                    body = part.get_payload(decode=True).decode()
                                    break
                        else:
                            body = msg.get_payload(decode=True).decode()

                        # Parse with AI
                        topic_data = self.parse_email_with_ai(subject, body)
                        
                        # Save to Supabase
                        self.save_topic(topic_data, sender)

        except Exception as e:
            logging.error(f"Error processing inbox: {e}")

    def save_topic(self, data, sender):
        """Save the parsed topic to Supabase"""
        if not self.supabase:
            logging.warning("Supabase not connected. Skipping save.")
            return

        try:
            # 1. Insert Topic
            topic_payload = {
                "title": data['title'],
                "description": data['description'],
                "status": "suggested", # New status
                "created_by": "email-agent", # Or map sender to user ID
                # "board_id": BOARD_ID # We need to know which board!
            }
            
            # Note: In a real app we need to resolve the Board ID.
            # For now we'll assume a single board or configured board ID
            # res = self.supabase.table('topics').insert(topic_payload).execute()
            
            logging.info(f"Saved topic: {data['title']}")
            
            # 2. Insert Facts/Opinions as Contributions
            # ... implementation ...

        except Exception as e:
            logging.error(f"Failed to save topic: {e}")

    def run(self):
        """Main loop"""
        logging.info("Tenexity Email Agent started...")
        while True:
            self.process_inbox()
            time.sleep(60) # Poll every minute

if __name__ == "__main__":
    agent = TenexityAgent()
    agent.run()
