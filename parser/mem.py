class MemoryCell:
    def __init__(self, addr: int, mem: "Memory"= None):
        self._addr = addr
        self._mem = mem

    @property
    def addr(self):
        if self._addr is None:
            raise KeyError("Эта ячейка памяти уже освобождена")
        return self._addr

    def release(self):
        if self._mem is not None:
            self._mem._release(self)
        self._addr = None

    def __repr__(self):
        return "<MemoryCell{}#{}>".format(
            ":" if self._mem is None else "",
            self._addr
        )


class Memory:
    def __init__(self):
        self.mem = []

    def alloc(self) -> MemoryCell:
        addr = 0
        while addr in self.mem:
            addr += 1
        self.mem.append(addr)
        return MemoryCell(addr, self)

    def _release(self, cell: MemoryCell):
        if cell.addr not in self.mem:
            raise ValueError("Ячейка памяти {} не найдена в памяти".format(cell.addr))
        self.mem.remove(cell.addr)
