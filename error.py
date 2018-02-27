class HBFError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return "Unknown HBF error `{}`".format(self.msg)
