import speech_recognition as sr
import pyttsx3
import operator

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for a mathematical expression...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source)
            expression = recognizer.recognize_google(audio)
            print(f"You said: {expression}")
            return expression
        except sr.UnknownValueError:
            print("Sorry, could not understand the audio.")
            speak("Sorry, I could not understand. Please try again.")
        except sr.RequestError:
            print("Error connecting to speech recognition service.")
            speak("There was an error with the speech service. Please check your connection.")
    return None

def calculate(expression):
    ops = {
        'plus': operator.add,
        'minus': operator.sub,
        'times': operator.mul,
        'multiplied by': operator.mul,
        'divided by': operator.truediv,
        'over': operator.truediv,
    }
    
    for word, op in ops.items():
        if word in expression:
            numbers = expression.split(word)
            try:
                num1, num2 = float(numbers[0]), float(numbers[1])
                result = op(num1, num2)
                return result
            except ValueError:
                print("Could not process numbers correctly.")
                speak("I could not process the numbers correctly. Please try again.")
                return None
    
    print("Operation not recognized.")
    speak("I did not recognize the operation. Please use words like plus, minus, times, or divided by.")
    return None

def main():
    speak("Welcome to the voice calculator. Please say a mathematical expression.")
    expression = recognize_speech()
    if expression:
        result = calculate(expression)
        if result is not None:
            print(f"Result: {result}")
            speak(f"The result is {result}")

if __name__ == "__main__":
    main()
