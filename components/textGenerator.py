from enum import Enum

from openai import OpenAI


class Type(Enum):
    FACTS = 1

def generate(promt_type):
    if promt_type == Type.FACTS:
        with open("promts/facts.txt", 'r') as file:
            prompt = file.read()

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
        with open("temp/text.txt", 'w') as file:
            print(response.choices[0].message.content.strip().replace("\n", ""))
            file.write(response.choices[0].message.content.strip().replace("\n", ""))
    except Exception as e:
        print(e)

