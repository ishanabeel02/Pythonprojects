import os
import time

MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
    'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
    '.': '.-.-.-', ',': '--..--', '?': '..--..', "'": '.----.', '!': '-.-.--',
    '/': '-..-.', '(': '-.--.', ')': '-.--.-', '&': '.-...', ':': '---...',
    ';': '-.-.-.', '=': '-...-', '+': '.-.-.', '-': '-....-', '_': '..--.-',
    '"': '.-..-.', '$': '...-..-', '@': '.--.-.', ' ': '/'
}

# Reverse mapping for decoding
MORSE_CODE_REVERSE = {v: k for k, v in MORSE_CODE_DICT.items()}

class MorseCodeTranslator:
    def __init__(self):
        self.history = []

    def encode(self, message):
        encoded = ' '.join(MORSE_CODE_DICT.get(ch.upper(), '') for ch in message)
        self.history.append((message, encoded))
        return encoded

    def decode(self, morse_message):
        decoded = ''.join(MORSE_CODE_REVERSE.get(code, '') for code in morse_message.split(' '))
        self.history.append((morse_message, decoded))
        return decoded

    def show_history(self):
        if not self.history:
            print("📭 No translations yet.")
            return
        print("\n📜 Translation History:")
        for i, (inp, outp) in enumerate(self.history, start=1):
            print(f"{i}. {inp} → {outp}")


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    translator = MorseCodeTranslator()

    while True:
        clear_screen()
        print("""
=============================
   Morse Code Translator
=============================
1. Encode Text → Morse
2. Decode Morse → Text
3. Show History
4. Quit
""")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            text = input("Enter text to encode: ")
            result = translator.encode(text)
            print(f"➡️ Morse Code: {result}")
            input("\nPress Enter to continue...")

        elif choice == "2":
            morse = input("Enter Morse code (separate letters with space, words with /): ")
            result = translator.decode(morse)
            print(f"➡️ Decoded Text: {result}")
            input("\nPress Enter to continue...")

        elif choice == "3":
            translator.show_history()
            input("\nPress Enter to continue...")

        elif choice == "4":
            print("👋 Goodbye!")
            break

        else:
            print("❌ Invalid choice!")
            time.sleep(1)


if __name__ == "__main__":
    main()