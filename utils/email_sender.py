#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate

class EmailSender:
    def __init__(self, logger):
        """
        Initialize the email sender

        Args:
            logger: Logger instance to log events
        """
        self.logger = logger

    def send_response(self, to_email, original_subject, response_data, assistant_config, html_formatter):
        """
        Send a response via email

        Args:
            to_email: Recipient's email address
            original_subject: Original subject of the email
            response_data: Response data
            assistant_config: Assistant configuration
            html_formatter: HTML formatter to create the email content

        Returns:
            bool: True if the email was sent successfully, False otherwise
        """
        try:
            email_config = assistant_config.get('email', {})
            sender_email = email_config.get('sender', 'no_sender_found@douxx.tech')

            subject = f"Re: {original_subject}" if original_subject else "Automatic response"

            html_content = html_formatter.create_html_response(response_data, assistant_config)

            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = sender_email
            msg['To'] = to_email
            msg['Date'] = formatdate(localtime=True)

            text_part = MIMEText(response_data['message'], 'plain')
            msg.attach(text_part)

            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)

            smtp_server = email_config.get('smtp_server', 'localhost')
            smtp_port = email_config.get('smtp_port', 587)
            smtp_user = email_config.get('smtp_user', '')
            smtp_password = email_config.get('smtp_password', '')

            if smtp_port == 465:
                smtp = smtplib.SMTP_SSL(smtp_server, smtp_port)
            else:
                smtp = smtplib.SMTP(smtp_server, smtp_port)
                if smtp_port == 587:  # Use STARTTLS for port 587
                    smtp.starttls()

            if smtp_user and smtp_password:
                smtp.login(smtp_user, smtp_password)

            smtp.send_message(msg)
            smtp.quit()

            self.logger.log_message(f"Response sent successfully to {to_email}")
            return True

        except Exception as e:
            self.logger.log_message(f"ERROR in send_response: {str(e)}")
            return False
