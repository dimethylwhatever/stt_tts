from RealtimeSTT import AudioToTextRecorder
import asyncio
import random
import string
import os
from pygame import mixer
from gtts import gTTS

mixer.init(devicename="Your virtual cable name here")


def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

async def text_to_speech(text):
    if not text or not isinstance(text, str):
        raise ValueError("Text input must be a non-empty string")
    
    def sync_tts():
        mp3_file = f"tts_{generate_random_string()}.mp3"
        tts = gTTS(text)
        tts.save(mp3_file)
        return mp3_file
    
    loop = asyncio.get_event_loop()
    mp3_file = await loop.run_in_executor(None, sync_tts)
    print(f"Speech saved to {mp3_file}")
    await play_through_VC(mp3_file)
    return mp3_file

async def play_through_VC(mp3_file):
    try:
        mixer.music.load(mp3_file)
        mixer.music.play()
        while mixer.music.get_busy():
            await asyncio.sleep(0.1)
            
        mixer.music.unload()
        print(f"Played {mp3_file}")
    except Exception as e:
        print(f"Error playing audio: {e}")
    finally:
        try:
            if os.path.exists(mp3_file):
                os.remove(mp3_file)
                print(f"Removed {mp3_file}")
        except Exception as e:
            print(f"Error removing {mp3_file}: {e}")

async def main():
    print("Initializing recorder... Please wait until it says 'Speak now'")
    try:
        recorder = AudioToTextRecorder(language="en")
        prev_text = ""
        print("Speak now")
        
        while True:
            try:
                text = recorder.text()
                if text and text != prev_text:
                    print(f"Recognized: {text}")
                    prev_text = text
                    await text_to_speech(text)
                await asyncio.sleep(0.1)
            except Exception as e:
                print(f"Error in processing loop: {e}")
                await asyncio.sleep(1)
    except Exception as e:
        print(f"Error initializing recorder: {e}")
    finally:
        mixer.quit()
        print("Program terminated")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Program interrupted by user")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        if mixer.get_init():
            mixer.quit()
