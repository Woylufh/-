import threading
import time
import queue


class Table:

    def __init__(self, nam=int):
        self.number = nam  # - номер стола
        self.is_busy = (bool == nam)  # - занят стол или нет.


class Cafe(Table):
    def __init__(self, nam):
        Table.__init__(self, nam=int)
        self.queue = queue.Queue()
        self.tables = nam
        self.customers = 0
        self.all_customers = threading.Event()

    def customer_arrival(self):  # - моделирует приход посетителя(каждую секунду).
        for customer in range(1, 21):
            print('-' * 20 + f' Посетитель номер {customer} прибыл')
            self.customers += 1
            cust = Customer(customer, self)
            cust.start()
            time.sleep(1)

    def serve_customer(self, customer):
        if bool(self.tables) == self.is_busy:  # Проверяет наличие свободных столов
            print(f'Посетитель номер {customer.number} ожидает свободный стол')
            self.queue.put(customer)  # ставим посетителя в очередь
            return

        table = self.tables.pop(0)  # в случае наличия стола - начинает обслуживание посетителя
        print(f'Посетитель номер {customer.number} сел за стол {table.number}')
        time.sleep(5)
        print('*' * 20 + f' Посетитель номер {customer.number} покушал и ушёл')
        self.tables.append(table)

        self.customers -= 1  # отсчет обслуженных посетителей
        if self.customers == 0:

            self.all_customers.set()  # событие установлено, потоки, ожидающие события, будут уведомлены.
            self.all_customers.wait()  # метод блокирует текущий поток, пока другой поток не вызовет set()
            print('\n'+'*' * 20 + ' Посетителей нет. Кафе закрыто!!! '+'*' * 20)

        if not self.queue.empty():  # Метод Queue.empty() возвращает True, если очередь пуста, иначе False.
            follow_cust = self.queue.get()  # Получаем элемент из очереди
            self.serve_customer(follow_cust)  # запускаем новый круг метода serve_customer


class Customer(threading.Thread):

    def __init__(self, nam, cafe, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.number = nam
        self.cafe = cafe

    def run(self):
        self.cafe.serve_customer(self)


table1 = Table(1)
table2 = Table(2)
table3 = Table(3)
tables = [table1, table2, table3]

# Инициализируем кафе
cafe = Cafe(nam=tables)

# Запускаем поток для прибытия посетителей
customer_arrival_thread = threading.Thread(target=cafe.customer_arrival)
customer_arrival_thread.start()

# Ожидаем завершения работы прибытия посетителей
customer_arrival_thread.join()

