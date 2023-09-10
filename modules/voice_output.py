import pyaudio  # pip install pyaudio
import pyttsx3  # pip install pyttsx3

import queue
import time
import threading
import wave
import os

from datetime import datetime

from utils.datatypes import ThreadSafeBoolean


class VoiceOutputThread(threading.Thread):
    def __init__(self, message_queue, interrupt_flag, is_playing_flag, voice_id=None):
        threading.Thread.__init__(self)

        self.message_queue = message_queue
        self.interrupt_flag = interrupt_flag
        self.is_playing_flag = is_playing_flag
        self.voice_id = voice_id

        self.daemon = True
        self.start()

    def run(self):
        self.engine = pyttsx3.init()

        if self.voice_id:
            self.engine.setProperty(
                "voice",
                self.voice_id,
            )

        t_running = True
        while t_running:
            if self.message_queue.empty():
                self.interrupt_flag.set(False)
                self.is_playing_flag.set(False)
                time.sleep(0.1)
            else:
                self.is_playing_flag.set(True)
                command, message = self.message_queue.get()
                if command == "exit":
                    t_running = False
                elif command == "say":
                    fname = os.path.join(
                        "wavs", datetime.now().strftime("output_%Y%m%d_%H%M%S.wav")
                    )
                    if not os.path.exists("wavs"):
                        os.mkdir("wavs")

                    self.engine.save_to_file(message, fname)
                    self.engine.runAndWait()

                    self.play_file(fname)

    def play_file(self, filename):
        p = pyaudio.PyAudio()

        with wave.open(filename, "rb") as wf:
            stream = p.open(
                format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True,
            )

            # Read and play the audio data in chunks
            chunk_size = 1024
            data = wf.readframes(chunk_size)
            while data:
                if self.interrupt_flag.get():
                    break

                stream.write(data)
                data = wf.readframes(chunk_size)

            stream.stop_stream()
            stream.close()

        p.terminate()


class VoiceOutput:
    def __init__(self, voice_id=None):
        self.message_queue = queue.Queue()
        self.interrupt_flag = ThreadSafeBoolean()
        self.is_playing_flag = ThreadSafeBoolean()
        self.voice_id = voice_id

        self.voice_output_thread = VoiceOutputThread(
            self.message_queue, self.interrupt_flag, self.is_playing_flag, self.voice_id
        )

    def __del__(self):
        self.message_queue.put(("exit", ""))
        self.voice_output_thread.join()

    def say(self, message):
        self.message_queue.put(("say", message))

    def interrupt(self):
        self.interrupt_flag.set(True)

    def is_playing(self):
        return self.is_playing_flag.get()
