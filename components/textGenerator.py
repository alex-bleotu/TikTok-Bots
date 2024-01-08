from enum import Enum

from openai import OpenAI


class Type(Enum):
    FACTS = 1

def getPromt(type):
    if type == Type.FACTS:
        with open("promts/facts.txt", 'r') as file:
            prompt = file.readline().strip()
    return prompt

def generate(promt_type, new_promt = None):
    if promt_type == Type.FACTS:
        with open("promts/facts.txt", 'r') as file:
            prompt = file.read()

    if new_promt is not None:
        prompt += ", make the facts specifically about " + new_promt

    client = OpenAI(
        # defaults to os.environ.get("OPENAI_API_KEY")
        api_key="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",
    )

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "dont ever make lists, create short texts, max 150 words, that i can use in a tik tok as a script"},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip().replace("\n", "")
    except Exception as e:
        print(e)

def save_text(text):
    with open("temp/text.txt", 'w') as file:
        file.write(text)


