import socket
import os
import tempfile
import platform
import ctypes
from ctypes import wintypes
import psutil
import time

while True:
    var = int(input("""Выберете информацию, которую хотите получить (Введите цифру):
    1 - Имя компьютера, имя пользователя 
    2 - Пути к системным каталогам Windows
    3 - Версия операционной системы
    4 - Системные метрики (не менее 2 метрик)
    5 - Системные параметры (не менее 2 параметров)
    6 - Системные цвета (определить цвет для некоторых символьных констант и изменить его на любой другой)
    7 - Функции для работы со временем
    8 - 
    Выберете 0 (ноль), чтобы завершить приложение\n    """))

    def zadanie_1():
        print("\nВы выбрали пункт 1:")
        comp_name = socket.gethostname()
        user_name = os.getenv('USERNAME')
        print(f"    Имя компьютера: {comp_name}\n    Имя пользователя: {user_name}\n")

    def  zadanie_2():
        print("\nВы выбрали пункт 2:")
        path = os.path.expandvars("%SystemRoot%")
        path1 = os.path.join(os.environ['SystemRoot'], 'System32')
        path2 = tempfile.gettempdir()
        print(f"""    Функция GetWindowsDirectory - {path}
    Функция GetSystemDirectory - {path1}
    Функция GetTempPath - {path2}\n""")
        
    def zadanie_3():
        print("\nВы выбрали пункт 3:")
        version = platform.system() + ' ' + platform.version()
        print(f'Версия операционной системы Windows: {version}\n')    
        
    def zadanie_4():
        user32 = ctypes.windll.user32
        width = user32.GetSystemMetrics(0)  # Ширина экрана
        height = user32.GetSystemMetrics(1)  # Высота экрана

        print("\nВы выбрали пункт 4:")
        print(f'Ширина экрана: {width} пикселей')
        print(f'Высота экрана: {height} пикселей\n')
        
    def zadanie_5():

        cpu_percent = psutil.cpu_percent()
        cpu_count = psutil.cpu_count(logical=False)  
        cpu_logical_count = psutil.cpu_count(logical=True) 

        memory = psutil.virtual_memory()

        disk_partitions = psutil.disk_partitions()
        disk_usage = psutil.disk_usage(disk_partitions[0].device)

        network_interfaces = psutil.net_if_addrs()

        print("\nВы выбрали пункт 5:")
        print(f'Загрузка CPU: {cpu_percent}%')
        print(f'Физические ядра CPU: {cpu_count}')
        print(f'Логические ядра CPU: {cpu_logical_count}')
        print(f'Использование памяти: {memory.percent}%')
        print(f'Использование диска: {disk_usage.percent}%')
        print(f'Сетевые интерфейсы: {list(network_interfaces.keys())}\n')
    
    def zadanie_6():
        print("\nВы выбрали пункт 6:")
        # Константы для элементов отображения
        COLOR_ACTIVEBORDER = 10
        COLOR_ACTIVECAPTION = 2
        COLOR_BTNFACE = 15

        def get_current_colors():
            return [ctypes.windll.user32.GetSysColor(COLOR_ACTIVEBORDER),
                    ctypes.windll.user32.GetSysColor(COLOR_ACTIVECAPTION),
                    ctypes.windll.user32.GetSysColor(COLOR_BTNFACE)]

        def set_system_colors(elements, colors):
            success = ctypes.windll.user32.SetSysColors(len(elements), (ctypes.c_int * len(elements))(*elements),
                                                        (ctypes.c_ulong * len(colors))(*colors))
            return success

        # Получаем текущие цвета
        original_colors = get_current_colors()
        print(f"Исходные цвета: {original_colors}")

        # Новый цвет для установки
        new_color = 0xFF0000  # Например, красный цвет (RGB: 255, 0, 0)

        # Вызываем функцию для установки новых цветов
        elements = [COLOR_ACTIVEBORDER, COLOR_ACTIVECAPTION, COLOR_BTNFACE]
        colors = [new_color] * len(elements)

        success = set_system_colors(elements, colors)

        if success:
            print("Цвет успешно изменен")
        else:
            print("Не удалось изменить цвет")

        # Дополнительная функция для восстановления исходных цветов
        def restore_original_colors():
            success = set_system_colors(elements, original_colors)
            if success:
                print("Цвета восстановлены")
            else:
                print("Не удалось восстановить цвета\n")

        # Раскомментируйте следующую строку, чтобы восстановить исходные цвета
        # restore_original_colors()
    
    def zadanie_7():
        print("\nВы выбрали пункт 7:")
        class SYSTEMTIME(ctypes.Structure):
            _fields_ = [
                ("wYear", wintypes.WORD),
                ("wMonth", wintypes.WORD),
                ("wDayOfWeek", wintypes.WORD),
                ("wDay", wintypes.WORD),
                ("wHour", wintypes.WORD),
                ("wMinute", wintypes.WORD),
                ("wSecond", wintypes.WORD),
                ("wMilliseconds", wintypes.WORD), ]

        class TIME_ZONE_INFORMATION(ctypes.Structure):
            _fields_ = [
                ("Bias", wintypes.LONG),
                ("StandardName", wintypes.WCHAR * 32),
                ("StandardDate", SYSTEMTIME),
                ("StandardBias", wintypes.LONG),
                ("DaylightName", wintypes.WCHAR * 32),
                ("DaylightDate", SYSTEMTIME),
                ("DaylightBias", wintypes.LONG), ]

        kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

        GetSystemTime = kernel32.GetSystemTime
        GetSystemTime.argtypes = [ctypes.POINTER(SYSTEMTIME)]
        GetSystemTime.restype = None
        GetTimeZoneInformation = kernel32.GetTimeZoneInformation
        GetTimeZoneInformation.argtypes = [ctypes.POINTER(TIME_ZONE_INFORMATION)]
        GetTimeZoneInformation.restype = wintypes.DWORD
        system_time = SYSTEMTIME()
        GetSystemTime(ctypes.byref(system_time))

        print(f"Текущая системная дата и время: {system_time.wYear}-{system_time.wMonth:02d}-{system_time.wDay:02d} {system_time.wHour:02d}:{system_time.wMinute:02d}:{system_time.wSecond:02d}")

        time_zone_info = TIME_ZONE_INFORMATION()
        GetTimeZoneInformation(ctypes.byref(time_zone_info))

        bias = time_zone_info.Bias
        print(f"Смещение относительно UTC: {bias} минут\n")

    def zadanie_8():
        
        print("\nВы выбрали пункт 8:")
        # 1
        kernel32 = ctypes.windll.kernel32
        def get_environment_variable(variable_name):
            buffer_size = 256  
            buffer = ctypes.create_unicode_buffer(buffer_size)
            result = kernel32.GetEnvironmentVariableW(variable_name, buffer, buffer_size)
            
            if result == 0:
                error_code = kernel32.GetLastError()
                print(f"Ошибка при получении переменной окружения {variable_name}. Код ошибки: {error_code}")
                return None
            else:
                return buffer.value

        variable_name = "USERNAME" 
        environment_value = get_environment_variable(variable_name)

        if environment_value is not None:
            print(f"Значение переменной окружения {variable_name}: {environment_value}")
        
        # 2
        kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
        value = 12345.67
        currency_format = wintypes.LCID(1033)  
        buffer_size = 256
        buffer = ctypes.create_unicode_buffer(buffer_size)
        kernel32.GetCurrencyFormatW(currency_format, 0, str(value), None, buffer, buffer_size)
        print(f"Форматированная строка для денежной суммы: {buffer.value}")
        
        # 3-4
        user32 = ctypes.windll.user32

        def get_cursor_pos():
            point = ctypes.wintypes.POINT()
            user32.GetCursorPos(ctypes.byref(point))
            return point.x, point.y

        def set_cursor_pos(x, y):
            user32.SetCursorPos(x, y)

        initial_pos = get_cursor_pos()
        print(f"Начальное положение курсора: {initial_pos}")

        new_x = initial_pos[0] - 400
        new_y = initial_pos[1] - 250
        set_cursor_pos(new_x, new_y)
        time.sleep(0.2) 

        final_pos = get_cursor_pos()
        print(f"Измененное положение курсора: {final_pos}\n")

    match var:
        case 1:
            zadanie_1()
        case 2:
            zadanie_2()
        case 3:
            zadanie_3()
        case 4:
            zadanie_4()
        case 5:
            zadanie_5()
        case 6:
            zadanie_6()
        case 7:
            zadanie_7()
        case 8:
            zadanie_8()
        case 0:
            break 
        case _:
            print("Неправильный ввод. Пожалуйста, введите число от 1 до 8.")



