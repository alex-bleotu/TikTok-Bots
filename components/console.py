from components import textToSpeech as tts
from components import videoProcessing as vid
from components import textGenerator as tg
from components.textGenerator import Type

class ConsoleUI():
    def __print_menu(self):
        print("\nChoose an option:")
        print("1. Facts")
        print("2. Story (Coming soon)")
        print("0. Exit")

    def __print_facts_menu(self):
        print("\nChoose an option:")
        print("1. Random Topics")
        print("2. Custom Topic")

    def __print_facts_new_promt(self):
        print("\nWhat should the facts be about?")

    def __print_video_confirmation(self):
        print("\nDo you want to generate a video with this script?  Y/N")

    def __print_video_config(self):
        print("\nDo you want to add subtitles?  Y/N")

    def __print_open_video(self):
        print("\nDo you want to open the video?  Y/N")

    def __generate_video(self, script):
        print("\nCurrent script:")
        print(script)

        tg.save_text(script)
        tts.generate()

        self.__print_video_confirmation()
        command = input("Enter your command: ")
        if command == "Y" or command == "y":
            self.__print_video_config()
            command = input("Enter your command: ")
            if command == "Y" or command == "y":
                vid.generate()
                print("\nVideo generated successfully with subtitles!")
            else:
                vid.generate(False)
                print("\nVideo generated successfully!")

            self.__print_open_video()
            command = input("Enter your command: ")
            if command == "Y" or command == "y":
                vid.open_video()


    def run(self):
        while True:
            self.__print_menu()
            try:
                command = int(input("Enter your command: "))
                if command == 1:
                    self.__print_facts_menu()
                    command = int(input("Enter your command: "))
                    if command == 1:
                        script = tg.generate(Type.FACTS)

                        self.__generate_video(script)
                    elif command == 2:
                        self.__print_facts_new_promt()
                        promt = input("Enter your topic: ")
                        script = tg.generate(Type.FACTS, promt)

                        self.__generate_video(script)
                    else:
                        print("Invalid command!")
                elif command == 2:
                    print("Coming soon")
                elif command == 0:
                    return
                else:
                    print("Invalid command!")

                return
            except ValueError:
                print("Invalid command!")
