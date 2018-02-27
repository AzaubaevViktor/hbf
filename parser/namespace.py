class NameSpace:
    def __init__(self, parent: "NameSpace"):
        self.parent = parent
        self.macros = {}
        self.registers = {}

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

