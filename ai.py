from openai import OpenAI


client = OpenAI(
  api_key='KEY-HERE'
)

def call_ai(call):
    
    completion = client.chat.completions.create(
    model='gpt-4o-mini',
    store=True,
    messages=[{'role': 'user', 'content': f'{call}'}]
    )
    return completion.choices[0].message.content


