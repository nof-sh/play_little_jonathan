import platform
import time
from pydub import AudioSegment
from pydub.playback import play
import numpy as np
import sounddevice as sd

def play_song():
    freqs = {"la": 220,
            "si": 247,
            "do": 261,
            "re": 293,
            "mi": 329,
            "fa": 349,
            "sol": 392,
            }

    notes = "sol,250-mi,250-mi,500-fa,250-re,250-re,500-do,250-re,250-mi,250-fa,250-sol,250-sol,250-sol,500"

    for note in notes.split("-"):
        note, duration = note.split(",")
        duration = int(duration) / 1000  # Convert duration from ms to s for time.sleep

        if platform.system() == "Windows":
            import winsound
            winsound.Beep(freqs[note], int(duration * 1000))  # winsound.Beep expects duration in ms
        else:  # MacOS, Linux, and others
            # Generate a 440 Hz sine wave for 5 seconds with -3 dBFS peak amplitude
            t = np.linspace(0, duration, int(duration * 44100), False)
            note = np.sin(freqs[note] * 2 * np.pi * t)
            audio = note * (2**15 - 1) / np.max(np.abs(note))
            audio = audio.astype(np.int16)

            # Start playback
            sd.play(audio, 44100)
            #sd.wait()

        time.sleep(duration)  # Wait for the duration of the note before playing the next
    sd.stop()

play_song()