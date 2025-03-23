#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests

class AIClient:
    def __init__(self, config, logger):
        """
        Initialize the client for the AI API

        Args:
            config: Configuration containing API parameters
            logger: Logger instance to log events
        """
        self.api_url = config.get('API', 'url')
        self.timeout = config.getint('API', 'timeout')
        self.logger = logger

    def ask_ai(self, content, sender, assistant_config, prompt_enhancer=None):
        """
        Query the AI API with specific content

        Args:
            content: The content to send to the API
            sender: The sender's email address
            assistant_config: The assistant configuration
            prompt_enhancer: Instance of PromptEnhancer (optional)

        Returns:
            tuple: (response, assistant_name)

        Raises:
            Exception: If an error occurs during the API call
        """
        try:
            base_prompt = assistant_config.get('prompt', 'Reply to the following prompt:')
            assistant_name = assistant_config.get('name', 'assistant')

            self.logger.log_message(f"Calling AI API for assistant: {assistant_name}...")

            if assistant_config.get('enhance_prompt', False) and prompt_enhancer:
                enhancements = assistant_config.get('enhancements', [])
                enriched_prompt = prompt_enhancer.enhance_prompt(base_prompt, enhancements)
            else:
                enriched_prompt = base_prompt

            full_content = f"{enriched_prompt} Reminder: You are talking to the sender ({sender}) of this mail! {content}"

            params = {'content': full_content, 'timeout': self.timeout}
            response = requests.get(self.api_url, params=params)

            self.logger.log_message(f"API response status: {response.status_code}")

            return response
        except Exception as e:
            self.logger.log_message(f"ERROR in ask_ai: {str(e)}")
            raise e

    def process_ai_response(self, response, assistant_config):
        """
        Process the AI API response

        Args:
            response: API response
            assistant_config: Assistant configuration

        Returns:
            dict: Processed response data
        """
        try:
            if response.status_code == 200:
                ai_data = response.json()
                self.logger.log_message(f"AI data received")

                if ai_data.get('success'):
                    ai_response = ai_data.get('message', "Sorry, I couldn't process your request.")
                    return {
                        'message': ai_response
                    }
                else:
                    return {
                        'message': "Sorry, the AI couldn't process your message correctly."
                    }
            else:
                return {
                    'message': f"Error communicating with the AI: {response.status_code}"
                }
        except Exception as e:
            self.logger.log_message(f"ERROR in process_ai_response: {str(e)}")
            return {
                'message': f"Error processing AI response: {str(e)}"
            }
