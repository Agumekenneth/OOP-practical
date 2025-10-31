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
        
