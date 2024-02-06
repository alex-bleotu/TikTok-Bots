import random

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

    def __choose_random_promt(self, type, video_type = None):
        if type == Type.FACT:
            promts = [f for f in os.listdir("utils/prompts/facts/" + video_type.value + "/") if f.endswith(".txt")]
            return random.choice(promts)
        elif type == Type.STORY:
            promts = [f for f in os.listdir("utils/prompts/stories/" + video_type.value + "/") if f.endswith(".txt")]
            return random.choice(promts)

    def generate(self, promt_type, new_promt = None, example = None, video_type = None):

        if example is None:
            if promt_type == Type.FACT:
                # choose random text file from folder utils/prompts/facts/
                prompt_file = self.__choose_random_promt(promt_type, video_type)
                with open("utils/prompts/facts/" + video_type.value + "/" + prompt_file, 'r') as file:
                    prompt = file.read()
                    prompt += "make a script like the on above with 3 facts,the script must have the same structure with a different wiered begining and other facts"
                    print("Promt:\n" + prompt)
                if (video_type == Type.MOTIVATION):
                    prompt = prompt.replace("other facts", "more motivation. Add a title at the begining like it is in the original.")
            elif promt_type == Type.STORY:
                prompt_file = self.__choose_random_promt(promt_type, video_type)
                with open("utils/prompts/stories/" + video_type.value + "/" + prompt_file, 'r') as file:
                    prompt = file.read()
                    prompt += "make a story like the on above,the script must have the same structure but a different story"
                    print("Promt:\n" + prompt)
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
                    {"role": "system", "content": "dont ever make lists, create short texts, max 150 words, "
                                                  "that i can use in a tik tok as a script without hasta tags or "
                                                  "emojis"},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content.strip().replace("\n", "")
        except Exception as e:
            raise e

    def save_text(self, text):
        with open("utils/temp/text.txt", 'w') as file:
            file.write(text)


