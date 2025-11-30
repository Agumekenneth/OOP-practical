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
            