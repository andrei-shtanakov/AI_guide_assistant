# ai_integration.py
from openai import OpenAI
from anthropic import Anthropic
import os

class AIAnalyzer:
    def __init__(self):
        self.openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.anthropic_client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
    
    def analyze_with_openai(self, config_text, existing_results):
        prompt = f"""Analyze this configuration and existing analysis results. 
        Provide your insights and recommendations.
        
        Configuration:
        {config_text}
        
        Existing analysis:
        {existing_results}
        
        Please provide:
        1. Your assessment of the configuration
        2. Agreement or disagreement with existing findings
        3. Additional recommendations if any
        """
        
        response = self.openai_client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are an expert system configuration analyzer."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content

    def analyze_with_claude(self, config_text, existing_results):
        prompt = f"""Analyze this configuration and existing analysis results. 
        Provide your insights and recommendations.
        
        Configuration:
        {config_text}
        
        Existing analysis:
        {existing_results}
        
        Please provide:
        1. Your assessment of the configuration
        2. Agreement or disagreement with existing findings
        3. Additional recommendations if any
        """
        
        response = self.anthropic_client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=2000,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        return response.content[0].text