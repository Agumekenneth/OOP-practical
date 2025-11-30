from abc import ABC, abstractmethod
class BankAccount:
    def __init__(self, account_number, balance=0):
        self._account_number = account_number
        self._balance = balance
    @property
    def account_number(self):
        '''read only for account number'''
        return self._account_number
    @property
    def balance(self):
        return self._balance
    @balance.setter
    def balance(self,amount):
        '''setter for modifying balance'''
        if amount >=0:
            self._balance = amount
        else:
            print(f"Balance can't be negative")

    @abstractmethod
    def deposit(self,amount):
        pass
    @abstractmethod
    def withdraw(self,amount):
        pass
    @abstractmethod
    def check_balance(self, amount):
        pass
class SavingsAccount(BankAccount):
    def __init__(self, account_number, balance=0, interest_rate = 0.05):
        super().__init__(account_number, balance)
        self._interest_rate = interest_rate
    def depsoit(self,amount):
        if amount >0:
            self.balance += amount
            print(f"Deposited{amount}, to savings account{self.account_number}, new balance is UGX{self.balance}")
        else:
            print(f"Invalid deposit amount please!!")
    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            print(f" withdrew amount UGX{amount} from account{self.account_number}and yoir new balnace is UGX{self.balance}")
        else:
            print(f"Invalid withdrew")
    def check_balance(self):
        print(f" Your savings account{self.account_number} has a balance of UGX{self.balance} please!!!")
    def calculate_interest(self):
        interest = self.balance * self._interest_rate
        self.deposit(interest)
        print(f"Interest of UGX{interest} has been addded to account{self.account_number}, your new balance is UGX{self.balance}")
class CheckingAccount(BankAccount):
    def __init__(self, account_number, balance =0,overdraft_limit=50000):
        self._overdraft_limit = overdraft_limit
        super().__init__(account_number,balance)
    def deposit(self,amount):
        if amount >0:
            self.balance += amount
            print(f"depsoited UGX{amount} from checking account {self.account_number} and your new balance is UGx{self.balance}")
        else:
            print(f'Invalid deposit')
    def withdraw(self, amount):
        if 0 < amount <= self.balance + self._overdraft_limit:
            self.balance -= amount
            print(f"withdrew amount UGX{amount} from checking account number{self.account_number} and your new balance is {self.balance}")
        else:
            print(f"Insufficient Funds, amount exceeds overdraft limit")
    def check_balance(self):
        print(f"checking account{self.account_number} has a balance of UGX{self.balance}")
class BankSystem:
    def __init__(self):
        self.accounts = []
    def create_account(self):
        account_type = input("Enter account type please!!(savings/checking)").strip().lower()
        account_number = input("Enter account number").strip()
        if account_number in self.accounts:
            print(f"Account already exists")
            return
        if account_type == 'savings':
            self.accounts[account_number] = SavingsAccount(account_number)
        elif account_type == 'checking':
            account_type[account_number] = CheckingAccount(account_number)
        else:
            print(f"Invalid account type, choose either 'savings' or 'checking' accounts.")
        print(f"{account_type.capitalize()}account {account_number} has been created ")
    def deposit(self):
        account_number = input("Enter account number").strip()
        amount = float(input("Enter the amount you wnat to deposit"))
        if account_number in self.accounts:
            self.accounts[account_number].deposit(amount)
        else:
            print("Account not found")
    def withdraw(self):
        account_number = input("Enter account number").strip()
        amount = float(input("Enter the withdraw amount"))
        if account_number in self.accounts:
            self.accounts[account_number].withdraw(amount)
        else:
            print(f"Account not found")
    def check_balance(self):
        account_number = input("Enter your account number")
        if account_number in self.accounts:
            self.accounts[account_number].check_balance()
        else:
            print('Account not found')
    