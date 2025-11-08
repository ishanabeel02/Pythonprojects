import random

class Question:
    def __init__(self, text, options, answer_letter):
        self.text = text
        self.options = options
        self.answer_letter = answer_letter  # "A", "B", "C", "D"

    def __str__(self):
        opts = "\n".join([f"{chr(65+i)}. {opt}" for i, opt in enumerate(self.options)])
        return f"{self.text}\n{opts}"

class QuizSystem:
    def __init__(self):
        self.categories = {
            "General": [
                Question("What is the capital of France?",
                         ["Berlin", "Madrid", "Paris", "Rome"], "C"),
                Question("Which planet is known as the Red Planet?",
                         ["Venus", "Mars", "Jupiter", "Saturn"], "B"),
                Question("What is the boiling point of water?",
                         ["90°C", "100°C", "120°C", "80°C"], "B"),
                Question("Which ocean is the deepest?",
                         ["Atlantic", "Indian", "Arctic", "Pacific"], "D"),
                Question("Who wrote '1984'?",
                         ["Austen", "Orwell", "Shakespeare", "Dickens"], "B"),
            ],
            "Science": [
                Question("What is H₂O commonly called?",
                         ["Hydrogen", "Oxygen", "Water", "Helium"], "C"),
                Question("What force keeps us on the ground?",
                         ["Magnetism", "Gravity", "Friction", "Electricity"], "B"),
                Question("What is the chemical symbol for gold?",
                         ["Au", "Ag", "Fe", "Pb"], "A"),
                Question("Speed of light is approx?",
                         ["3×10⁵ km/s", "3×10⁸ m/s", "3×10³ m/s", "3×10² km/s"], "B"),
                Question("What is the powerhouse of the cell?",
                         ["Nucleus", "Mitochondria", "Ribosome", "Chloroplast"], "B"),
            ],
            "History": [
                Question("Who was the first President of the USA?",
                         ["Lincoln", "Washington", "Jefferson", "Adams"], "B"),
                Question("In which year did WW2 end?",
                         ["1942", "1945", "1948", "1939"], "B"),
                Question("The Roman Empire fell in?",
                         ["476 AD", "1066 AD", "395 AD", "800 AD"], "A"),
                Question("Who discovered America?",
                         ["Columbus", "Vespucci", "Magellan", "Cook"], "A"),
                Question("The Magna Carta was signed in?",
                         ["1215", "1315", "1415", "1515"], "A"),
            ]
        }
        self.results = []

    def list_categories(self):
        print("\nCategories:")
        for idx, cat in enumerate(self.categories.keys()):
            print(f"{idx+1}. {cat}")

    def add_question(self):
        print("\n--- Add Question ---")
        self.list_categories()
        cat_choice = input("Enter category name or number: ").strip()
        if cat_choice.isdigit():
            cat_list = list(self.categories.keys())
            cat_idx = int(cat_choice) - 1
            if 0 <= cat_idx < len(cat_list):
                category = cat_list[cat_idx]
            else:
                print("Invalid category number.")
                return
        else:
            category = cat_choice
            if category not in self.categories:
                self.categories[category] = []
        text = input("Enter the question: ")
        options = []
        for i in range(4):
            opt = input(f"Enter option {chr(65+i)}: ")
            options.append(opt)
        ans_letter = input("Enter correct answer letter (A/B/C/D): ").strip().upper()
        if ans_letter not in ["A", "B", "C", "D"]:
            print("Invalid answer letter. Must be A, B, C, or D.")
            return
        q = Question(text, options, ans_letter)
        self.categories[category].append(q)
        print(f"Question added to '{category}' category.")

    def list_questions(self):
        print("\n--- List of Questions ---")
        for cat, questions in self.categories.items():
            print(f"\nCategory: {cat}")
            for idx, q in enumerate(questions):
                print(f"Q{idx+1}: {q.text}")
                for i, opt in enumerate(q.options):
                    print(f"{chr(65+i)}. {opt}")
                print(f"Answer: {q.answer_letter}")
                print("-" * 20)

    def take_quiz(self):
        print("\n--- Take Quiz ---")
        self.list_categories()
        cat_choice = input("Select category by name or number: ").strip()
        if cat_choice.isdigit():
            cat_list = list(self.categories.keys())
            cat_idx = int(cat_choice) - 1
            if 0 <= cat_idx < len(cat_list):
                category = cat_list[cat_idx]
            else:
                print("Invalid category number.")
                return
        else:
            category = cat_choice
            if category not in self.categories:
                print("Category not found.")
                return
        questions = self.categories[category]
        if not questions:
            print("No questions in this category.")
            return
        questions_copy = questions[:]
        random.shuffle(questions_copy)
        score = 0
        responses = []
        for idx, q in enumerate(questions_copy):
            print(f"\nQ{idx+1}:")
            print(q)
            resp = input("Your answer (A/B/C/D): ").strip().upper()
            if resp == q.answer_letter:
                print("Correct!")
                score += 1
            else:
                print(f"Incorrect! The correct answer was: {q.answer_letter}")
            responses.append((q.text, resp, q.answer_letter))
        print(f"\nQuiz completed! Your score: {score}/{len(questions_copy)}")
        self.results.append((category, score, len(questions_copy), responses))

    def view_results(self):
        print("\n--- Quiz Results ---")
        if not self.results:
            print("No results yet.")
            return
        for idx, res in enumerate(self.results):
            cat, score, total, answers = res
            print(f"Quiz {idx+1} | Category: {cat} | Score: {score}/{total}")
            for q_text, user_ans, correct_ans in answers:
                print(f"Q: {q_text}\nYour Answer: {user_ans}, Correct: {correct_ans}")
            print("-" * 30)

    def menu(self):
        while True:
            print("\n=== Quiz System ===")
            print("1. List Categories")
            print("2. Add Question")
            print("3. List Questions")
            print("4. Take Quiz")
            print("5. View Results")
            print("6. Exit")
            choice = input("Enter your choice: ")
            if choice == "1":
                self.list_categories()
            elif choice == "2":
                self.add_question()
            elif choice == "3":
                self.list_questions()
            elif choice == "4":
                self.take_quiz()
            elif choice == "5":
                self.view_results()
            elif choice == "6":
                print("Exiting Quiz System. Goodbye!")
                break
            else:
                print("Invalid choice. Try again!")

if __name__ == "__main__":
    quiz = QuizSystem()
    quiz.menu()