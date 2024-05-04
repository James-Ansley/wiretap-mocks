# Wiretap Mocks

Approval tests for mock objects. Perhaps useful for legacy systems with complex
interactions between objects.

This project is very much in the early proof-of-concept phase.

Objects can be wiretapped and any subsequent method calls are logged:

```python
from wiretap import Ledger, Wiretap


class Foo:
    def __init__(self, bar):
        self.strategy = bar

    def baz(self, x, y):
        return self.strategy.apply(x) + self.strategy.apply(y)


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
```

This will produce a summary of the method calls between wiretapped objects:

```text
Bar(1).apply(1) -> 2
Bar(1).apply(2) -> 3
```
