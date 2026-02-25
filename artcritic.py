#!/usr/bin/env python


import os
import dotenv
import base64
import time
import anthropic
import shutil
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer


class ArtCritic():
    def __init__(self, api_key: str, system_prompt: str):
        self.api_key = api_key
        self.system_prompt = system_prompt

        self.client = anthropic.Anthropic(api_key=api_key)


    @staticmethod
    def encode_image(image_path: str) -> str:
        with open(image_path, 'rb') as f:
            image_data = base64.b64encode(f.read()).decode('utf-8')
            return image_data


    def get_title_from_ai(self, image_path: str) -> str:
        image_data = ArtCritic.encode_image(image_path)

        try:
            message = self.client.messages.create(
                model='claude-haiku-4-5-20251001',
                max_tokens=100,
                system=self.system_prompt,
                messages=[
                    {
                        'role': 'user',
                        'content': [
                            {
                                'type': 'image',
                                'source': {
                                    'type': 'base64',
                                    'media_type': 'image/jpeg',
                                    'data': image_data,
                                },
                            },
                        ],
                    }
                ],
            )
            return message.content[0].text
        except Exception as e:
            print(e)
            return 'Untitled'


def get_system_prompt(system_prompt_path: str|None = None) -> str:
    if system_prompt_path is None:
        system_prompt_path = os.path.join(os.path.split(__file__)[0], 'system_prompt.txt')
    with open(system_prompt_path, 'r') as f:
        return f.read()


class MyEventHandler(FileSystemEventHandler):
    def __init__(self, api_key, system_prompt, target_dir):
        super().__init__()
        self.art_critic = ArtCritic(api_key, system_prompt)
        self.target_dir = target_dir

    def on_created(self, event):
        image_path = event.src_path

        # wait to make sure the file is written before (max 10 retries)
        prev_file_size = None
        for i in range(10):
            file_size = os.path.getsize(image_path)
            if file_size == prev_file_size:
                break
            prev_file_size = file_size
            time.sleep(1)
        else:
            print(f"Warning: {image_path} did not stabilize, skipping.")
            return
        
        _, image_name = os.path.split(image_path)
        image_base_name, image_extension = os.path.splitext(image_name)

        if image_extension != '.jpg':
            return
        
        title = self.art_critic.get_title_from_ai(image_path)

        target_txt_path = os.path.join(self.target_dir, f'{image_base_name}.txt')
        with open(target_txt_path, 'w') as f:
            f.write(title)

        target_img_path = os.path.join(self.target_dir, image_name)
        shutil.copy2(image_path, target_img_path)
        print(title)


def main():
    # load the environment variables from .env
    dotenv.load_dotenv()

    event_handler = MyEventHandler(api_key=os.environ['ANTHROPIC_API_KEY'],
                                   system_prompt=get_system_prompt(),
                                   target_dir=os.environ['TARGET_DIR'])
    observer = Observer()
    observer.schedule(event_handler, os.environ['WATCH_DIR'])
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nshutdown by user")
    finally:
        observer.stop()
        observer.join()


if __name__ == '__main__':
    main()
