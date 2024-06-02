from openai import OpenAI
import os
import tiktoken

class ml_backend:
    def __init__(self,api_key) -> None:

        self.api_key = api_key
        self.client = OpenAI(
            api_key=api_key
        ) 

        # models = self.client.models.list() # list of model names
        # https://openai.com/api/pricing/
        self.model = 'gpt-3.5-turbo-0125'

    def generate_email(self, userPrompt ="Write me a professionally sounding email", subject="Project Meeting!", max_tokens=100):
        """Returns a generated an email using GPT3 with a certain prompt and starting sentence"""
        
        if self.model == 'davinci-002':
            # use v1/completions (legacy)
            # https://platform.openai.com/docs/api-reference/completions/create

            response = self.client.completions.create(
                model=self.model,
                prompt=userPrompt + ". Subject of email:" + "'" + subject + "'",
                temperature=0.71,
                max_tokens=max_tokens,
                top_p=1,
                frequency_penalty=0.36,
                presence_penalty=0.75
                )
            return response.choices[0].text
        
        elif self.model == 'gpt-3.5-turbo-0125': 
            # Creates a model response for the given chat conversation. 
            # https://platform.openai.com/docs/api-reference/chat/create
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an concise email writing assistant."},
                    {"role": "user", "content": userPrompt + ". Subject of email:" + "'" + subject + "'"}
                ],
                temperature=0.71,
                max_tokens=max_tokens, #The maximum number of tokens that can be generated in the chat completion
                n=1, #How many chat completion choices to generate for each input message
                frequency_penalty=0.36, #Number between -2.0 and 2.0. Positive values penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim.
                presence_penalty=0.75, #Number between -2.0 and 2.0. Positive values penalize new tokens based on whether they appear in the text so far, increasing the model's likelihood to talk about new topics.
                )
            return response.choices[0].message.content
        
    def gmail_friendly(self, sample):
        """Returns a string with each space being replaced with a plus so the email hyperlink can be formatted properly"""
        changed = list(sample)
        for i, c in enumerate(changed):
            if(c == ' ' or c =='  ' or c =='   '):
                changed[i] = '+'
            elif(c=='\n' or c=='\n\n' ):
                changed[i] = '%0a'
        return ''.join(changed)
    
    def num_tokens_from_string(string: str, model_name: str) -> int:
        """Returns the number of tokens in a text string."""
        encoding = tiktoken.encoding_for_model(model_name)
        num_tokens = len(encoding.encode(string))
        return num_tokens
    
