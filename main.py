from RealtimeSTT import AudioToTextRecorder
import pyttsx3
import asyncio
import random
import string
import os
from pygame import mixer

mixer.init(devicename="Line 1 (Virtual Audio Cable)")

engine = pyttsx3.init()
engine.setProperty('rate', 210)

def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

async def speech(text):
    text = text.replace(",", "")
    name = f"{generate_random_string()}.wav"
    engine.save_to_file(text, name)
    engine.runAndWait()
    mixer.music.load(name)
    mixer.music.play()
    while mixer.music.get_busy():
        await asyncio.sleep(3)
    mixer.music.unload()
    os.remove(name)

if __name__ == '__main__':
    print("Wait until it says 'speak now'")
    recorder = AudioToTextRecorder(language="en")
    async def main_loop():
        prev_text = ""
        while True:
            text = recorder.text()
            if text != prev_text:
                print(text)
                await speech(text)
                prev_text = text
            await asyncio.sleep(0.1)
    asyncio.run(main_loop())


