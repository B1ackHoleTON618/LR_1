import ctypes
from ctypes import wintypes, byref, create_string_buffer
import matplotlib.pyplot as plt
import os


while True:
    var = int(input("""Выберете информацию, которую хотите получить (Введите цифру):
    1 - Информация, получаемая при использовании API GlobalMemoryStatus.
    При выводе информации используйте графическое представление (диаграммы, псевдографика).
     
    2 - Карта виртуальной памяти для любого существующего процесса по выбору
    
    Выберете 0 (ноль), чтобы завершить приложение\n    """))
    

    def oone():
        
        class MEMORYSTATUS(ctypes.Structure):
            _fields_ = [("dwLength", wintypes.DWORD),
                        ("dwMemoryLoad", wintypes.DWORD),
                        ("dwTotalPhys", ctypes.c_size_t),
                        ("dwAvailPhys", ctypes.c_size_t),
                        ("dwTotalPageFile", ctypes.c_size_t),
                        ("dwAvailPageFile", ctypes.c_size_t),
                        ("dwTotalVirtual", ctypes.c_size_t),
                        ("dwAvailVirtual", ctypes.c_size_t)]

        GlobalMemoryStatus = ctypes.windll.kernel32.GlobalMemoryStatus
        GlobalMemoryStatus.argtypes = [ctypes.POINTER(MEMORYSTATUS)]
        GlobalMemoryStatus.restype = None

        status = MEMORYSTATUS()
        status.dwLength = ctypes.sizeof(MEMORYSTATUS)
        GlobalMemoryStatus(ctypes.byref(status))

        labels = ['Использование физической памяти', 'Свободно физической памяти', 'Использование файла подкачки', 'Свободно файла подкачки']
        sizes = [status.dwTotalPhys - status.dwAvailPhys, status.dwAvailPhys, 
                status.dwTotalPageFile - status.dwAvailPageFile, status.dwAvailPageFile]
        colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue'] 

        def custom_autopct(pct):
            total = sum(sizes)
            val = int(round(pct*total/100))
            return "{p:.1f}% ({v:.1f} GB)".format(p=pct, v=val / 1024**3)

        total_memory_gb = status.dwTotalPhys / 1024**3
        plt.figure(figsize=(10, 6))
        plt.title(f'Использование системной памяти\n(Всего физической памяти: {total_memory_gb:.1f} GB)')
        plt.pie(sizes, labels=labels, colors=colors,
        autopct=custom_autopct, shadow=True, startangle=140)
        plt.axis('equal') 
        plt.show()

    def ttwo():

        class MEMORY_BASIC_INFORMATION(ctypes.Structure):
            _fields_ = [
                ("BaseAddress",       ctypes.c_void_p),
                ("AllocationBase",    ctypes.c_void_p),
                ("AllocationProtect", wintypes.DWORD),
                ("RegionSize",        ctypes.c_size_t),
                ("State",             wintypes.DWORD),
                ("Protect",           wintypes.DWORD),
                ("Type",              wintypes.DWORD),
            ]

        VirtualQueryEx = ctypes.windll.kernel32.VirtualQueryEx
        VirtualQueryEx.restype = ctypes.c_size_t
        VirtualQueryEx.argtypes = [wintypes.HANDLE, ctypes.c_void_p, ctypes.POINTER(MEMORY_BASIC_INFORMATION), ctypes.c_size_t]

        OpenProcess = ctypes.windll.kernel32.OpenProcess
        CloseHandle = ctypes.windll.kernel32.CloseHandle

        PROCESS_QUERY_INFORMATION = 0x0400
        PROCESS_VM_READ = 0x0010

        pid = 4952
        process_handle = OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, False, pid)
        if not process_handle:
            raise Exception("Could not open process with PID {}".format(pid))

        mem_basic_info = MEMORY_BASIC_INFORMATION()
        address = 0
        regions = []

        while VirtualQueryEx(process_handle, address, byref(mem_basic_info), ctypes.sizeof(mem_basic_info)):
            regions.append((
                mem_basic_info.BaseAddress,
                mem_basic_info.RegionSize,
                mem_basic_info.State,
                mem_basic_info.Protect,
                mem_basic_info.Type
            ))
            
            address += mem_basic_info.RegionSize

        for region in regions:
            base_address, size, state, protect, type = region
            print(f"BaseAddress: {base_address}, Size: {size}, State: {state}, Protect: {protect}, Type: {type}")

        CloseHandle(process_handle)


    match var:
        case 1: oone()
        case 2: ttwo()
        case 0: break