from datetime import datetime
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
        self.current_balance = None     # Текущий баланс

    def __str__(self):
        return f'{self.type} {self.amount}'


class Client:
    """
    Класс клиент банка
    """

    def __init__(self, name):
        self.name = name                # Имя клиента
        self.balanse = '0'              # Баланс
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
    oreration.current_balance = activ_client.balanse
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
        client_balanse = Decimal(activ_client.balanse) - Decimal(amount)
        if client_balanse < 0:
            print("Error. This amount exceeds сlient's balanse.")
            return
        activ_client.balanse = str(client_balanse)
        oreration = BankOperation(amount=amount, description=description, type='withdraw')
        oreration.current_balance = client_balanse
        activ_client.operations.append(oreration)
        print('Withdrawal operation was successful!')
    else:
        print("Error! This client don't have bank account.")


def show_bank_statement(client, since=None, till=None):
    global clients
    activ_client = clients.get(client.title())
    if activ_client:
        if since and till:
            try:
                since = datetime.strptime(since, "%Y-%m-%d %H:%M:%S")
                till = datetime.strptime(till, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                print('Invalid date format. The date must be in the format: "2000-01-01 00:00:00"')
                return
            operations = \
                [operation for operation in activ_client.operations if (operation.datetime >= since) and (
                    operation.datetime <= till)]
        elif since:
            try:
                since = datetime.strptime(since, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                print('Invalid date format. The date must be in the format: "2000-01-01 00:00:00"')
                return
            operations = [operation for operation in activ_client.operations if (operation.datetime >= since)]
        elif till:
            try:
                till = datetime.strptime(till, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                print('Invalid date format. The date must be in the format: "2000-01-01 00:00:00"')
                return
            operations = [operation for operation in activ_client.operations if operation.datetime <= till]
        else:
            operations = [operation for operation in activ_client.operations]
        print(f'|{"Date":<20}|{"Description":<20}|{"Withdrawals":<12}|{"Deposits":<12}|{"Balance":<12}|')
        if since and len(operations) > 0 and activ_client.operations[0].datetime < operations[0].datetime:
            pervious_balanse = activ_client.operations[int(activ_client.operations.index(operations[0])-1)].current_balance
        else:
            pervious_balanse = 0
        print(f'|{"":<20}|{" Previous balance":<20}|{"":<12}|{"":<12}|'
                f'{"$"+"{value:.2f}".format(value=float(pervious_balanse)):>12}|')
        total_count_deposit = Decimal(0)
        total_count_withdraw = Decimal(0)
        for operation in operations:
            total_count_deposit += Decimal(operation.amount if operation.type == "deposit" else 0)
            total_count_withdraw += Decimal(operation.amount if operation.type == "withdraw" else 0)
            print(f'|{"":-^20}|{"":-^20}|{"":-^12}|{"":-^12}|{"":-^12}|')
            print(f'|{operation.datetime.strftime("%Y-%m-%d %H:%M:%S"):^20}|'
                  f'{operation.description:<20}|'
                  f'{"$"+"{value:.2f}".format(value=float(operation.amount)) if operation.type == "withdraw" else "":>12}|'
                  f'{"$"+"{value:.2f}".format(value=float(operation.amount)) if operation.type == "deposit" else "":>12}|'
                  f'{"$" + "{value:.2f}".format(value=float(operation.current_balance)):>12}|')
        total_balanse = Decimal(pervious_balanse) + Decimal(total_count_deposit) - Decimal(total_count_withdraw)
        print(f'|{"":-^20}|{"":-^20}|{"":-^12}|{"":-^12}|{"":-^12}|')
        print(f'|{"":20}|{"Totals":<20}|{"$" + "{value:.2f}".format(value=float(total_count_withdraw)):>12}|'
              f'{"$" + "{value:.2f}".format(value=float(total_count_deposit)):>12}|'
              f'{"$" + "{value:.2f}".format(value=float(total_balanse)):>12}|')
    else:
        print("Error! This client don't have bank account.")



if __name__ == '__main__':
    """Запуск сеанса"""
    print('Service started!')
    while True:
        command = input('>>')
        if command == 'exit':
            print('Service finished!')
            break
        elif command == 'help':
            print('Service for working with clients accounts')
            print("To create a new client account's and add money to the account, enter the command:")
            print('\t\tdeposit --client="(unput name)" --amount=(input amount) --description="(input description)"')
            print("\nTo withdraw money from the client's account, enter the command")
            print('\t\t withdraw --client="(unput name)" --amount=(input amount) --description="(input description)"')
            print("\nTo display information about operations and the state of the client's account on the console, enter the command:")
            print('\t\tshow_bank_statement --client="(unput name)" --since="(start date and time)" --till="(finish date and time)"')
            print('\t\tstart date and time and finish date and time enter in the format: "2000-01-01 00:00:00"')
            print('\t\tstart date and time and finish date and time may not be entered')
            print('\nTo exit, enter the command:')
            print('\t\texit')
        arguments = command.split('--')
        function = arguments[0].strip()
        params = dict()
        params.clear()
        for argument in arguments[1:]:
            list_arguments = argument.split('=')
            key = list_arguments[0].replace('-', '').replace('=', '').strip()
            value = list_arguments[-1].replace("'", "").replace('"', '').strip()
            params[key] = value
        try:
            f = globals()[function]
            f(**params)
        except:
            print('Invalid input!')
