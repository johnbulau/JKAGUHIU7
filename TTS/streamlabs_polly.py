import random
import time

import requests
from requests.exceptions import JSONDecodeError

from utils import settings
from utils.voice import check_ratelimit

voices = {
    "Brian",
    "Emma",
    "Russell",
    "Joey",
    "Matthew",
    "Joanna",
    "Kimberly",
    "Amy",
    "Geraint",
    "Nicole",
    "Justin",
    "Ivy",
    "Kendra",
    "Salli",
    "Raveena",
}


# valid voices https://lazypy.ro/tts/


class StreamlabsPolly:
    def __init__(self):
        self.url = "https://streamlabs.com/polly/speak"
        self.max_chars = 450
        self.voices = voices
        self.has_sub = False

    def run(self, text, filepath, random_voice: bool = False, tries=0):
        if random_voice:
            voice = self.randomvoice()
        else:
            if not settings.config["settings"]["tts"]["streamlabs_polly_voice"]:
                raise ValueError(
                    f"Please set the config variable STREAMLABS_POLLY_VOICE to a valid voice. options are: {voices}"
                )
            voice = str(
                settings.config["settings"]["tts"]["streamlabs_polly_voice"]
            ).capitalize()
        body = {"voice": voice, "text": text, "service": "polly"}
        response = requests.post(self.url, data=body)
        if not check_ratelimit(response):
            self.run(text, filepath, random_voice)

        else:
            try:
                voice_data = requests.get(response.json()["speak_url"])
                with open(filepath, "wb") as f:
                    f.write(voice_data.content)
            except (KeyError, JSONDecodeError):
                try:
                    if response.json()["error"] == "No text specified!":
                        raise ValueError("Please specify a text to convert to speech.")
                except (KeyError, JSONDecodeError):
                    print("Error occurred calling Streamlabs Polly")
            except Exception as e:
                print("an exception is being resolved in streamlabs polly", e)
                if tries > 3:
                    tries += 1
                else:
                    raise ValueError("streamlabspolly tts not allowing to get audio data.")
                time.sleep(random.randint(1, 5))
                self.run(text, filepath, random_voice)

    def randomvoice(self) -> str:
        return random.choice(tuple(self.voices))