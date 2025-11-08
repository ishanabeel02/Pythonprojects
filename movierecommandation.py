import random

class Movie:
    def __init__(self, title, genre, year):
        self.title = title
        self.genre = genre
        self.year = year
        self.ratings = []

    def add_rating(self, rating):
        self.ratings.append(rating)

    def average_rating(self):
        if not self.ratings:
            return None
        return sum(self.ratings) / len(self.ratings)

    def __str__(self):
        avg = self.average_rating()
        rating_str = f"{avg:.1f}/5" if avg is not None else "No ratings"
        return f"{self.title} ({self.year}) [{self.genre}] - {rating_str}"

class MovieSystem:
    def __init__(self):
        self.movies = []
        self.add_sample_movies()

    def add_sample_movies(self):
        self.movies.append(Movie("The Shawshank Redemption", "Drama", 1994))
        self.movies.append(Movie("The Godfather", "Crime", 1972))
        self.movies.append(Movie("Inception", "Sci-Fi", 2010))
        self.movies.append(Movie("Titanic", "Romance", 1997))
        self.movies.append(Movie("The Dark Knight", "Action", 2008))
        self.movies.append(Movie("Forrest Gump", "Comedy", 1994))
        self.movies.append(Movie("Interstellar", "Sci-Fi", 2014))
        self.movies.append(Movie("La La Land", "Musical", 2016))
        self.movies.append(Movie("Parasite", "Thriller", 2019))
        self.movies.append(Movie("Gladiator", "Action", 2000))

    def list_movies(self):
        print("\n--- Movie List ---")
        for idx, m in enumerate(self.movies):
            print(f"{idx+1}. {m}")

    def add_movie(self):
        print("\n--- Add Movie ---")
        title = input("Movie Title: ")
        genre = input("Genre: ")
        year = input("Year: ")
        try:
            year = int(year)
        except ValueError:
            print("Invalid year.")
            return
        self.movies.append(Movie(title, genre, year))
        print(f"Movie '{title}' added.")

    def rate_movie(self):
        self.list_movies()
        idx = input("Select movie number to rate: ")
        try:
            idx = int(idx) - 1
            movie = self.movies[idx]
        except:
            print("Invalid selection.")
            return
        rating = input("Enter your rating (1-5): ")
        try:
            rating = float(rating)
            if not (1 <= rating <= 5):
                raise ValueError
        except:
            print("Invalid rating.")
            return
        movie.add_rating(rating)
        print(f"Rated '{movie.title}' {rating}/5.")

    def recommend_movies(self):
        print("\n--- Movie Recommendation ---")
        genre = input("Enter preferred genre: ").strip()
        rated_movies = [m for m in self.movies if m.average_rating() is not None]
        genre_movies = [m for m in rated_movies if m.genre.lower() == genre.lower()]
        if not genre_movies:
            print("No movies found in this genre with ratings. Try another genre or rate more movies!")
            return
        # Recommend top 3 by rating
        genre_movies.sort(key=lambda m: m.average_rating(), reverse=True)
        top_movies = genre_movies[:3]
        print(f"\nTop recommended movies for genre '{genre}':")
        for m in top_movies:
            print(f"- {m.title} ({m.year}) [Rating: {m.average_rating():.1f}/5]")

    def random_recommendation(self):
        print("\n--- Random Recommendation ---")
        unrated = [m for m in self.movies if m.average_rating() is None]
        if unrated:
            print("You haven't rated these movies yet. Consider watching:")
            for m in random.sample(unrated, min(3, len(unrated))):
                print(f"- {m.title} ({m.year}) [{m.genre}]")
        else:
            print("You've rated all movies! Here's a random pick:")
            print(random.choice(self.movies))

    def menu(self):
        while True:
            print("\n=== Movie Recommendation System ===")
            print("1. List Movies")
            print("2. Add Movie")
            print("3. Rate Movie")
            print("4. Get Recommendations (by Genre)")
            print("5. Random Recommendation")
            print("6. Exit")
            choice = input("Enter your choice: ")
            if choice == "1":
                self.list_movies()
            elif choice == "2":
                self.add_movie()
            elif choice == "3":
                self.rate_movie()
            elif choice == "4":
                self.recommend_movies()
            elif choice == "5":
                self.random_recommendation()
            elif choice == "6":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Try again.")

if __name__ == "__main__":
    msys = MovieSystem()
    msys.menu()