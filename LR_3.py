import threading
import time
from time import sleep
from threading import Thread, Event, current_thread, active_count, Barrier
def crit_section():
    critical_section = threading.Lock()
    shared_data = 0

    def thread_function(thread_id):
        nonlocal shared_data
        
        with critical_section:
            print(f"Поток {thread_id}: входит в критическую секцию")
            shared_data += 1
            print(f"Поток {thread_id}: общие данные = {shared_data}")
            time.sleep(0.5)
            print(f"Поток {thread_id}: покидает критическую секцию")

    threads = []
    for i in range(5):
        thread = threading.Thread(target=thread_function, args=(i,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print("Все потоки завершили выполнение")

def mmutex():
    mutex = threading.Lock()
    shared_resource = 0
    
    def access_resource():
        nonlocal shared_resource
        print(f'{threading.current_thread().name} ожидает доступ к ресурсу')
        mutex.acquire()
        print(f'{threading.current_thread().name} получил доступ к ресурсу')
        shared_resource += 1
        time.sleep(0.5)
        mutex.release()
        print(f'{threading.current_thread().name} освободил ресурс')
     
    threads = []
    for i in range(5):
        thread = threading.Thread(target=access_resource)
        threads.append(thread)
        thread.start()
     
    for thread in threads:
        thread.join()
     
    print(f'Значение shared_resource: {shared_resource}')

def eevent():
    event = Event()
    max_t = 5
    def f():
        thr_num = current_thread().name
        print(f"Поток {thr_num} запустился. Но ждёт остальных.")
        event.wait()
        print(f"Событие наступило! Поток {thr_num} продолжил свою работу")
        
    threads = []  # Список для хранения созданных потоков
    for i in range(max_t):
        thread = Thread(target=f)
        thread.start()
        threads.append(thread)
        time.sleep(0.2)
    time.sleep(1)

    event.set()
    for thread in threads:
        thread.join()

    print("Все потоки завершили выполнение.")
    

def barier():

    br = Barrier(3)
    def worker1():
        print("Работник 1 начал свою часть работы")
        time.sleep(2) 
        print("Работник 1 завершил свою часть работы")
        br.wait()  
        print("Работник 1 начал следующий этап работы")

    def worker2():
        print("Работник 2 начал свою часть работы")
        time.sleep(3) 
        print("Работник 2 завершил свою часть работы")
        br.wait()  
        print("Работник 2 начал следующий этап работы")

    def worker3():
        print("Работник 3 начал свою часть работы")
        time.sleep(1) 
        print("Работник 3 завершил свою часть работы")
        br.wait()  
        print("Работник 3 начал следующий этап работы")

    threads = [Thread(target=worker1), Thread(target=worker2), Thread(target=worker3)]
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print("Все работники перешли к следующему этапу работы.")
    
print("1 - Критическая секция")
print("2 - Мьютекс")
print("3 - Событие")
print("4 - Барьер") 
while True:
    var = int(input("Введите значение: "))
    match var:
        case 1: crit_section()
        case 2: mmutex()
        case 3: eevent()
        case 4: barier()
        case 0: break
