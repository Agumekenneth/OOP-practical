from abc import ABC, abstractmethod

class BankAccount(ABC):
    def __init__(self, account_number, balance=0):
        self._account_number = account_number
        self._balance = balance

    @property
    def account_number(self):
        return self._account_number

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, amount):
        if amount >= 0:
            self._balance = amount
        else:
            print("Balance cannot be negative")

    @abstractmethod
    def deposit(self, amount):
        pass

    @abstractmethod
    def withdraw(self, amount):
        pass

    @abstractmethod
    def check_balance(self):
        pass

class SavingsAccount(BankAccount):
    def __init__(self, account_number, balance=0, interest_rate=0.05):
        super().__init__(account_number, balance)
        self._interest_rate = interest_rate

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"Deposited UGX {amount} to savings account {self.account_number}. New balance: UGX {self.balance}")
        else:
            print("Invalid deposit amount")

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            print(f"Withdrew UGX {amount} from savings account {self.account_number}. New balance: UGX {self.balance}")
        else:
            print("Invalid withdrawal amount or insufficient balance")

    def check_balance(self):
        print(f"Savings Account {self.account_number} balance: UGX {self.balance}")

    def calculate_interest(self):
        interest = self.balance * self._interest_rate
        self.deposit(interest)
        print(f"Interest of UGX {interest} added. New balance: UGX {self.balance}")

class CheckingAccount(BankAccount):
    def __init__(self, account_number, balance=0, overdraft_limit=50000):
        super().__init__(account_number, balance)
        self._overdraft_limit = overdraft_limit

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"Deposited UGX {amount} to checking account {self.account_number}. New balance: UGX {self.balance}")
        else:
            print("Invalid deposit amount")

    def withdraw(self, amount):
        if 0 < amount <= self.balance + self._overdraft_limit:
            self.balance -= amount
            print(f"Withdrew UGX {amount} from checking account {self.account_number}. New balance: UGX {self.balance}")
        else:
            print("Withdrawal amount exceeds overdraft limit")

    def check_balance(self):
        print(f"Checking Account {self.account_number} balance: UGX {self.balance}")

# Dictionary to hold accounts
accounts = {}

def create_account():
    account_type = input("Enter account type (savings/checking): ").strip().lower()
    account_number = input("Enter account number: ").strip()
    if account_number in accounts:
        print("Account number already exists.")
        return
    if account_type == "savings":
        accounts[account_number] = SavingsAccount(account_number)
    elif account_type == "checking":
        accounts[account_number] = CheckingAccount(account_number)
    else:
        print("Invalid account type. Please choose 'savings' or 'checking'.")
        return
    print(f"{account_type.capitalize()} account {account_number} created.")

def deposit():
    account_number = input("Enter account number: ").strip()
    amount = float(input("Enter deposit amount: "))
    if account_number in accounts:
        accounts[account_number].deposit(amount)
    else:
        print("Account not found.")

def withdraw():
    account_number = input("Enter account number: ").strip()
    amount = float(input("Enter withdrawal amount: "))
    if account_number in accounts:
        accounts[account_number].withdraw(amount)
    else:
        print("Account not found.")

def check_balance():
    account_number = input("Enter account number: ").strip()
    if account_number in accounts:
        accounts[account_number].check_balance()
    else:
        print("Account not found.")

def user_interface():
    while True:
        print("\n--- Bank Account Manager ---")
        print("1. Create Account")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Check Balance")
        print("5. Exit")

        choice = input("Select an action (1-5): ").strip()

        if choice == '1':
            create_account()
        elif choice == '2':
            deposit()
        elif choice == '3':
            withdraw()
        elif choice == '4':
            check_balance()
        elif choice == '5':
            print("Exiting the Bank Account Manager.")
            break
        else:
            print("Invalid choice. Please select a valid option.")

# Run the user interface
user_interface()
