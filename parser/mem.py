class MemoryCell:
    def __init__(self, addr: int, mem: "Memory"):
        self._addr = addr
        self._mem = mem

    @property
    def addr(self):
        if self._addr is None:
            raise KeyError("Эта ячейка памяти уже освобождена")
        return self._addr

    def release(self):
        self._mem._release(self)
        self._addr = None


class Memory:
    def __init__(self):
        self.mem = []

    def alloc(self):
        addr = 0
        while addr in self.mem:
            addr += 1
        return addr

    def _release(self, cell: MemoryCell):
        if cell.addr not in self.mem:
            raise ValueError("Ячейка памяти {} не найдена в памяти".format(cell.addr))
        self.mem.remove(cell.addr)
