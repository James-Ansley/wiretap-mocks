from pytest import raises
from approvaltests import verify

from mock_approvals import ledger
from mock_approvals.ledger import Ledger, LedgerContexException
from mock_approvals.wiretap import Wiretap
from utils import test


class Foo:
    def __init__(self, x):
        self.x = x

    def bar(self):
        return self.x

    def baz(self, other):
        return Foo(self.x + other.x)

    def __repr__(self):
        return f"{type(self).__name__}({self.x})"


@test
def ledger_can_log_method_calls():
    ledger = Ledger()
    foo = Foo(1)
    ledger.log_method_call(foo, "bar", (), {}, 1)
    foo.x += 1
    ledger.log_method_call(foo, "bar", (), {}, 2, caller=object())
    verify(ledger.logs())


@test
def ledger_can_log_calls():
    ledger = Ledger()
    ledger.log_call(list, ([1, 2, 3],), {}, [1, 2, 3])
    ledger.log_call(tuple, ([1, 2, 3],), {}, (1, 2, 3), caller=object())
    verify(ledger.logs())


@test
def wiretaps_report_events_to_ledgers():
    ledger = Ledger()
    foo = Wiretap(Foo(1), ledger)
    foo.bar()
    foo.baz(Foo(2))
    verify(ledger.logs())


# noinspection PyProtectedMember
@test
def a_single_global_ledger_can_be_set_within_a_context_manager():
    assert ledger._root_ledger is None
    with Ledger() as l:
        assert ledger._root_ledger is l
    assert ledger._root_ledger is None


@test
def multiple_global_ledgers_cannot_be_set():
    with raises(LedgerContexException):
        with Ledger() as l1:
            with Ledger() as l2:
                ...
