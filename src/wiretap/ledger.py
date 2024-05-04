from itertools import chain

_root_ledger = None


def global_ledger():
    global _root_ledger
    return _root_ledger


class LedgerContexException(Exception):
    ...


class Ledger:
    def __init__(self):
        self.events = []

    def log_method_call(self, obj, meth, args, kwargs, returned, caller=None):
        args = ", ".join(chain(
            (repr(arg) for arg in args),
            (f"{k}={repr(arg)}" for k, arg in kwargs),
        ))
        if caller is None:
            self.events.append(
                f"{repr(obj)}.{meth}({args}) -> {returned}"
            )
        else:
            self.events.append(
                f"{repr(obj)}.{meth}({args}) -> {returned} "
                f"(within: {caller.__class__})"
            )

    def log_call(self, function, args, kwargs, returned, caller=None):
        args = ", ".join(chain(
            (repr(arg) for arg in args),
            (f"{k}={repr(arg)}" for k, arg in kwargs),
        ))
        if caller is None:
            self.events.append(f"{function.__name__}({args}) -> {returned}")
        else:
            self.events.append(f"{function.__name__}({args}) -> {returned} "
                               f"(within: {caller.__class__})")

    def logs(self):
        return "\n".join(self.events)

    def __enter__(self):
        global _root_ledger
        if _root_ledger is None:
            _root_ledger = self
        else:
            raise LedgerContexException(
                "An attempt to set a global ledger was made, "
                "but one was already set"
            )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        global _root_ledger
        _root_ledger = None
        return False
