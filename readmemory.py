import ctypes
from ctypes import wintypes


class MemoryReader:
    ERROR_PARTIAL_COPY = 0x012B
    PROCESS_VM_READ = 0x0010
    SIZE_T = ctypes.c_size_t
    PSIZE_T = ctypes.POINTER(SIZE_T)

    def __init__(self, pid) -> None:
        self.pid = pid
        self.kernel32 = ctypes.WinDLL('self.kernel32', use_last_error=True)
        self.kernel32.OpenProcess.errcheck = self._check_zero
        self.kernel32.OpenProcess.restype = wintypes.HANDLE
        self.kernel32.OpenProcess.argtypes = (
            wintypes.DWORD,  # _In_ dwDesiredAccess
            wintypes.BOOL,  # _In_ bInheritHandle
            wintypes.DWORD)  # _In_ dwProcessId
        self.kernel32.ReadProcessMemory.errcheck = self._check_zero
        self.kernel32.ReadProcessMemory.argtypes = (
            wintypes.HANDLE,  # _In_  hProcess
            wintypes.LPCVOID,  # _In_  lpBaseAddress
            wintypes.LPVOID,  # _Out_ lpBuffer
            self.SIZE_T,  # _In_  nSize
            self.PSIZE_T)  # _Out_ lpNumberOfBytesRead
        self.kernel32.CloseHandle.argtypes = (wintypes.HANDLE,)

    def _check_zero(self, result, func, args):
        if not result:
            raise ctypes.WinError(ctypes.get_last_error())
        return args

    def _read_process_memory(self, address, size, allow_partial=False):
        buf = (ctypes.c_char * size)()
        nread = self.SIZE_T()
        hProcess = self.kernel32.OpenProcess(self.PROCESS_VM_READ, False, self.pid)
        try:
            self.kernel32.ReadProcessMemory(hProcess, address, buf, size,
                                            ctypes.byref(nread))
        except WindowsError as e:
            if not allow_partial or e.winerror != self.ERROR_PARTIAL_COPY:
                raise
        finally:
            self.kernel32.CloseHandle(hProcess)
        return buf[:nread.value]

    def read(self, address, size=3, endian='little'):
        return int.from_bytes(
            self._read_process_memory(address, size),
            endian
        )
