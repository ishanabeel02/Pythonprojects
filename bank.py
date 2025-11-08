"""
Simple Banking System (single-file)
Features:
- Create account (name, initial deposit, 4-digit PIN)
- Login / Logout
- Check balance
- Deposit
- Withdraw (requires OTP)
- Transfer to other account (requires OTP)
- Pay bill (requires OTP)
- View transaction history
- Change PIN
- Delete account
Persistence: accounts.json
"""

import json
import os
import uuid
import hashlib
import random
import time
from datetime import datetime, timedelta

DB_FILE = "accounts.json"
OTP_EXPIRY_SECONDS = 120  # OTP valid for 2 minutes


def load_db():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        return json.load(f)


def save_db(db):
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=2)


def hash_pin(pin: str, salt: str):
    return hashlib.sha256((pin + salt).encode()).hexdigest()


def generate_account_number():
    # human-readable shorter UUID
    return str(uuid.uuid4())[:8]


def now_str():
    return datetime.utcnow().isoformat() + "Z"


class OTPManager:
    def __init__(self):
        # store otp -> (value, expires_at)
        self._store = {}

    def create_otp(self, account_no):
        val = f"{random.randint(100000, 999999)}"  # 6-digit
        expires_at = time.time() + OTP_EXPIRY_SECONDS
        self._store[account_no] = (val, expires_at)
        # in real world: send via SMS/email. Here we'll print to console.
        print(f"[SYSTEM] OTP for account {account_no}: {val} (valid for {OTP_EXPIRY_SECONDS}s)")
        return val

    def verify_otp(self, account_no, otp_input):
        rec = self._store.get(account_no)
        if not rec:
            return False, "No OTP requested."
        val, expires_at = rec
        if time.time() > expires_at:
            del self._store[account_no]
            return False, "OTP expired."
        if otp_input == val:
            del self._store[account_no]
            return True, "OTP verified."
        return False, "Incorrect OTP."


otp_manager = OTPManager()


