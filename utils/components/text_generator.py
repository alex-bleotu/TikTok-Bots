from openai import OpenAI
from utils.components.json_reader import VideoType as Type
from dotenv import load_dotenv
import os

load_dotenv()

key = os.environ.get('TOKEN_CHAT_GPT')

class TextGenerator:
    def __init__(self):
        pass

    def get_promt(self, type):
        if type == Type.FACTS:
            with open("utils/prompts/fact.txt", 'r') as file:
                prompt = file.readline().strip()
        return prompt

    def generate(self, promt_type, new_promt = None, example = None):

        if example is None:
            if promt_type == Type.FACT:
                with open("utils/prompts/facts/fact.txt", 'r') as file:
                    prompt = file.read()
                    prompt += "make a script like the on above,the script must have the same structure with a different wiered begining and other facts"
                    print(prompt)
            elif promt_type == Type.STORY:
                with open("utils/prompts/stories/story.txt", 'r') as file:
                    prompt = file.read()
                    prompt += "make a script like the on above,the script must have the same structure but a different story"
            else:
                raise Exception("Invalid promt type")
        else:
            prompt = example

        if new_promt is not None:
            if promt_type == Type.FACT:
                prompt += ", make the facts specifically about " + new_promt
            else:
                prompt += ", make the story specifically about " + new_promt

        client = OpenAI(
            api_key=key,
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
            raise e

    def save_text(self, text):
        with open("utils/temp/text.txt", 'w') as file:
            file.write(text)


