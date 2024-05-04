from mock_approvals.ledger import Ledger
from mock_approvals.wiretap import Wiretap, WiretappedMethod, ledger
from pytest import approx

from utils import test


class Foo:
    def __init__(self, x):
        self.x = x

    def bar(self):
        return self.x

    def baz(self, other):
        return Foo(self.x + other.x)

    def __matmul__(self, other):
        return self.x + other


class Bar:
    ...


def func(x):
    """The Doc"""
    return x + 1


@test
def a_wiretap_does_not_change_object_behaviour():
    obj = Wiretap("Hello")
    assert obj == "Hello"
    assert isinstance(obj, str)
    assert type(obj) is Wiretap
    assert obj.upper() == "HELLO"
    assert dir(obj) == dir("Hello")

    foo = Foo(1)
    obj = Wiretap(foo)
    assert vars(obj) == vars(Foo(1))
    assert obj.__class__ == Foo
    assert dir(obj) == dir(Foo(1))
    obj.x = 2
    assert foo.x == 2

    cls = Wiretap(Foo)
    assert cls.__name__ == "Foo"
    cls.__name__ = "Bar"
    assert cls.__name__ == "Bar"

    obj = Wiretap(Foo(1))
    obj.__class__ = Bar
    assert obj.__class__ == Bar

    obj = Wiretap(func)
    assert obj.__module__ == func.__module__
    assert obj.__doc__ == "The Doc"
    obj.__module__ = "AnotherModule"
    assert obj.__module__ == "AnotherModule"
    obj.__doc__ = "The new Doc"
    assert obj.__doc__ == "The new Doc"

    obj = Wiretap((1, 2, 3))
    assert obj[1] == 2


@test
def wiretapped_methods_are_wrapped():
    foo = Wiretap(Foo(1))
    meth = foo.bar
    assert type(meth) is WiretappedMethod


@test
def new_wiretaps_will_search_for_the_global_ledger_if_not_given_one():
    with Ledger() as l:
        foo = Wiretap(Foo(1))
        assert ledger(foo) is l
        another_ledger = Ledger()
        bar = Wiretap(Foo(2), another_ledger)
        assert ledger(bar) is another_ledger


@test
def a_wiretap_forwards_operator_dunders():
    obj = Wiretap(5)
    assert obj < 6
    assert obj < Wiretap(6)
    assert 5 < Wiretap(6)
    assert obj <= 5
    assert obj <= Wiretap(5)
    assert 5 <= Wiretap(5)
    assert obj == 5
    assert obj == Wiretap(5)
    assert 5 == Wiretap(5)
    assert obj != 4
    assert obj != Wiretap(4)
    assert 5 != Wiretap(4)
    assert obj >= 5
    assert obj >= Wiretap(5)
    assert 5 >= Wiretap(5)
    assert obj > 4
    assert obj > Wiretap(4)
    assert 5 > Wiretap(4)

    assert obj + 1 == 6
    assert obj + Wiretap(1) == 6
    assert 5 + Wiretap(1) == 6
    assert obj - 1 == 4
    assert obj - Wiretap(1) == 4
    assert 5 - Wiretap(1) == 4
    assert obj * 2 == 10
    assert obj * Wiretap(2) == 10
    assert 5 * Wiretap(2) == 10
    assert obj / 2 == approx(2.5)
    assert obj / Wiretap(2) == approx(2.5)
    assert 5 / Wiretap(2) == approx(2.5)
    assert obj // 2 == 2
    assert obj // Wiretap(2) == 2
    assert 5 // Wiretap(2) == 2
    assert obj % 2 == 1
    assert obj % Wiretap(2) == 1
    assert 5 % Wiretap(2) == 1
    assert obj ** 2 == 25
    assert obj ** Wiretap(2) == 25
    assert 5 ** Wiretap(2) == 25
    assert pow(obj, 2, 7) == 4
    assert pow(obj, Wiretap(2), 7) == 4
    assert pow(obj, 2, Wiretap(7)) == 4
    assert pow(obj, Wiretap(2), Wiretap(7)) == 4

    obj = Wiretap(-1)
    assert abs(obj) == 1
    assert -obj == 1
    assert +obj == -1

    obj = Wiretap(7)
    assert divmod(obj, 3) == (2, 1)
    assert divmod(7, Wiretap(3)) == (2, 1)
    assert divmod(obj, Wiretap(3)) == (2, 1)

    obj = Wiretap(Foo(1))
    assert obj @ 2 == 3
    assert obj @ Wiretap(2) == 3
    assert Foo(1) @ Wiretap(2) == 3

    assert (Wiretap(0b1010) | 0b0101) == 0b1111
    assert (0b1010 | Wiretap(0b0101)) == 0b1111
    assert (Wiretap(0b1010) | 0b1010) == 0b1010
    assert (0b1010 | Wiretap(0b1010)) == 0b1010
    assert (Wiretap(0b11) | 0b00) == 0b11
    assert (0b11 | Wiretap(0b00)) == 0b11
    assert (Wiretap(0b11) | 0b11) == 0b11
    assert (0b11 | Wiretap(0b11)) == 0b11

    assert (Wiretap(0b1010) & 0b0101) == 0b0000
    assert (0b1010 & Wiretap(0b0101)) == 0b0000
    assert (Wiretap(0b1010) & 0b1010) == 0b1010
    assert (0b1010 & Wiretap(0b1010)) == 0b1010
    assert (Wiretap(0b1010) & 0b1010) == 0b1010
    assert (0b1010 & Wiretap(0b1010)) == 0b1010
    assert (Wiretap(0b11) & 0b00) == 0b00
    assert (0b11 & Wiretap(0b00)) == 0b00
    assert (Wiretap(0b11) & 0b11) == 0b11
    assert (0b11 & Wiretap(0b11)) == 0b11

    assert (~Wiretap(1)) == -2
    assert (~Wiretap(10)) == -11

    assert (Wiretap(2) << 1) == 4
    assert (2 << Wiretap(1)) == 4
    assert (Wiretap(2) << 2) == 8
    assert (2 << Wiretap(2)) == 8
    assert (Wiretap(4) << 1) == 8
    assert (4 << Wiretap(1)) == 8
    assert (Wiretap(8) << 2) == 32
    assert (8 << Wiretap(2)) == 32

    assert (Wiretap(2) >> 1) == 1
    assert (2 >> Wiretap(1)) == 1
    assert (Wiretap(2) >> 2) == 0
    assert (2 >> Wiretap(2)) == 0
    assert (Wiretap(4) >> 1) == 2
    assert (4 >> Wiretap(1)) == 2
    assert (Wiretap(8) >> 2) == 2
    assert (8 >> Wiretap(2)) == 2

    assert (Wiretap(0b1010) ^ 0b0101) == 0b1111
    assert (0b1010 ^ Wiretap(0b0101)) == 0b1111
    assert (Wiretap(0b1010) ^ 0b1010) == 0
    assert (0b1010 ^ Wiretap(0b1010)) == 0
    assert (Wiretap(0b1010) ^ 0b1010) == 0b0000
    assert (0b1010 ^ Wiretap(0b1010)) == 0b0000
    assert (Wiretap(0b11) ^ 0b00) == 0b11
    assert (0b11 ^ Wiretap(0b00)) == 0b11
    assert (Wiretap(0b11) ^ 0b11) == 0b00
    assert (0b11 ^ Wiretap(0b11)) == 0b00