class Bank:
    def __init__(self):
        self.db = load_db()  # dict: account_no -> account_data
        # ensure structure
        self.db.setdefault("_meta", {"created_at": now_str()})
        save_db(self.db)

    def create_account(self, name: str, pin: str, initial_deposit: float = 0.0):
        if not (pin.isdigit() and len(pin) == 4):
            raise ValueError("PIN must be 4 digits.")
        account_no = generate_account_number()
        salt = uuid.uuid4().hex
        hashed = hash_pin(pin, salt)
        account = {
            "name": name,
            "salt": salt,
            "pin_hash": hashed,
            "balance": round(float(initial_deposit), 2),
            "transactions": [
                {"time": now_str(), "type": "CREATE", "amount": round(float(initial_deposit), 2),
                 "desc": "Account created"}
            ],
            "created_at": now_str(),
        }
        self.db[account_no] = account
        save_db(self.db)
        return account_no

    def authenticate(self, account_no: str, pin: str):
        acc = self.db.get(account_no)
        if not acc:
            return False
        expected = acc["pin_hash"]
        salt = acc["salt"]
        return hash_pin(pin, salt) == expected

    def get_account(self, account_no):
        return self.db.get(account_no)

    def deposit(self, account_no: str, amount: float, desc="Deposit"):
        acc = self.get_account(account_no)
        if not acc:
            raise ValueError("Account not found.")
        amount = round(float(amount), 2)
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        acc["balance"] = round(acc["balance"] + amount, 2)
        acc["transactions"].append({"time": now_str(), "type": "DEPOSIT", "amount": amount, "desc": desc})
        save_db(self.db)

    def withdraw(self, account_no: str, amount: float, desc="Withdrawal"):
        acc = self.get_account(account_no)
        if not acc:
            raise ValueError("Account not found.")
        amount = round(float(amount), 2)
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if acc["balance"] < amount:
            raise ValueError("Insufficient funds.")
        acc["balance"] = round(acc["balance"] - amount, 2)
        acc["transactions"].append({"time": now_str(), "type": "WITHDRAW", "amount": -amount, "desc": desc})
        save_db(self.db)

    def transfer(self, from_acc: str, to_acc: str, amount: float):
        if from_acc == to_acc:
            raise ValueError("Cannot transfer to same account.")
        a_from = self.get_account(from_acc)
        a_to = self.get_account(to_acc)
        if not a_from or not a_to:
            raise ValueError("One or both accounts not found.")
        amount = round(float(amount), 2)
        if amount <= 0:
            raise ValueError("Transfer amount must be positive.")
        if a_from["balance"] < amount:
            raise ValueError("Insufficient funds.")
        a_from["balance"] = round(a_from["balance"] - amount, 2)
        a_to["balance"] = round(a_to["balance"] + amount, 2)
        now = now_str()
        a_from["transactions"].append({"time": now, "type": "TRANSFER_OUT", "amount": -amount, "desc": f"To {to_acc}"})
        a_to["transactions"].append({"time": now, "type": "TRANSFER_IN", "amount": amount, "desc": f"From {from_acc}"})
        save_db(self.db)

    def pay_bill(self, account_no: str, biller: str, amount: float):
        desc = f"Bill Payment to {biller}"
        self.withdraw(account_no, amount, desc=desc)

    def change_pin(self, account_no: str, new_pin: str):
        if not (new_pin.isdigit() and len(new_pin) == 4):
            raise ValueError("PIN must be 4 digits.")
        acc = self.get_account(account_no)
        if not acc:
            raise ValueError("Account not found.")
        salt = uuid.uuid4().hex
        acc["salt"] = salt
        acc["pin_hash"] = hash_pin(new_pin, salt)
        acc["transactions"].append({"time": now_str(), "type": "PIN_CHANGE", "amount": 0, "desc": "PIN changed"})
        save_db(self.db)

    def delete_account(self, account_no: str):

        if account_no in self.db:
            del self.db[account_no]
            save_db(self.db)
        else:
            raise ValueError("Account not found.")


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def pause(msg="Press Enter to continue..."):
    input(msg)


def pretty_transactions(txns):
    lines = []
    for t in txns[-10:][::-1]:  # show last 10, newest first
        time_s = t.get("time", "")
        typ = t.get("type", "")
        amt = t.get("amount", 0)
        desc = t.get("desc", "")
        lines.append(f"{time_s} | {typ:12} | {amt:8} | {desc}")
    return "\n".join(lines) if lines else "(no transactions)"


def main_menu():
    print("=== Welcome to PyBank (toy) ===")
    print("1) Create account")
    print("2) Login")
    print("3) Exit")


def account_menu(name, acc_no):
    print(f"=== Dashboard: {name} ({acc_no}) ===")
    print("1) Check balance")
    print("2) Deposit")
    print("3) Withdraw (OTP)")
    print("4) Transfer (OTP)")
    print("5) Pay bill (OTP)")
    print("6) Transaction history")
    print("7) Change PIN")
    print("8) Delete account")
    print("9) Logout")


def input_money(prompt="Amount: "):
    try:
        s = input(prompt).strip()
        return round(float(s), 2)
    except:
        raise ValueError("Invalid amount.")


