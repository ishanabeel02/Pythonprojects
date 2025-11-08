from googletrans import Translator
import os
import time

class LanguageTranslator:
    def __init__(self):
        self.translator = Translator()
        self.history = []

    def translate_text(self, text, src_lang, dest_lang):
        try:
            translation = self.translator.translate(text, src=src_lang, dest=dest_lang)
            result = translation.text
            self.history.append({
                "original": text,
                "src": src_lang,
                "dest": dest_lang,
                "translated": result
            })
            return result
        except Exception as e:
            return f"❌ Translation failed: {str(e)}"

    def show_history(self):
        if not self.history:
            print("📭 No translations yet.")
            return
        print("\n📜 Translation History:")
        for i, item in enumerate(self.history, start=1):
            print(f"{i}. [{item['src']} → {item['dest']}] {item['original']} → {item['translated']}")


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    translator = LanguageTranslator()

    while True:
        clear_screen()
        print("""
=============================
    🌍 Language Translator
=============================
1. Translate Text
2. Show History
3. Quit
""")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            text = input("Enter text to translate: ")
            src_lang = input("Enter source language (e.g., 'en' for English): ").strip()
            dest_lang = input("Enter target language (e.g., 'fr' for French): ").strip()

            print("Translating...")
            time.sleep(1)
            result = translator.translate_text(text, src_lang, dest_lang)
            print(f"➡️ Translated: {result}")
            input("\nPress Enter to continue...")

        elif choice == "2":
            translator.show_history()
            input("\nPress Enter to continue...")

        elif choice == "3":
            print("👋 Goodbye!")
            break

        else:
            print("❌ Invalid choice!")
            time.sleep(1)


if __name__ == "__main__":
    main()