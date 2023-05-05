# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Importing Libraries / Modules 
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
import pygame
import math
from pydub import AudioSegment
import numpy as np

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Variables
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Define Morse code mappings
MORSE_CODE_DICT = {'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
                   'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
                   'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
                   'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
                   '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.'}


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Functions
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# -- Function to generate dot sound --
def generate_dot_sound():
    # Set parameters for the sound
    frequency = 700  # Hz
    duration = 0.1  # seconds
    volume = 32767  # 16-bit integer
    
    # Generate the sound wave
    samples = []
    for i in range(int(duration * 44100)):
        value = int(volume * math.sin(2 * math.pi * frequency * i / 44100))
        samples.append(value)
    
    # Save the sound wave in a NumPy array
    dot_sound = np.array(samples, dtype=np.int16)
    
    return dot_sound

# -- Function to generate dash Sound --
def generate_dash_sound():
    # Set parameters for the sound
    frequency = 600  # Hz
    duration = 0.4  # seconds
    volume = 32767  # 16-bit integer

    # Generate the sound wave
    sound_wave = []
    for i in range(int(duration * 44100)):
        value = int(volume * math.sin(2 * math.pi * frequency * i / 44100))
        sound_wave.append(value)

    # convert the list to numpy array and return it
    return np.array(sound_wave)

# -- Function to convert text to Morse code --
def text_to_morse_code(text):
    morse_code = ""
    for char in text.upper():
        if char == " ":
            morse_code += "  "
        elif char in MORSE_CODE_DICT:
            morse_code += MORSE_CODE_DICT[char] + " "
    return morse_code


# -- Function to convert Morse code to MP3 --
def morse_code_to_mp3(morse_code, output_file):
    # Initialize mixer
    pygame.mixer.init()

    silence_duration = 66 # in milliseconds

    # Generate audio segments for Morse code
    audio_segments = []
    for symbol in morse_code:
        if symbol == ".":
            # generate dot sound
            dot_sound = generate_dot_sound()
            audio_normalized = np.int16(dot_sound * (32767 / np.max(np.abs(dot_sound))))
            audio_segments.append(AudioSegment(audio_normalized.tobytes(), frame_rate=44100, sample_width=2, channels=1))
            # audio_segments.append(AudioSegment(dot_sound.tobytes(), frame_rate=freq, sample_width=2, channels=1))
            audio_segments.append(AudioSegment.silent(duration=silence_duration))
       
        elif symbol == "-":
            # generate dash sound
            sound_wave = generate_dash_sound()
            audio_normalized = np.int16(sound_wave * (32767 / np.max(np.abs(sound_wave))))
            audio_segments.append(AudioSegment(audio_normalized.tobytes(), frame_rate=44100, sample_width=2, channels=1))
            audio_segments.append(AudioSegment.silent(duration=silence_duration))
        elif symbol == " ":
            audio_segments.append(AudioSegment.silent(duration=100)) # 100ms of silence
        else:
            # Ignore unknown characters
            continue

    # combine audio segments
    combined_sound = AudioSegment.empty()
    for segment in audio_segments:
        combined_sound += segment

    # export the combined sound to a new MP3 file
    combined_sound.export(output_file, format="mp3")

    # Stop mixer
    pygame.mixer.quit()

# --- Function to print out my Logo ---
def myLogo():
    print("Created and Tested by: ")
    print("   __                  _         ___ _                       ")
    print("   \ \  __ _  ___ ___ | |__     / __\ | ___  _   _ ___  ___  ")
    print("    \ \/ _` |/ __/ _ \| '_ \   / /  | |/ _ \| | | / __|/ _ \ ")
    print(" /\_/ / (_| | (_| (_) | |_) | / /___| | (_) | |_| \__ \  __/ ")
    print(" \___/ \__,_|\___\___/|_.__/  \____/|_|\___/ \__,_|___/\___| ")
    print("Dedicated to Peter Zlomek and Harely Alderson III")


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# MAIN
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
myLogo()
print("## == == == == == == == == == == == == == == == == == == == == == == == == == == == == ##")
inputFile = input('Name of text file (DO NOT include .txt extension): ') 
outputFile = input('Name of output mp3 (DO NOT include .mp3 extension): ') 
print("## == == == == == == == == == == == == == == == == == == == == == == == == == == == == ##")

# Read input file
with open(f"{inputFile}.txt", "r") as f:
    text = f.read()

# Convert text to Morse code
morse_code = text_to_morse_code(text)

# Open a file named "output.txt" in write mode
with open(f"{outputFile}.txt", "w") as file:
    # Write the string to the file
    file.write(morse_code)

# Convert Morse code to MP3
morse_code_to_mp3(morse_code, f"{outputFile}.mp3")
print(f"Done making {outputFile}.mp3 from {inputFile}.txt!")
