import speech_recognition as sr
import pyttsx3
import re

# Initialize text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    """Converts text to speech."""
    engine.say(text)
    engine.runAndWait()

def recognize_speech():
    """Captures and recognizes speech input from the microphone."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for a mathematical expression...")
        speak("Please say a mathematical expression.")
        recognizer.adjust_for_ambient_noise(source)
        
        try:
            audio = recognizer.listen(source)
            expression = recognizer.recognize_google(audio)
            print(f"You said: {expression}")
            return expression.lower()
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand. Please try again.")
            speak("Sorry, I couldn't understand. Please try again.")
            return None
        except sr.RequestError:
            print("Could not request results. Check your internet connection.")
            speak("Could not request results. Check your internet connection.")
            return None

def preprocess_expression(expression):
    """Converts spoken words into a valid mathematical expression."""
    words_to_symbols = {
        "plus": "+", "minus": "-", "times": "*", "multiplied by": "*",
        "divided by": "/", "over": "/", "x": "*"  # Ensure "x" is replaced with "*"
    }

    # Replace words with corresponding symbols
    for word, symbol in words_to_symbols.items():
        expression = expression.replace(word, symbol)
    
    # Remove invalid characters (keep numbers, operators, spaces, and parentheses)
    expression = re.sub(r"[^0-9+\-*/(). ]", "", expression)

    return expression.strip()  # Trim extra spaces

def calculate(expression):
    """Evaluates a full mathematical expression."""
    try:
        expression = preprocess_expression(expression)  # Convert words to symbols
        print(f"Evaluating: {expression}")  # Debugging print statement
        result = eval(expression)  # Evaluate the expression safely
        return result
    except Exception as e:
        print("Invalid expression:", e)
        return None

def main():
    """Main function to run the voice calculator."""
    while True:
        expression = recognize_speech()
        
        if expression:
            result = calculate(expression)
            
            if result is not None:
                print(f"Result: {result}")
                speak(f"The result is {result}")
            else:
                print("Operation not recognized. Please try again.")
                speak("Operation not recognized. Please try again.")

        speak("Do you want to calculate another expression? Say yes or no.")
        response = recognize_speech()

        if response and "no" in response:
            speak("Okay, goodbye!")
            break

if __name__ == "__main__":
    main()
