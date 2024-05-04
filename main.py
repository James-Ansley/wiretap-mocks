from wiretap import Ledger, Wiretap


class Foo:
    def __init__(self, bar):
        self.strategy = bar

    def baz(self, x, y):
        return self.strategy.apply(x) + self.strategy.apply(y)

    def __repr__(self):
        return f"Foo({repr(self.strategy)})"


class Bar:
    def __init__(self, x):
        self.x = x

    def apply(self, other):
        return self.x + other

    def __repr__(self):
        return f"Bar({self.x})"


with Ledger() as ledger:
    strategy = Wiretap(Bar(1))
    foo = Foo(strategy)
    foo.baz(1, 2)

print(ledger.logs())