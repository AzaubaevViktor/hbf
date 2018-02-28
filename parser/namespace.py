from typing import Dict

from .mem import MemoryCell, Memory


class NameSpace:
    def __init__(self, parent: "NameSpace", mem: "Memory"):
        self.parent = parent

        self.objs = {}  # type: Dict[str, object]
        self.mem = mem

    @property
    def is_root(self):
        return self.parent is None

    def __setitem__(self, name, obj):
        if name in self.objs:
            raise KeyError("Name `{}` already used".format(name))

        self.objs[name] = obj

    def __getitem__(self, name) -> object:
        if name in self.objs:
            return self.objs[name]

        if self.is_root:
            raise KeyError("Can't find `{}`".format(
                name
            ))

        return self.parent[name]

    def add_macro(self, macro: "Macro"):
        self[macro.name] = macro

    def add_register(self, name: str):
        self[name] = self.mem.alloc()

    def release_register(self, name):
        reg = self.get(name, MemoryCell)
        reg.release()
        del self.objs[name]

    def get(self, name, _type: type):
        obj = self[name]
        if isinstance(obj, _type):
            return obj
        raise TypeError("`{}` should be `{}`, not `{}`".format(
            name, _type, type(obj)
        ))

    def create_child(self):
        return NameSpace(self, self.mem)

    def cleanup(self):
        for reg in self.objs.values():
            if isinstance(reg, MemoryCell):
                reg.release()
