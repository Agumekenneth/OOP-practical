from abc import ABC, abstractmethod
class BankAccount(ABC):
    def __init__(self, account_number, balance=0):
        self._account_number = account_number   
        self._balance = balance                 

    @property
    def account_number(self):
        """Read-only property for account number"""
        return self._account_number

    @property
    def balance(self):
        """Getter for balance"""
        return self._balance

    @balance.setter
    def balance(self, amount):
        """Setter for balance with validation"""
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

# Savings Account Class
class SavingsAccount(BankAccount):
    def __init__(self, account_number, balance=0, interest_rate=0.05):
        super().__init__(account_number, balance)
        self._interest_rate = interest_rate

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"Deposited UGX {amount} to savings account {self.account_number}. "
                  f"New balance: UGX {self.balance}")
        else:
            print("Invalid deposit amount")

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            print(f"Withdrew UGX {amount} from savings account {self.account_number}. "
                  f"New balance: UGX {self.balance}")
        else:
            print("Invalid withdrawal amount or insufficient balance")

    def check_balance(self):
        print(f"Savings Account {self.account_number} balance: UGX {self.balance}")

    def calculate_interest(self):
        interest = self.balance * self._interest_rate
        self.deposit(interest)
        print(f"Interest of UGX {interest} added. New balance: UGX {self.balance}")


# Checking Account Class
class CheckingAccount(BankAccount):
    def __init__(self, account_number, balance=0, overdraft_limit=50000):
        super().__init__(account_number, balance)
        self._overdraft_limit = overdraft_limit

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"Deposited UGX {amount} to checking account {self.account_number}. "
                  f"New balance: UGX {self.balance}")
        else:
            print("Invalid deposit amount")

    def withdraw(self, amount):
        if 0 < amount <= self.balance + self._overdraft_limit:
            self.balance -= amount
            print(f"Withdrew UGX {amount} from checking account {self.account_number}. "
                  f"New balance: UGX {self.balance}")
        else:
            print("Withdrawal amount exceeds overdraft limit")

    def check_balance(self):
        print(f"Checking Account {self.account_number} balance: UGX {self.balance}")

# Bank System Class
class BankSystem:
    def __init__(self):
        self.accounts = {}  # Dictionary to hold accounts

    def create_account(self):
        account_type = input("Enter account type (savings/checking): ").strip().lower()
        account_number = input("Enter account number: ").strip()

        if account_number in self.accounts:
            print("Account number already exists.")
            return

        if account_type == "savings":
            self.accounts[account_number] = SavingsAccount(account_number)
        elif account_type == "checking":
            self.accounts[account_number] = CheckingAccount(account_number)
        else:
            print("Invalid account type. Please choose 'savings' or 'checking'.")
            return

        print(f"{account_type.capitalize()} account {account_number} created.")

    def deposit(self):
        account_number = input("Enter account number: ").strip()
        amount = float(input("Enter deposit amount: "))
        if account_number in self.accounts:
            self.accounts[account_number].deposit(amount)
        else:
            print("Account not found.")

    def withdraw(self):
        account_number = input("Enter account number: ").strip()
        amount = float(input("Enter withdrawal amount: "))
        if account_number in self.accounts:
            self.accounts[account_number].withdraw(amount)
        else:
            print("Account not found.")

    def check_balance(self):
        account_number = input("Enter account number: ").strip()
        if account_number in self.accounts:
            self.accounts[account_number].check_balance()
        else:
            print("Account not found.")

    def user_interface(self):
        """Main user menu loop"""
        while True:
            print("\n--- Bank Account Manager ---")
            print("1. Create Account")
            print("2. Deposit")
            print("3. Withdraw")
            print("4. Check Balance")
            print("5. Exit")

            choice = input("Select an action (1-5): ").strip()

            if choice == '1':
                self.create_account()
            elif choice == '2':
                self.deposit()
            elif choice == '3':
                self.withdraw()
            elif choice == '4':
                self.check_balance()
            elif choice == '5':
                print("Exiting the Bank Account Manager.")
                break
            else:
                print("Invalid choice. Please select a valid option.")


# Main Program Entry
if __name__ == "__main__":
    bank = BankSystem()
    bank.user_interface()
