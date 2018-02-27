class NameSpace:
    def __init__(self, parent: "NameSpace", mem: "Memory"):
        self.parent = parent
        self.macros = {}
        self.registers = {}
        self.mem = mem

    @property
    def is_root(self):
        return self.parent is None

    def add_macro(self, macro: "Macro"):
        self.macros[macro.name] = macro

    def find_macro(self, name: str) -> "Macro":
        if name in self.macros:
            return self.macros[name]

        if self.is_root:
            raise KeyError("Can't find macros `{}`".format(
                name
            ))

        return self.parent.find_macro(name)

    def add_register(self, name: str):
        self.registers[name] = self.mem.alloc()

    def release_register(self, name):
        self.registers[name].release()
        del self.registers[name]

    def find_register(self, name):
        if name in self.registers:
            return self.registers[name]

        if self.is_root:
            raise KeyError("Can't find register `{}`".format(
                name
            ))

        return self.parent.find_register(name)
