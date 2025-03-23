#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import uuid
import json
import requests
from datetime import datetime

class Logger:
    def __init__(self, config):
        """
        Initialize the logging system

        Args:
            config: Configuration containing logging parameters
        """
        self.log_file = config.get('General', 'log_file')
        self.raw_email_log = config.get('General', 'raw_email_log')
        self.temp_log_dir = config.get('General', 'temp_log_dir')
        self.discord_webhook_url = config.get('Discord', 'webhook_url', fallback=None)

        # Create a session ID and a temporary file path
        self.session_id = str(uuid.uuid4())
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.temp_log_filename = f"marechan_{timestamp}_{self.session_id}.txt"
        self.temp_log_path = os.path.join(self.temp_log_dir, self.temp_log_filename)

        # Ensure the temporary log directory exists
        os.makedirs(self.temp_log_dir, exist_ok=True)

        # Ensure the parent directory of the log files exists
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        os.makedirs(os.path.dirname(self.raw_email_log), exist_ok=True)

        self.log_message("Logger initialized")

    def log_message(self, message, temp_log=True):
        """
        Log a message to the log files

        Args:
            message: The message to log
            temp_log: If True, also log to the temporary file
        """
        log_entry = f"{datetime.now().isoformat()} - {message}\n"

        with open(self.log_file, "a") as log:
            log.write(log_entry)

        if temp_log:
            with open(self.temp_log_path, "a") as temp_log:
                temp_log.write(log_entry)

    def log_raw_email(self, raw_email):
        """
        Log a raw email to the log files

        Args:
            raw_email: The raw email to log
        """
        try:
            with open(self.raw_email_log, "a") as raw_log:
                raw_log.write("==== NEW EMAIL BEGIN ====\n")
                raw_log.write(raw_email)
                raw_log.write("\n==== EMAIL END ====\n\n")

            with open(self.temp_log_path, "a") as temp_log:
                temp_log.write("==== RAW EMAIL BEGIN ====\n")
                temp_log.write(raw_email)
                temp_log.write("\n==== RAW EMAIL END ====\n\n")

            self.log_message(f"Raw email logged to {self.raw_email_log} and temp log", temp_log=False)
        except Exception as e:
            self.log_message(f"ERROR logging raw email: {str(e)}")

    def send_log_to_discord(self, email_data, response_data, assistant_name):
        """
        Send a summary of the email processing to Discord

        Args:
            email_data: Data of the processed email
            response_data: Data of the sent response
            assistant_name: Name of the assistant that processed the email

        Returns:
            bool: True if sending was successful, False otherwise
        """
        try:
            self.log_message("Preparing to send log to Discord...")

            if not self.discord_webhook_url:
                self.log_message("Discord webhook not configured, sending ignored")
                return False

            files = {
                'file': (self.temp_log_filename, open(self.temp_log_path, 'rb'), 'text/plain')
            }

            sender_name = email_data.get('sender', 'Unknown')
            if '<' in sender_name:
                sender_name = sender_name.split('<')[0].strip()

            embed = {
                "title": f"New response from {assistant_name.capitalize()}",
                "description": f"{assistant_name.capitalize()} replied to an email from **{sender_name}**",
                "color": 0x2196F3,
                "fields": [
                    {
                        "name": "Subject",
                        "value": email_data.get('subject', 'No subject'),
                        "inline": True
                    },
                    {
                        "name": "Assistant",
                        "value": assistant_name.capitalize(),
                        "inline": True
                    },
                    {
                        "name": "Response",
                        "value": (response_data.get('message', '')[:250] + '...')
                                if len(response_data.get('message', '')) > 250
                                else response_data.get('message', 'No response')
                    }
                ],
                "timestamp": datetime.now().isoformat()
            }

            payload = {
                "content": f"📧 **New email processed by {assistant_name.capitalize()}** | {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
                "embeds": [embed],
            }

            response = requests.post(
                self.discord_webhook_url,
                data={"payload_json": json.dumps(payload)},
                files=files
            )

            if response.status_code == 200:
                self.log_message(f"Log successfully sent to Discord (Status: {response.status_code})")
                return True
            else:
                self.log_message(f"Error sending to Discord: Status {response.status_code}, Response: {response.text}")
                return False

        except Exception as e:
            self.log_message(f"ERROR in send_log_to_discord: {str(e)}")
            return False
