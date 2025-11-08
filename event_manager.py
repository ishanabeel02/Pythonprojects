import json
from datetime import datetime


class EventManager:
    def __init__(self):
        self.events = {}
        self.attendees = {}
        self.load_data()

    def load_data(self):
        try:
            with open('event_data.json') as f:
                data = json.load(f)
                self.events = data.get('events', {})
                self.attendees = data.get('attendees', {})
        except FileNotFoundError:
            pass

    def save_data(self):
        with open('event_data.json', 'w') as f:
            json.dump({
                'events': self.events,
                'attendees': self.attendees
            }, f)

    def create_event(self, event_id, name, date, capacity, description=""):
        if event_id in self.events:
            return "Event ID already exists"

        self.events[event_id] = {
            'name': name,
            'date': date,
            'capacity': capacity,
            'registered': 0,
            'description': description,
            'attendees': []
        }
        return f"Event '{name}' created successfully"

    def register_attendee(self, attendee_id, name, email, event_id):
        if event_id not in self.events:
            return "Event not found"

        if self.events[event_id]['registered'] >= self.events[event_id]['capacity']:
            return "Event is full"

        if attendee_id in self.attendees:
            return "Attendee ID already exists"

        self.attendees[attendee_id] = {
            'name': name,
            'email': email,
            'events': [event_id]
        }

        self.events[event_id]['attendees'].append(attendee_id)
        self.events[event_id]['registered'] += 1
        return f"{name} registered for {self.events[event_id]['name']}"

    def get_event_details(self, event_id):
        if event_id not in self.events:
            return "Event not found"

        event = self.events[event_id]
        details = f"\n=== {event['name']} ===\n"
        details += f"Date: {event['date']}\n"
        details += f"Capacity: {event['registered']}/{event['capacity']}\n"
        details += f"Description: {event['description']}\n"
        details += "Attendees:\n"

        for attendee_id in event['attendees']:
            attendee = self.attendees[attendee_id]
            details += f"- {attendee['name']} ({attendee['email']})\n"

        return details

    def get_attendee_events(self, attendee_id):
        if attendee_id not in self.attendees:
            return "Attendee not found"

        attendee = self.attendees[attendee_id]
        events = f"\nEvents for {attendee['name']}:\n"

        for event_id in attendee['events']:
            event = self.events[event_id]
            events += f"- {event['name']} on {event['date']}\n"

        return events

    def list_upcoming_events(self):
        today = datetime.now().strftime("%Y-%m-%d")
        upcoming = []

        for event_id, event in self.events.items():
            if event['date'] >= today:
                upcoming.append((event_id, event))

        if not upcoming:
            return "No upcoming events"

        upcoming.sort(key=lambda x: x[1]['date'])
        report = "\n=== Upcoming Events ===\n"

        for event_id, event in upcoming:
            report += f"{event_id}: {event['name']} ({event['date']}) - {event['registered']}/{event['capacity']}\n"

        return report


def main():
    manager = EventManager()

    # Sample data if empty
    if not manager.events:
        manager.create_event("E001", "Tech Conference", "2023-12-15", 100, "Annual technology conference")
        manager.create_event("E002", "Music Festival", "2023-11-20", 500, "Summer music festival")
        manager.register_attendee("A001", "John Doe", "john@example.com", "E001")
        manager.register_attendee("A002", "Jane Smith", "jane@example.com", "E001")

    while True:
        print("\nEvent Management System")
        print("1. Create Event")
        print("2. Register Attendee")
        print("3. View Event Details")
        print("4. View Attendee Events")
        print("5. List Upcoming Events")
        print("6. Exit")

        choice = input("Enter choice (1-6): ")

        if choice == "1":
            event_id = input("Enter event ID: ")
            name = input("Event name: ")
            date = input("Date (YYYY-MM-DD): ")
            capacity = int(input("Capacity: "))
            description = input("Description: ")
            print(manager.create_event(event_id, name, date, capacity, description))

        elif choice == "2":
            attendee_id = input("Attendee ID: ")
            name = input("Full name: ")
            email = input("Email: ")
            event_id = input("Event ID: ")
            print(manager.register_attendee(attendee_id, name, email, event_id))

        elif choice == "3":
            event_id = input("Enter event ID: ")
            print(manager.get_event_details(event_id))

        elif choice == "4":
            attendee_id = input("Enter attendee ID: ")
            print(manager.get_attendee_events(attendee_id))

        elif choice == "5":
            print(manager.list_upcoming_events())

        elif choice == "6":
            manager.save_data()
            print("Data saved. Goodbye!")
            break

        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()