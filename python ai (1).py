import speech_recognition as sr
import pyttsx3
import webbrowser
import time
import requests
from bs4 import BeautifulSoup
import wikipedia

# Initialize the speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Set to first available voice

# Function to make Jarvis speak
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen to user's command
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = r.listen(source)
        
        try:
            statement = r.recognize_google(audio, language='en-in')
            print(f"Jarvis heard: {statement}")
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that. Could you please repeat?")
            return "none"
        except sr.RequestError:
            speak("There was an error with the speech recognition service. Please try again.")
            return "none"
        return statement.lower()

# Google Search function using web scraping
def google_search(query):
    search_url = f"https://www.google.com/search?q={query}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    result = soup.find('div', {'class': 'BNeawe iBp4i AP7Wnd'})
    
    if result:
        return result.get_text()
    else:
        return "Sorry, I couldn't find any relevant results on Google."

# Wikipedia Search function (only called explicitly)
def search_wikipedia(query):
    try:
        results = wikipedia.summary(query, sentences=3)
        return results
    except wikipedia.exceptions.DisambiguationError as e:
        return f"I found multiple results for {query}. Could you be more specific?"
    except wikipedia.exceptions.HTTPTimeoutError:
        return "Sorry, I couldn't reach Wikipedia. Please try again later."
    except Exception as e:
        return "Sorry, I couldn't find anything related to your query."

# Main function
def main():
    speak("Hello, I am Jarvis. How can I assist you today?")
    
    while True:
        statement = takeCommand()

        # Handle exit command
        if 'quit' in statement or 'exit' in statement or 'stop' in statement:
            speak("Goodbye!")
            break

        # Open Google in browser
        elif 'open google' in statement:
            webbrowser.open_new_tab("https://www.google.com")
            speak("Opening Google.")
            time.sleep(5)

        # Open YouTube in browser
        elif 'open youtube' in statement:
            webbrowser.open_new_tab("https://www.youtube.com")
            speak("Opening YouTube.")
            time.sleep(5)

        # Search Google (default behavior)
        elif 'search' in statement:
            speak("What would you like to search on Google?")
            query = takeCommand()
            if query != "none":
                google_result = google_search(query)
                speak(f"Here is what I found on Google: {google_result}")

        # Search Wikipedia (only when specifically asked)
        elif 'search wikipedia' in statement:
            speak("What would you like to search for on Wikipedia?")
            query = takeCommand()
            if query != "none":
                results = search_wikipedia(query)
                speak(f"Here is what I found on Wikipedia: {results}")

        # Handle unrecognized commands
        elif 'rickroll' in statement:
            speak("I see you want to be Rickrolled! Opening a Rickroll video.")
            webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        
        else:
            speak("Sorry, I didn't understand that. Please try again.")

# Run the main function
if __name__ == "__main__":
    main()
