#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import json
import configparser

from utils.logger import Logger
from utils.email_parser import EmailParser
from utils.ai_client import AIClient
from utils.prompt_enhancer import PromptEnhancer
from utils.response_formatter import ResponseFormatter
from utils.email_sender import EmailSender

def get_script_directory():
    """
    Get the directory of the current script

    Returns:
        str: Directory path of the current script
    """
    return os.path.dirname(os.path.abspath(__file__))

def load_config():
    """
    Load configuration from the config.conf file

    Returns:
        configparser.ConfigParser: Configuration object
    """
    config = configparser.ConfigParser()
    script_dir = get_script_directory()
    config_path = os.path.join(script_dir, 'config.conf')

    if not os.path.exists(config_path):
        print(f"Configuration file 'config.conf' not found at {config_path}!")
        sys.exit(1)

    config.read(config_path)
    return config

def load_assistants():
    """
    Load assistants configuration from the assistants.json file

    Returns:
        dict: Assistants configuration
    """
    script_dir = get_script_directory()
    assistants_path = os.path.join(script_dir, 'assistants.json')

    if not os.path.exists(assistants_path):
        print(f"Assistants configuration file 'assistants.json' not found at {assistants_path}!")
        sys.exit(1)

    with open(assistants_path, 'r') as file:
        return json.load(file)

def process_email():
    """
    Process an email received via standard input
    """
    config = load_config()
    assistants_config = load_assistants()

    logger = Logger(config)
    logger.log_message("Script started")

    try:
        raw_email = sys.stdin.read()
        logger.log_message(f"Email received, length: {len(raw_email)}")

        logger.log_raw_email(raw_email)

        email_parser = EmailParser(logger)
        prompt_enhancer = PromptEnhancer(logger)
        ai_client = AIClient(config, logger)
        response_formatter = ResponseFormatter(config, logger)
        email_sender = EmailSender(logger)

        email_data = email_parser.extract_email_content(raw_email)

        if email_parser.is_no_reply_address(email_data['sender'], assistants_config):
            logger.log_message("Sender is a no-reply address. No response will be sent.")
            return

        default_assistant = config.get('General', 'default_assistant')
        assistant_name = email_parser.detect_assistant(email_data, assistants_config, default_assistant)

        if assistant_name in assistants_config:
            assistant_config = assistants_config[assistant_name]
        else:
            assistant_config = assistants_config.get('default', {})
            logger.log_message(f"Assistant {assistant_name} not found, using default")

        assistant_config['name'] = assistant_name

        ai_response = ai_client.ask_ai(
            email_data['content'],
            email_data['sender'],
            assistant_config,
            prompt_enhancer
        )

        response_data = ai_client.process_ai_response(ai_response, assistant_config)

        email_sender.send_response(
            email_data['sender'],
            email_data['subject'],
            response_data,
            assistant_config,
            response_formatter
        )

        logger.send_log_to_discord(email_data, response_data, assistant_name)

    except Exception as e:
        error_msg = f"Error during processing: {str(e)}"
        logger.log_message(f"CRITICAL ERROR: {error_msg}")
        try:
            if 'email_data' in locals() and 'sender' in email_data:
                error_response = {
                    'message': "Sorry, an error occurred while processing your email."
                }
                if 'assistant_config' not in locals():
                    assistant_config = assistants_config.get('default', {})

                email_sender.send_response(
                    email_data['sender'],
                    email_data.get('subject', 'Error'),
                    error_response,
                    assistant_config,
                    response_formatter
                )

                logger.send_log_to_discord(email_data, error_response, 'error')
        except Exception as e2:
            logger.log_message(f"Error sending error response: {str(e2)}")
    finally:
        logger.log_message("Done")

if __name__ == "__main__":
    process_email()
