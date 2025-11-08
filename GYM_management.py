import json
from datetime import datetime, timedelta


class GymManagement:
    def __init__(self):
        self.members = {}
        self.workouts = {}
        self.payments = {}
        self.load_data()

    def load_data(self):
        try:
            with open('gym_data.json') as f:
                data = json.load(f)
                self.members = data.get('members', {})
                self.workouts = data.get('workouts', {})
                self.payments = data.get('payments', {})
        except FileNotFoundError:
            pass

    def save_data(self):
        with open('gym_data.json', 'w') as f:
            json.dump({
                'members': self.members,
                'workouts': self.workouts,
                'payments': self.payments
            }, f)

    def add_member(self, member_id, name, phone, plan="Basic"):
        if member_id in self.members:
            return "Member ID already exists!"

        self.members[member_id] = {
            'name': name,
            'phone': phone,
            'plan': plan,
            'join_date': datetime.now().strftime("%Y-%m-%d"),
            'expiry_date': (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        }
        return f"Member {name} added successfully!"

    def log_workout(self, member_id, workout_type, duration):
        if member_id not in self.members:
            return "Member not found!"

        workout_id = str(len(self.workouts) + 1)
        self.workouts[workout_id] = {
            'member_id': member_id,
            'type': workout_type,
            'duration': duration,
            'date': datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        return f"Workout logged for {self.members[member_id]['name']}"

    def record_payment(self, member_id, amount):
        if member_id not in self.members:
            return "Member not found!"

        payment_id = str(len(self.payments) + 1)
        self.payments[payment_id] = {
            'member_id': member_id,
            'amount': amount,
            'date': datetime.now().strftime("%Y-%m-%d")
        }

        # Extend membership by 30 days
        expiry = datetime.strptime(self.members[member_id]['expiry_date'], "%Y-%m-%d")
        new_expiry = expiry + timedelta(days=30)
        self.members[member_id]['expiry_date'] = new_expiry.strftime("%Y-%m-%d")

        return f"Payment of ${amount} recorded. Membership extended to {new_expiry.strftime('%Y-%m-%d')}"

    def get_member_details(self, member_id):
        if member_id not in self.members:
            return "Member not found!"

        member = self.members[member_id]
        details = f"\n=== Member Details ===\n"
        details += f"Name: {member['name']}\n"
        details += f"Phone: {member['phone']}\n"
        details += f"Plan: {member['plan']}\n"
        details += f"Joined: {member['join_date']}\n"
        details += f"Expiry: {member['expiry_date']}\n"

        # Get workout history
        workouts = [w for w in self.workouts.values() if w['member_id'] == member_id]
        if workouts:
            details += "\nWorkout History:\n"
            for w in workouts:
                details += f"- {w['type']} ({w['duration']} mins) on {w['date']}\n"

        # Get payment history
        payments = [p for p in self.payments.values() if p['member_id'] == member_id]
        if payments:
            details += "\nPayment History:\n"
            for p in payments:
                details += f"- ${p['amount']} on {p['date']}\n"

        return details

    def get_active_members(self):
        today = datetime.now().strftime("%Y-%m-%d")
        active = [m for m in self.members.values() if m['expiry_date'] >= today]

        if not active:
            return "No active members!"

        report = "\n=== Active Members ===\n"
        for member_id, member in self.members.items():
            if member['expiry_date'] >= today:
                report += f"{member_id}: {member['name']} (Expires: {member['expiry_date']})\n"

        return report


def main():
    gym = GymManagement()

    # Sample data if empty
    if not gym.members:
        gym.add_member("M001", "John Doe", "555-1234", "Premium")
        gym.add_member("M002", "Jane Smith", "555-5678", "Basic")
        gym.log_workout("M001", "Cardio", 45)
        gym.log_workout("M001", "Weight Training", 60)
        gym.record_payment("M001", 50.00)

    while True:
        print("\nGYM Management System")
        print("1. Add Member")
        print("2. Log Workout")
        print("3. Record Payment")
        print("4. View Member Details")
        print("5. List Active Members")
        print("6. Exit")

        choice = input("Enter choice (1-6): ")

        if choice == "1":
            member_id = input("Member ID: ")
            name = input("Name: ")
            phone = input("Phone: ")
            plan = input("Plan (Basic/Premium): ")
            print(gym.add_member(member_id, name, phone, plan))

        elif choice == "2":
            member_id = input("Member ID: ")
            workout_type = input("Workout Type: ")
            duration = input("Duration (mins): ")
            print(gym.log_workout(member_id, workout_type, duration))

        elif choice == "3":
            member_id = input("Member ID: ")
            amount = float(input("Amount: $"))
            print(gym.record_payment(member_id, amount))

        elif choice == "4":
            member_id = input("Member ID: ")
            print(gym.get_member_details(member_id))

        elif choice == "5":
            print(gym.get_active_members())

        elif choice == "6":
            gym.save_data()
            print("Data saved. Goodbye!")
            break

        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()