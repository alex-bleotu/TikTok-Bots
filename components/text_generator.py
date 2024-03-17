import random

from openai import OpenAI
from components.json_reader import VideoType as Type
from components.json_reader import FactType
from dotenv import load_dotenv
import os

load_dotenv()

key = os.environ.get('TOKEN_CHAT_GPT')


class TextGenerator:
    def __init__(self):
        self.__motivational_hashtags = [
            "#inspirational",
            "#quotes",
            "#motivation",
            "#positivevibes",
            "#challenge",
            "#lifestyle",
            "#goals",
            "#success",
            "#selfimprovement",
            "#growth",
            "#mindset",
            "#positivity",
            "#dreambig",
            "#believeinyourself",
            "#overcome",
            "#perseverance",
            "#determination",
            "#inspire",
            "#motivational"
        ]

    def get_promt(self, type):
        if type == Type.FACTS:
            with open("utils/prompts/fact.txt", 'r') as file:
                prompt = file.readline().strip()
        return prompt

    def __choose_random_promt(self, type, video_type=None):
        if type == Type.FACT:
            promts = [f for f in os.listdir("utils/prompts/facts/" + video_type.value + "/") if f.endswith(".txt")]
            return random.choice(promts)
        elif type == Type.STORY:
            promts = [f for f in os.listdir("utils/prompts/stories/" + video_type.value + "/") if f.endswith(".txt")]
            return random.choice(promts)

    def generate(self, promt_type, new_promt=None, example=None, video_type=None):

        if example is None:
            if promt_type == Type.FACT:
                # choose random text file from folder utils/prompts/facts/
                prompt_file = self.__choose_random_promt(promt_type, video_type)
                with open("utils/prompts/facts/" + video_type.value + "/" + prompt_file, 'r') as file:
                    prompt = file.read()
                    prompt += ("\n\nmake a script like the one above,the script must have the same structure")
                    print("Promt:\n" + prompt)
                if (video_type == Type.MOTIVATION):
                    prompt = prompt.replace("other facts", "more motivation. Keep the initial introduction the same, "
                                                           "and the first sentence must not be longer than 30 "
                                                           "characters")
            elif promt_type == Type.STORY:
                prompt_file = self.__choose_random_promt(promt_type, video_type)
                with open("utils/prompts/stories/" + video_type.value + "/" + prompt_file, 'r') as file:
                    prompt = file.read()
                    prompt += ("make a story like the one above,the script must have the same structure but a "
                               "different story")
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
                                                  "emojis. dont use the word boost"},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content.strip().replace("\n", "")
        except Exception as e:
            raise e

    def save_text(self, text):
        with open("utils/temp/text.txt", 'w') as file:
            file.write(text)

    def __list_to_string(self, list):
        return ' '.join([str(elem) for elem in list])

    def get_hash_tags(self, type, video_type=None):
        if type == Type.FACT:
            if video_type == FactType.MOTIVATIONAL:
                return self.__list_to_string(random.sample(self.__motivational_hashtags, 6) + ["#tiktok", "#fyp",
                                                                                               "#foryoupage"])
            return ""
        if type == Type.SEGMENT:
            return "#tiktok #fyp #foryoupage"
        return ""
