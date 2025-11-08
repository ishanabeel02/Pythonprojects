import datetime

class Flight:
    def __init__(self, flight_no, origin, destination, departure_time, seats):
        self.flight_no = flight_no
        self.origin = origin
        self.destination = destination
        self.departure_time = departure_time
        self.seats = seats
        self.booked_seats = {}

    def book_seat(self, passenger):
        for seat in range(1, self.seats + 1):
            if seat not in self.booked_seats:
                self.booked_seats[seat] = passenger
                return seat
        return None

    def cancel_seat(self, seat_no):
        if seat_no in self.booked_seats:
            del self.booked_seats[seat_no]
            return True
        return False

    def available_seats(self):
        return self.seats - len(self.booked_seats)

    def __str__(self):
        return f"{self.flight_no}: {self.origin} -> {self.destination}, {self.departure_time}, Seats: {self.available_seats()}/{self.seats}"

class Passenger:
    def __init__(self, name, passport_no):
        self.name = name
        self.passport_no = passport_no

    def __str__(self):
        return f"{self.name} (Passport: {self.passport_no})"

class Booking:
    def __init__(self, flight, passenger, seat_no):
        self.flight = flight
        self.passenger = passenger
        self.seat_no = seat_no
        self.booking_time = datetime.datetime.now()

    def __str__(self):
        return f"Booking: {self.passenger} on Flight {self.flight.flight_no}, Seat {self.seat_no}, Time: {self.booking_time.strftime('%Y-%m-%d %H:%M:%S')}"

class AirlineSystem:
    def __init__(self):
        self.flights = []
        self.passengers = []
        self.bookings = []

    def add_flight(self):
        print("\n--- Add Flight ---")
        flight_no = input("Flight Number: ")
        origin = input("Origin: ")
        destination = input("Destination: ")
        departure_time = input("Departure Time (YYYY-MM-DD HH:MM): ")
        seats = int(input("Total Seats: "))
        flight = Flight(flight_no, origin, destination, departure_time, seats)
        self.flights.append(flight)
        print(f"Flight {flight_no} added.")

    def list_flights(self):
        print("\n--- List of Flights ---")
        for flight in self.flights:
            print(flight)

    def add_passenger(self):
        print("\n--- Add Passenger ---")
        name = input("Name: ")
        passport_no = input("Passport Number: ")
        passenger = Passenger(name, passport_no)
        self.passengers.append(passenger)
        print(f"Passenger {name} added.")

    def list_passengers(self):
        print("\n--- List of Passengers ---")
        for p in self.passengers:
            print(p)

    def book_ticket(self):
        print("\n--- Book Ticket ---")
        self.list_flights()
        flight_no = input("Enter Flight Number to book: ")
        flight = next((f for f in self.flights if f.flight_no == flight_no), None)
        if not flight:
            print("Flight not found!")
            return
        self.list_passengers()
        passport_no = input("Enter Passenger Passport Number: ")
        passenger = next((p for p in self.passengers if p.passport_no == passport_no), None)
        if not passenger:
            print("Passenger not found!")
            return
        seat_no = flight.book_seat(passenger)
        if seat_no:
            booking = Booking(flight, passenger, seat_no)
            self.bookings.append(booking)
            print(f"Ticket booked: Seat {seat_no}")
        else:
            print("No seats available!")

    def list_bookings(self):
        print("\n--- List of Bookings ---")
        for booking in self.bookings:
            print(booking)

    def cancel_ticket(self):
        print("\n--- Cancel Ticket ---")
        self.list_bookings()
        flight_no = input("Enter Flight Number: ")
        seat_no = int(input("Enter Seat Number: "))
        booking = next((b for b in self.bookings if b.flight.flight_no == flight_no and b.seat_no == seat_no), None)
        if not booking:
            print("Booking not found!")
            return
        if booking.flight.cancel_seat(seat_no):
            self.bookings.remove(booking)
            print("Ticket canceled.")
        else:
            print("Cancellation failed.")

    def menu(self):
        while True:
            print("\n=== Airline Management System ===")
            print("1. Add Flight")
            print("2. List Flights")
            print("3. Add Passenger")
            print("4. List Passengers")
            print("5. Book Ticket")
            print("6. List Bookings")
            print("7. Cancel Ticket")
            print("8. Exit")
            choice = input("Enter choice: ")
            if choice == "1":
                self.add_flight()
            elif choice == "2":
                self.list_flights()
            elif choice == "3":
                self.add_passenger()
            elif choice == "4":
                self.list_passengers()
            elif choice == "5":
                self.book_ticket()
            elif choice == "6":
                self.list_bookings()
            elif choice == "7":
                self.cancel_ticket()
            elif choice == "8":
                print("Exiting system. Goodbye!")
                break
            else:
                print("Invalid choice!")

if __name__ == "__main__":
    system = AirlineSystem()
    system.menu()
