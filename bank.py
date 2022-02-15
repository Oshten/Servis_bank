from time import sleep

from datetime import datetime
from pprint import pprint
from decimal import Decimal


clients = dict()    # дополняемый список клиентов (экземпляров Client)


class BankOperation:
    """
    Класс банковской операции
    """

    def __init__(self, amount, description, type):
        self.datetime = datetime.now()  # Дата и время операции
        self.type = type                # Тип операции [deposit, withdraw]
        self.description = description  # Описание операции
        self.amount = amount            # Сумма операции

    def __str__(self):
        return f'{self.type} {self.amount}'


class Client:
    """
    Класс клиент банка
    """

    def __init__(self, name):
        self.name = name                # Имя клиента
        self.balanse = '0'           # Баланс
        self.operations = None          # Список операций

    def __str__(self):
        return f'{self.name} (Balanse: ${self.balanse})'


def deposit(client, amount, description):
    """Класть деньги на банковский счет"""
    global clients
    old_client = clients.get(client.title())
    if old_client:
        activ_client = old_client
    else:
        activ_client = Client(name=client.title())
        clients[activ_client.name] = activ_client
    activ_client.balanse = str(Decimal(activ_client.balanse) + Decimal(amount))
    oreration = BankOperation(amount=amount, description=description, type='deposit')
    if activ_client.operations:
        activ_client.operations.append(oreration)
    else:
        activ_client.operations = [oreration, ]
    print('Deposit operation was successful!')

def withdraw(client, amount, description):
    """Снимать деньги с банковского счета"""
    global clients
    activ_client = clients.get(client.title())
    if activ_client:
        activ_client.balanse = str(Decimal(activ_client.balanse) - Decimal(amount))
        oreration = BankOperation(amount=amount, description=description, type='withdraw')
        activ_client.operations.append(oreration)
        print('Withdrawal operation was successful!')
    else:
        print("Error! This client don't have bank account.")



deposit('John Jones', '100', 'ATM Deposit')
sleep(3)
deposit('John Jones', '50', 'ATM Deposit')
deposit('Jek Sebastian', '1000', 'ATM Deposit')
pprint(clients)
print(clients['John Jones'])
print(clients['John Jones'].operations[0].datetime)
print(clients['John Jones'].operations[1].datetime)