def run_console():
    bank = Bank()
    session = {"logged_in": False, "acc_no": None, "name": None}

    while True:
        clear_screen()
        if not session["logged_in"]:
            main_menu()
            choice = input("Choose: ").strip()
            if choice == "1":
                name = input("Full name: ").strip()
                pin = input("4-digit PIN: ").strip()
                try:
                    init_dep = input("Initial deposit (leave blank for 0): ").strip()
                    init_dep = float(init_dep) if init_dep else 0.0
                except:
                    print("Invalid initial deposit.")
                    pause()
                    continue
                try:
                    acc_no = bank.create_account(name, pin, initial_deposit=init_dep)
                    print(f"Account created! Account number: {acc_no}")
                except Exception as e:
                    print("Error:", e)
                pause()
            elif choice == "2":
                acc_no = input("Account number: ").strip()
                pin = input("PIN: ").strip()
                if bank.authenticate(acc_no, pin):
                    acc = bank.get_account(acc_no)
                    session.update({"logged_in": True, "acc_no": acc_no, "name": acc["name"]})
                    print("Login successful.")
                else:
                    print("Authentication failed.")
                pause()
            elif choice == "3":
                print("Goodbye 👋")
                break
            else:
                print("Invalid choice.")
                pause()
        else:
            clear_screen()
            account_menu(session["name"], session["acc_no"])
            choice = input("Choose: ").strip()
            acc_no = session["acc_no"]
            try:
                if choice == "1":
                    acc = bank.get_account(acc_no)
                    print(f"Balance: Rs. {acc['balance']:.2f}")
                    pause()
                elif choice == "2":
                    amount = input_money("Deposit amount: ")
                    bank.deposit(acc_no, amount)
                    print("Deposit successful.")
                    pause()
                elif choice == "3":
                    amount = input_money("Withdrawal amount: ")
                    # OTP flow
                    otp_manager.create_otp(acc_no)
                    otp_input = input("Enter OTP (check system output): ").strip()
                    ok, msg = otp_manager.verify_otp(acc_no, otp_input)
                    if not ok:
                        print("OTP failed:", msg)
                        pause()
                        continue
                    bank.withdraw(acc_no, amount)
                    print("Withdrawal successful.")
                    pause()
                elif choice == "4":
                    target = input("Target account number: ").strip()
                    amount = input_money("Transfer amount: ")
                    otp_manager.create_otp(acc_no)
                    otp_input = input("Enter OTP: ").strip()
                    ok, msg = otp_manager.verify_otp(acc_no, otp_input)
                    if not ok:
                        print("OTP failed:", msg)
                        pause()
                        continue
                    bank.transfer(acc_no, target, amount)
                    print("Transfer successful.")
                    pause()
                elif choice == "5":
                    biller = input("Biller name: ").strip()
                    amount = input_money("Bill amount: ")
                    otp_manager.create_otp(acc_no)
                    otp_input = input("Enter OTP: ").strip()
                    ok, msg = otp_manager.verify_otp(acc_no, otp_input)
                    if not ok:
                        print("OTP failed:", msg)
                        pause()
                        continue
                    bank.pay_bill(acc_no, biller, amount)
                    print("Bill paid successfully.")
                    pause()
                elif choice == "6":
                    acc = bank.get_account(acc_no)
                    print("--- Transactions (latest first) ---")
                    print(pretty_transactions(acc.get("transactions", [])))
                    pause()
                elif choice == "7":
                    old = input("Current PIN: ").strip()
                    if not bank.authenticate(acc_no, old):
                        print("Wrong current PIN.")
                        pause()
                        continue
                    new_pin = input("New 4-digit PIN: ").strip()
                    bank.change_pin(acc_no, new_pin)
                    print("PIN changed.")
                    pause()
                elif choice == "8":
                    confirm = input("Are you sure? Type DELETE to confirm: ").strip()
                    if confirm == "DELETE":
                        # require OTP for deletion
                        otp_manager.create_otp(acc_no)
                        otp_input = input("Enter OTP: ").strip()
                        ok, msg = otp_manager.verify_otp(acc_no, otp_input)
                        if not ok:
                            print("OTP failed:", msg)
                            pause()
                            continue
                        bank.delete_account(acc_no)
                        print("Account deleted. Logging out.")
                        session = {"logged_in": False, "acc_no": None, "name": None}
                        pause()
                    else:
                        print("Deletion cancelled.")
                        pause()
                elif choice == "9":
                    session = {"logged_in": False, "acc_no": None, "name": None}
                else:
                    print("Invalid choice.")
                    pause()
            except Exception as e:
                print("Error:", e)
                pause()


if __name__ == "__main__":
    run_console()

