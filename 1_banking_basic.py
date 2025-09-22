# Objective
# You've been tasked by a local bank to create a simple bank account manager
# that can perform basic operations like deposit, withdrawal, and balance check.
# Use Object-Oriented Programming (OOP) to accomplish this.

# Step 1: Create BankAccount class
class BankAccount:
    def __init__(self, account_number, balance=0):
        self.account_number = account_number
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        print(f"Deposited {amount}. New balance: {self.balance}")

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            print(f"Withdrew {amount}. New balance: {self.balance}")
        else:
            print("Insufficient funds.")

    def check_balance(self):
        print(f"Account balance: {self.balance}")

# Step 2: Create a dictionary to store accounts
accounts = {} # k:V

# Step 3: User Interface
while True:
    print("\n1. Create Account")
    print("2. Deposit")
    print("3. Withdraw")
    print("4. Check Balance")
    print("5. Exit")

    choice = input("Choose an option: ")

    if choice == '1':
        account_number = input("Enter new account number: ")
        initial_balance = float(input("Enter initial balance: "))
        accounts[account_number] = BankAccount(account_number, initial_balance)
        #print(accounts["1"].balance)
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
    elif choice == '5':
        break
    else:
        print("Invalid choice.")