from . import config

from captcha.image import ImageCaptcha

import base64
import random
import string
import time
import uuid


def timestamp_expired(timestamp):
    timestamp += config.config.captcha_timeout * 60
    return timestamp < time.time()


class Captcha:

    def __init__(self) -> None:
        self.captcha_dict = {}

    def clean(self):
        for k, v in self.captcha_dict.items():
            if timestamp_expired(v["timestamp"]):
                del self.captcha_dict[k]

    def validate(self, captcha_answer, captcha_token):
        data = self.captcha_dict.pop(captcha_token, None)
        if data:            
            return (False if timestamp_expired(data["timestamp"]) 
                else captcha_answer.lower() == data["captcha_answer"])
        return False

    def generate(self):
        self.clean()
        captcha_token = str(uuid.uuid4())
        captcha_answer = (''.join(random.choice(string.ascii_lowercase + string.digits)
            for _ in range(config.config.captcha_length)))
        image = ImageCaptcha(width = 320, height = 94)
        captcha_image = base64.b64encode(image.generate(captcha_answer).getvalue())
        data = {
            "captcha_image": captcha_image,
            "captcha_token": captcha_token,
            "captcha_answer": captcha_answer,
            "timestamp": time.time()
        }
        self.captcha_dict[captcha_token] = data
        return data

captcha = None
