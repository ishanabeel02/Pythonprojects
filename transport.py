import json
from datetime import datetime


class TransportSystem:
    def __init__(self):
        self.vehicles = {}
        self.routes = {}
        self.bookings = {}
        self.load_data()

    def load_data(self):
        try:
            with open('transport_data.json') as f:
                data = json.load(f)
                self.vehicles = data.get('vehicles', {})
                self.routes = data.get('routes', {})
                self.bookings = data.get('bookings', {})
        except FileNotFoundError:
            pass

    def save_data(self):
        with open('transport_data.json', 'w') as f:
            json.dump({
                'vehicles': self.vehicles,
                'routes': self.routes,
                'bookings': self.bookings
            }, f)

    def add_vehicle(self, vehicle_id, vehicle_type, capacity, status="Available"):
        self.vehicles[vehicle_id] = {
            'type': vehicle_type,
            'capacity': capacity,
            'status': status,
            'last_maintenance': datetime.now().strftime("%Y-%m-%d")
        }
        return f"Vehicle {vehicle_id} added successfully"

    def add_route(self, route_id, origin, destination, distance, duration):
        self.routes[route_id] = {
            'origin': origin,
            'destination': destination,
            'distance': distance,
            'duration': duration,
            'stops': []
        }
        return f"Route {route_id} added: {origin} to {destination}"

    def add_stop(self, route_id, stop_name):
        if route_id not in self.routes:
            return "Route not found"
        self.routes[route_id]['stops'].append(stop_name)
        return f"Stop '{stop_name}' added to route {route_id}"

    def book_ticket(self, booking_id, passenger_name, route_id, vehicle_id, seat_num):
        if route_id not in self.routes or vehicle_id not in self.vehicles:
            return "Invalid route or vehicle"

        if self.vehicles[vehicle_id]['status'] != "Available":
            return "Vehicle not available"

        self.bookings[booking_id] = {
            'passenger': passenger_name,
            'route': route_id,
            'vehicle': vehicle_id,
            'seat': seat_num,
            'date': datetime.now().strftime("%Y-%m-%d"),
            'status': "Confirmed"
        }

        self.vehicles[vehicle_id]['status'] = "Booked"
        return f"Booking confirmed for {passenger_name} on vehicle {vehicle_id}"

    def complete_trip(self, vehicle_id):
        if vehicle_id not in self.vehicles:
            return "Vehicle not found"

        self.vehicles[vehicle_id]['status'] = "Available"
        self.vehicles[vehicle_id]['last_maintenance'] = datetime.now().strftime("%Y-%m-%d")

        # Mark all bookings for this vehicle as completed
        for booking_id, booking in self.bookings.items():
            if booking['vehicle'] == vehicle_id and booking['status'] == "Confirmed":
                self.bookings[booking_id]['status'] = "Completed"

        return f"Trip completed for vehicle {vehicle_id}"

    def get_vehicle_status(self, vehicle_id):
        if vehicle_id not in self.vehicles:
            return "Vehicle not found"

        vehicle = self.vehicles[vehicle_id]
        status = f"\nVehicle {vehicle_id} Status:\n"
        status += f"Type: {vehicle['type']}\n"
        status += f"Capacity: {vehicle['capacity']}\n"
        status += f"Current Status: {vehicle['status']}\n"
        status += f"Last Maintenance: {vehicle['last_maintenance']}\n"

        # Get bookings for this vehicle
        bookings = [b for b in self.bookings.values() if b['vehicle'] == vehicle_id]
        if bookings:
            status += "\nBookings:\n"
            for b in bookings:
                status += f"- {b['passenger']} (Seat {b['seat']}, Status: {b['status']})\n"

        return status

    def get_route_details(self, route_id):
        if route_id not in self.routes:
            return "Route not found"

        route = self.routes[route_id]
        details = f"\nRoute {route_id} Details:\n"
        details += f"From: {route['origin']}\n"
        details += f"To: {route['destination']}\n"
        details += f"Distance: {route['distance']} km\n"
        details += f"Duration: {route['duration']} hours\n"

        if route['stops']:
            details += f"\nStops: {', '.join(route['stops'])}\n"

        return details


def main():
    system = TransportSystem()

    # Sample data if empty
    if not system.vehicles:
        system.add_vehicle("V001", "Bus", 50)
        system.add_vehicle("V002", "Minibus", 20)
        system.add_route("R001", "New York", "Boston", 350, 5)
        system.add_stop("R001", "Hartford")
        system.book_ticket("B001", "John Doe", "R001", "V001", "12A")

    while True:
        print("\nTransport Management System")
        print("1. Add Vehicle")
        print("2. Add Route")
        print("3. Add Stop to Route")
        print("4. Book Ticket")
        print("5. Complete Trip")
        print("6. View Vehicle Status")
        print("7. View Route Details")
        print("8. Exit")

        choice = input("Enter choice (1-8): ")

        if choice == "1":
            vid = input("Vehicle ID: ")
            vtype = input("Vehicle Type: ")
            cap = input("Capacity: ")
            print(system.add_vehicle(vid, vtype, cap))

        elif choice == "2":
            rid = input("Route ID: ")
            origin = input("Origin: ")
            dest = input("Destination: ")
            dist = input("Distance (km): ")
            dur = input("Duration (hours): ")
            print(system.add_route(rid, origin, dest, dist, dur))

        elif choice == "3":
            rid = input("Route ID: ")
            stop = input("Stop Name: ")
            print(system.add_stop(rid, stop))

        elif choice == "4":
            bid = input("Booking ID: ")
            name = input("Passenger Name: ")
            rid = input("Route ID: ")
            vid = input("Vehicle ID: ")
            seat = input("Seat Number: ")
            print(system.book_ticket(bid, name, rid, vid, seat))

        elif choice == "5":
            vid = input("Vehicle ID: ")
            print(system.complete_trip(vid))

        elif choice == "6":
            vid = input("Vehicle ID: ")
            print(system.get_vehicle_status(vid))

        elif choice == "7":
            rid = input("Route ID: ")
            print(system.get_route_details(rid))

        elif choice == "8":
            system.save_data()
            print("Data saved. Goodbye!")
            break

        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()