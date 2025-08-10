import os
import google.generativeai as genai
import pyttsx3
import speech_recognition as sr
import webbrowser
import requests
import datetime
import wikipedia
import pyjokes

# Initialize api key
genai.configure(api_key="AIzaSyBTvLDnwSzJRoWRuG3B9r8hDLfz3eZj4O4")

# Function to get AI-generated replies

                
def Reply(question):
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        prompt = (
            "You are SAKSHI, a helpful AI assistant. "
            "and i am from india okay??"
            "My name is Puskar"
            "I am an engineer "
            "I use you as my ai assistant"
            "Respond in a helpful and concise manner.\n\n"
            f"User: {question}"
        )
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}"


# Initialize text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Function to convert text to speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen and convert speech to text
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You said: {query}\n")
    except Exception:
        print("Could not understand audio. Please say that again.")
        return "None"
    return query

# Function to get current weather of a city
def get_weather(city):
    api_key = os.getenv("32207e0863967be32037e3f42fc68997") 
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(base_url)
    data = response.json()

    if data["cod"] != "404":
        main = data["main"]
        temperature = main["temp"]
        weather_desc = data["weather"][0]["description"]
        return f"The temperature in {city} is {temperature}°C with {weather_desc}."
    else:
        return "City not found."

# Function to get current time
def get_time():
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    return f"The current time is {current_time}"

# Function to tell a random joke
def tell_joke():
    
    return pyjokes.get_joke()



# Main program execution
if __name__ == '__main__':
    speak("Hello! How can I assist you today?")

    while True:
        query = takeCommand().lower()

        if query == "none":
            continue

        if 'open youtube' in query:
            webbrowser.open("https://www.youtube.com")
            speak("Opening YouTube")

        elif 'open google' in query:
            webbrowser.open("https://www.google.com")
            speak("Opening Google")

        elif 'open github' in query:
            webbrowser.open("https://www.github.com")
            speak("Opening GitHub")

        elif 'time' in query:
            current_time = get_time()
            print(current_time)
            speak(current_time)

        elif 'weather' in query:
            speak("Please tell me the city name.")
            city = takeCommand().lower()
            if city != "none":
                weather = get_weather(city)
                print(weather)
                speak(weather)
            else:
                speak("I did not catch the city name.")

        elif 'joke' in query:
            joke = tell_joke()
            print(joke)
            speak(joke)

        elif 'wikipedia' in query:
            speak("What would you like to know about?")
            search_query = takeCommand().lower()
            if search_query != "none":
                try:
                    results = wikipedia.summary(search_query, sentences=2)
                    print(results)
                    speak(results)
                except wikipedia.exceptions.DisambiguationError:
                    speak("That term is ambiguous. Please be more specific.")
                except wikipedia.exceptions.PageError:
                    speak("Sorry, I could not find any information about that.")
            else:
                speak("I did not hear the topic.")

        elif 'bye' in query:
            speak("Goodbye!")
            break

        else:
            ans = Reply(query)
            speak(ans)
            print(ans)
