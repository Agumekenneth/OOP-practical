from abc import ABC, abstractmethod
class BankAccount(ABC):
    def __init__(self, account_number, balance = 0):
        self._acount_number = account_number
        self._balance = balance
    @property
    def account_number(self):
        return self._account_number
    @property
    def balance(self):
        return self._balance
    @balance.setter
    def balance(self,amount):
        if amount >= 0:
            self.balance = amount
        else:
            print("Balance can't be negative")
    @abstractmethod
    def deposit(self, amount):
        pass
class SavingsAccount(BankAccount):
    def __init__(self, account_number, balance = 0, interest_rate = 0.05):
            super().__init__(account_number, balance)
            self.interest_rate = interest_rate
    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"Deposited UGX {amount} to savings account {self.account_number}. New balance: UGX {self.balance}")
        else:
            print("Invalide deposit amount")
    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            print(f" Withdrew UGX {amount} from savings account {self.account_number}. New balance: UGX: {self.balance}")
        else:
            print("Invalid withdrawal amount or insufficient balance")
    def calaculate_interest(self):
        interest = self.balance * self.interest_rate
        self.deposit(interest)
        print(f"Interest of UGX {interest} added. New balance: UGX {self.balance}")
class CheckingAccount(BankAccount):
    def __init__(self, account_number, balance = 0, overdraft_limit = 5000):
        super().__init__(account_number, balance)
        self.overdraft_limit = overdraft_limit
    def deposit(self, amount):
        if 0 < amount <= self.balance + self.overdraft_limit:
            self.balance -= amount
            print(f"Withdrew UGX {amount}from checking account{self.account_number}. New balance{self.balance}:")
        else:
            print("Invalid withdrawal amount or exceeds overdraft limit")
    def check_balance(self):
        print(f"Checking Account {self.account_number} balance: UGX {self.balance}")
        
class BankSystem:
    def __init__(self):
        self.accounts = {}
    def create_account(self):
        account_type = input("Enter account type (savings/checking):").strip().lower()
        account_number = input('Enter account number:').strip()
        if account_number in self.accounts:
            print("Account number already exists.")
            return
        if account_type == 'savings':
            self.accounts[account_number] = SavingsAccount(account_number)
        elif account_type == 'checking':
            self.accounts[account_number] = CheckingAccount(account_number)
        else:
            print("Invalid account type. Please choose 'savings or 'checking'.")
        return
    print("{account_type.capitalize()} account {account_number} created.")
    def deposit(self):
        account_number =input('Enter account number:').strip()
        amount = float(input("Enter deposit amount:"))
        if account_number in self.accounts:
            self.accounts[account_number].deposit(amount)
        else:
            print("Account not found.")
    def withdraw(self):
        account_number = input("Enter account number:").strip()
        amount = float(input("Enter withdrawal amount:"))
        if account_number in self.accounts:
            self.accounts[account_number].withdraw(amount)


        
