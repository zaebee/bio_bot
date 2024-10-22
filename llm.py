import cohere

import preambles

class Client:
    
    def __init__(self, api_key: str):
        self.llm = cohere.AsyncClient(api_key=api_key)
        self.preamble = preambles.BASE
    
    async def generate(self, message: str):
        messages=[
            {'role': 'system', 'content': self.preamble},
            {
                'role': 'user',
                'content': message,
            },
        ]
        response = await self.llm.chat(message=message, preamble=self.preamble)
        return response