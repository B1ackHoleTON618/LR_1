import psutil
import wmi
import ctypes
from ctypes import wintypes
import threading
import sys
import win32api
import win32con


def our_code_info():
    process_pyt = psutil.Process()
    poisk = process_pyt.pid

    def find_library_path(library_name):
        kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
        buffer_size = 260  # MAX_PATH
        buffer = ctypes.create_unicode_buffer(buffer_size)
        result = kernel32.SearchPathW(None, library_name, None, buffer_size, buffer, None)
        if result != 0:
            return buffer.value

    def find_library_handle(library_name):
        library_handle = ctypes.windll.kernel32.GetModuleHandleW(library_name)
        if library_handle != 0:
            return library_handle

    library_name = "user32.dll"
    library_path = find_library_path(library_name)
    library_handle = find_library_handle(library_name)
    print(f"\tИмя - {library_name},\n\tПолное имя - {library_path},\n\tДескриптор - {library_handle}\n")

    return poisk

def get_process_info(poisk):
    try:
        process = psutil.Process(int(poisk))
        print(f"\tИмя - {process.name()},\n\tПолное имя - {process.exe()},\n\tДескриптор - {process.pid}\n")
        return process.name(), process.exe(), process.pid
    except (psutil.NoSuchProcess, ValueError):
        pass

    try:
        process = next((p for p in psutil.process_iter() if p.name() == poisk), None)
        if process:
            print(f"\tИмя - {process.name()},\n\tПолное имя - {process.exe()},\n\tДескриптор - {process.pid}\n")
            return process.name(), process.exe(), process.pid
    except psutil.NoSuchProcess:
        pass

    try:
        c = wmi.WMI()
        for process in c.Win32_Process():
            if process.ExecutablePath == poisk:
                print(f"\tИмя - {process.Name},\n\tПолное имя - {process.ExecutablePath},\n\tДескриптор - {process.ProcessId}\n")
                return process.Name, process.ExecutablePath, process.ProcessId
    except Exception as e:
        pass
    raise ValueError("Процесс не найден")


def info1():
    kernel32 = ctypes.windll.kernel32
    process_id = kernel32.GetCurrentProcessId()
    process_handle = kernel32.GetCurrentProcess()
    current_process_handle = wintypes.HANDLE()
    kernel32.DuplicateHandle(kernel32.GetCurrentProcess(), process_handle,
                             kernel32.GetCurrentProcess(), ctypes.byref(current_process_handle),
                             0, False, 0x0002) 

    opened_process_handle = kernel32.OpenProcess(0x0400 | 0x0010, False, process_id) 
    return process_id, process_handle, current_process_handle, opened_process_handle

def list_system_info():

    print("Процессы:")
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['pid', 'name', 'username'])
        except psutil.NoSuchProcess:
            pass
        else:
            print(pinfo)

    print("\nПотоки:")
    for thread in threading.enumerate():
        print(thread)

    print("\nМодули:")
    modules_list = ", ".join(sys.modules.keys())
    print(modules_list)

    print("\nДрайверы устройств:")
    try:
        reg_handle = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,
                                         r"SYSTEM\CurrentControlSet\Services")
        drivers = []
        i = 0
        while True:
            try:
                key_name = win32api.RegEnumKey(reg_handle, i)
                drivers.append(key_name)
                i += 1
            except win32api.error as e:
                break
        print(", ".join(drivers))
    except Exception as e:
        print("Ошибка при получении информации о драйверах устройств:", e)

while True:
    var = int(input("""\nВыберите действие:
    1 - Вывести дескриптор, имя и полное имя библиотеки user32.dll и моей программы
    2 - Программа, которая принимая дескриптор, имя или полное имя модуля, возвращает
другие два элемента в своих выходных параметрах
    3 - Набор действий
    4 - Список перечисления всех процессов, потоков, модулей и их свойства в
системе, а также список загруженных драйверов устройств
    0 - Выход из программы\n"""))

    match var:
        case 1:
            poisk = our_code_info()
            get_process_info(poisk)
        case 2:
            p = input("Введите дескриптор, имя или полное имя модуля: ")
            poisk = p
            get_process_info(poisk)
        case 3:
            current_process_id, current_pseudo_handle, current_process_handle, opened_process_handle = info1()
            print("Идентификатор текущего процесса:", current_process_id)
            print("Псевдодескриптор текущего процесса:", current_pseudo_handle)
            print("Дескриптор текущего процесса:", current_process_handle)
            print("Дескриптор открытого процесса:", opened_process_handle)
            # Закрываем дескриптор, полученный функцией DuplicateHandle
            kernel32 = ctypes.windll.kernel32
            kernel32.CloseHandle(current_process_handle)
            # Закрываем дескриптор, полученный функцией OpenProcess
            kernel32.CloseHandle(opened_process_handle)
        case 4:
            list_system_info()
        case 0:
            break
        case _:
            print("Неправильный ввод.")
