#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import email

class EmailParser:
    def __init__(self, logger):
        """
        Initialize the email parser

        Args:
            logger: Logger instance to log events
        """
        self.logger = logger

    def extract_email_content(self, raw_email):
        """
        Extract content from a raw email

        Args:
            raw_email: The raw email to process

        Returns:
            dict: Dictionary containing email data

        Raises:
            Exception: If an error occurs during extraction
        """
        try:
            msg = email.message_from_string(raw_email)

            sender = msg['From']
            subject = msg['Subject'] or "No subject"
            recipient = msg['To']

            content = ""
            if msg.is_multipart():
                for part in msg.get_payload():
                    if part.get_content_type() == 'text/plain':
                        content += part.get_payload(decode=True).decode('utf-8', errors='ignore')
            else:
                content = msg.get_payload(decode=True).decode('utf-8', errors='ignore')

            content = content.strip()
            self.logger.log_message(f"From: {sender}, To: {recipient}, Subject: {subject}")
            self.logger.log_message(f"Content extracted: {content[:100]}...")

            return {
                'sender': sender,
                'subject': subject,
                'recipient': recipient,
                'content': content
            }
        except Exception as e:
            self.logger.log_message(f"ERROR extracting email: {str(e)}")
            raise e

    def is_no_reply_address(self, sender_email, assistants_config=None):
        """
        Check if the email address is a no-reply address or an assistant address

        Args:
            sender_email: The email address to check
            assistants_config: Assistants configuration (optional)

        Returns:
            bool: True if it's a no-reply or assistant address, False otherwise
        """
        sender_email = sender_email.lower()

        # Check if it's a standard no-reply address
        if 'noreply' in sender_email or 'no-reply' in sender_email or 'daemon' in sender_email:
            return True

        # Check if it's an assistant address
        if assistants_config:
            for assistant_name, config in assistants_config.items():
                if 'email' in config and 'sender' in config['email']:
                    assistant_email = config['email']['sender'].lower()
                    if sender_email == assistant_email:
                        return True

        return False

    def detect_assistant(self, email_data, assistants_config, default_assistant):
        """
        Detect the assistant to use based on email data

        Args:
            email_data: Email data
            assistants_config: Assistants configuration
            default_assistant: Name of the default assistant

        Returns:
            str: Name of the assistant to use
        """
        recipient_email = email_data['recipient'].lower()

        # Check each configured assistant
        for assistant_name in assistants_config:
            if assistant_name == "default":
                continue


            if assistant_name.lower() in recipient_email:
                self.logger.log_message(f"Detected assistant: {assistant_name}")
                return assistant_name

        self.logger.log_message(f"No specific assistant detected, using default: {default_assistant}")
        return default_assistant
