# Objective
# You've been tasked by a local bank to create a simple bank account manager
# that can perform basic operations like deposit, withdrawal, and balance check.
# Use Object-Oriented Programming (OOP) to accomplish this.

# Step 1: Create BankAccount class
class BankAccount:
    def __init__(self, account_number, balance=0):
        self.account_number = account_number
        self.name = name
        self.balance = balance
        self.history = []

    def deposit(self, amount):
        if amount < 0:
             print('Invalid deposit amount')
        else:
             self.balance += amount
             print(f"Deposited {amount}. New balance: {self.balance}")
             self.history.append(f"Deposited {amount}")

    def withdraw(self, amount):
        if amount <= 0:
            print("Invalid withdrawal amount.")
        elif self.balance >= amount:
            self.balance -= amount
            print(f"Withdrew {amount}. New balance: {self.balance}")
            self.history.append(f"Withdrew {amount}")
        else:
            print("Insufficient funds.")

    def check_balance(self):
        print(f"Account {self.account_number} ({self.name}) balance: {self.balance}")
  
    def apply_interest(self, rate):
        interest = self.balance * rate
        self.balance += interest
        print(f"Applied interest {interest}. New balance: {self.balance}")

    def show_history(self):
        print(f"Transaction history for account {self.account_number} ({self.name}):")
        if not self.history:
            print("No transactions yet.")
        else:
            for transaction in self.history:
                print(transaction)


# Step 2: Create a dictionary to store accounts
accounts = {} # k:V

# Step 3: User Interface
while True:
    print("\n1. Create Account")
    print("2. Deposit")
    print("3. Withdraw")
    print("4. Check Balance")
    print("5. Exit")
    print("6. Show Transaction History")
    print("7. Transfer Funds")

    choice = input("Choose an option: ")

    if choice == '1':
        account_number = input("Enter new account number: ")
        name = input("Enter account holder's name: ")
        initial_balance = float(input("Enter initial balance: "))
        accounts[account_number] = BankAccount(account_number, name, initial_balance)
        print("Account created.")
    elif choice == '2':
        account_number = input("Enter account number: ")
        amount = float(input("Enter amount to deposit: "))
        accounts[account_number].deposit(amount)
    elif choice == '3':
        account_number = input("Enter account number: ")
        amount = float(input("Enter amount to withdraw: "))
        accounts[account_number].withdraw(amount)
    elif choice == '4':
        account_number = input("Enter account number: ")
        accounts[account_number].check_balance()
    elif choice == '6':
        account_number = input("Enter account number: ")
        accounts[account_number].show_history()
    elif choice == '7':
        source = input("Enter source account number: ")
        dest = input("Enter destination account number: ")
        amount = float(input("Enter amount to transfer: "))
        if amount <= 0:
            print("Invalid transfer amount.")
        elif source not in accounts or dest not in accounts:
            print("One or both accounts not found.")
        elif accounts[source].balance < amount:
            print("Insufficient funds in source account.")
        else:
            accounts[source].balance -= amount
            accounts[dest].balance += amount
            accounts[source].history.append(f"Transferred {amount} to {dest}")
            accounts[dest].history.append(f"Received {amount} from {source}")
            print(f"Transferred {amount} from {source} to {dest}. New source balance: {accounts[source].balance}. New dest balance: {accounts[dest].balance}")
    elif choice == '5':
        break
    else:
        print("Invalid choice.")
    
