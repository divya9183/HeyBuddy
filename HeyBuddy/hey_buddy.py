import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import random
import time

# Initialize speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 170)

def speak(text):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

def listen(prompt=None, timeout=6):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        if prompt:
            speak(prompt)
        print("🎙️ Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=timeout)
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.WaitTimeoutError:
            print("Timeout: No speech detected.")
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
        except sr.RequestError as e:
            print(f"API error; {e}")
    return ""

def greet_user():
    if not os.path.exists("username.txt") or os.stat("username.txt").st_size == 0:
        name = listen("Hi! What’s your name?")
        if name:
            with open("username.txt", "w") as f:
                f.write(name)
            speak(f"Nice to meet you, {name}!")
        else:
            speak("Sorry, I didn't catch your name.")
    else:
        with open("username.txt", "r") as f:
            name = f.read().strip()
        speak(f"Welcome back, {name}!")

def add_to_todo(item):
    with open("todo.txt", "a") as file:
        file.write(f"- {item}\n")
    speak(f"I added '{item}' to your to-do list.")

jokes = [
    "Why don’t scientists trust atoms? Because they make up everything!",
    "Why did the math book look sad? Because it had too many problems.",
    "I told my computer I needed a break, and now it won’t stop sending me KitKat ads."
]

def respond(command):
    print(f"[Command]: {command}")

    if any(kw in command for kw in ["wikipedia", "wiki"]):
        query = command.replace("wikipedia", "").replace("wiki", "").strip()
        if not query:
            speak("What should I search on Wikipedia?")
            query = listen()
        if query:
            speak(f"Searching Wikipedia for {query}")
            try:
                result = wikipedia.summary(query, sentences=2)
                speak(result)
            except wikipedia.exceptions.DisambiguationError:
                speak("There are multiple results. Please be more specific.")
            except wikipedia.exceptions.PageError:
                speak("I couldn't find anything on Wikipedia.")
            except Exception as e:
                speak("Something went wrong with Wikipedia.")
                print(f"Wikipedia error: {e}")
        else:
            speak("No query provided for Wikipedia search.")

    elif any(kw in command for kw in ["search google", "google", "search about", "tell me about"]):
        # Treat "search google" as Wikipedia search and speak
        # Remove keywords from command to get query
        query = command
        for phrase in ["search google", "google", "search about", "tell me about"]:
            query = query.replace(phrase, "")
        query = query.strip()
        if not query:
            speak("What should I tell you about?")
            query = listen()
        if query:
            speak(f"Let me tell you about {query} from Wikipedia.")
            try:
                result = wikipedia.summary(query, sentences=2)
                speak(result)
            except wikipedia.exceptions.DisambiguationError:
                speak("There are multiple results. Please be more specific.")
            except wikipedia.exceptions.PageError:
                speak("I couldn't find anything.")
            except Exception as e:
                speak("Something went wrong.")
                print(f"Wiki search error: {e}")
        else:
            speak("No topic provided.")

    elif "time" in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {now}.")

    elif any(kw in command for kw in ["joke", "funny", "laugh"]):
        speak(random.choice(jokes))

    elif any(kw in command for kw in ["to-do", "todo", "add task"]):
        item = listen("What should I add to your to-do list?")
        if item:
            add_to_todo(item)
        else:
            speak("I didn't hear what to add.")

    elif "youtube" in command:
        speak("Opening YouTube.")
        webbrowser.open("https://www.youtube.com")

    elif "google" in command:
        # If user just says "open google" or similar
        speak("Opening Google.")
        webbrowser.open("https://www.google.com")

    elif any(kw in command for kw in ["stop", "exit", "quit", "bye"]):
        speak("Goodbye!")
        exit()

    else:
        speak("Sorry, I don't know that command yet.")

if __name__ == "__main__":
    greet_user()
    speak("Hey Buddy is ready. Say 'Hey Buddy' to begin.")

    while True:
        wake = listen(timeout=5)
        print(f"[Wake Input]: {wake}")

        if any(keyword in wake for keyword in ["hey buddy", "hi buddy", "a buddy", "buddy"]):
            speak("Yes? I'm listening...")
            command = listen("What can I do for you?")
            if command:
                respond(command)
            else:
                speak("Sorry, I didn't catch that.")
        else:
            print("Wake word not detected. Listening again...")
        time.sleep(1)
