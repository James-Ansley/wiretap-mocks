import inspect
from typing import Final

from wiretap.ledger import Ledger, global_ledger

_WIRETAP_OBJECT_FIELD: Final[str] = "__Wiretap_object"
_WIRETAP_LEDGER_FIELD: Final[str] = "__Wiretap_ledger"


def unwrap(self):
    return object.__getattribute__(self, _WIRETAP_OBJECT_FIELD)


def ledger(self) -> "Ledger":
    return object.__getattribute__(self, _WIRETAP_LEDGER_FIELD)


def try_unwrap(self):
    if type(self) is Wiretap:
        return unwrap(self)
    else:
        return self


class Wiretap:
    def __new__[T](cls, obj: T, ledger: Ledger = None, *args, **kwargs) -> T:
        """
        Created a new Wiretapped object which, where possible, emulates the
        behaviour of ``obj``.

        :param obj: The object to wiretap
        :param ledger: the ledger to report to
        :param args: args to pass to object.__new__
        :param kwargs: kwargs to pass to object.__new__
        """
        instance = super().__new__(cls, *args, **kwargs)
        ledger = ledger if ledger is not None else global_ledger()
        object.__setattr__(instance, _WIRETAP_OBJECT_FIELD, obj)
        object.__setattr__(instance, _WIRETAP_LEDGER_FIELD, ledger)
        return instance

    def __getattr__(self, item):
        attr = getattr(unwrap(self), item)
        if inspect.ismethod(attr) and attr.__self__ is unwrap(self):
            return WiretappedMethod(attr, ledger(self))
        else:
            return attr

    def __setattr__(self, key, value):
        return setattr(unwrap(self), key, value)

    @property
    def __class__(self):
        return unwrap(self).__class__

    @__class__.setter
    def __class__(self, value):
        unwrap(self).__class__ = value

    @property
    def __doc__(self):
        return unwrap(self).__doc__

    @__doc__.setter
    def __doc__(self, value):
        unwrap(self).__doc__ = value

    def __dir__(self):
        return dir(unwrap(self))

    @property
    def __module__(self):
        return unwrap(self).__module__

    @__module__.setter
    def __module__(self, value):
        unwrap(self).__module__ = value

    @property
    def __dict__(self):
        return unwrap(self).__dict__

    def __getitem__(self, item):
        return unwrap(self)[item]

    def __lt__(self, other):
        return unwrap(self) < other

    def __le__(self, other):
        return unwrap(self) <= other

    def __eq__(self, other):
        return unwrap(self) == other

    def __ne__(self, other):
        return unwrap(self) != other

    def __ge__(self, other):
        return unwrap(self) >= other

    def __gt__(self, other):
        return unwrap(self) > other

    def __abs__(self):
        return abs(unwrap(self))

    def __pos__(self):
        return +unwrap(self)

    def __neg__(self):
        return -unwrap(self)

    def __add__(self, other):
        return unwrap(self) + other

    def __sub__(self, other):
        return unwrap(self) - other

    def __floordiv__(self, other):
        return unwrap(self) // other

    def __mul__(self, other):
        return unwrap(self) * other

    def __truediv__(self, other):
        return unwrap(self) / other

    def __matmul__(self, other):
        return unwrap(self) @ other

    def __mod__(self, other):
        return unwrap(self) % other

    def __pow__(self, other, modulo=None):
        return pow(unwrap(self), try_unwrap(other), try_unwrap(modulo))

    def __or__(self, other):
        return unwrap(self) | other

    def __and__(self, other):
        return unwrap(self) & other

    def __invert__(self):
        return ~unwrap(self)

    def __lshift__(self, other):
        return unwrap(self) << other

    def __rshift__(self, other):
        return unwrap(self) >> other

    def __xor__(self, other):
        return unwrap(self) ^ other

    def __radd__(self, other):
        return other + unwrap(self)

    def __rsub__(self, other):
        return other - unwrap(self)

    def __rmul__(self, other):
        return other * unwrap(self)

    def __rtruediv__(self, other):
        return other / unwrap(self)

    def __rmatmul__(self, other):
        return other @ unwrap(self)

    def __rfloordiv__(self, other):
        return other // unwrap(self)

    def __rmod__(self, other):
        return other % unwrap(self)

    def __divmod__(self, other):
        return divmod(unwrap(self), other)

    def __rdivmod__(self, other):
        return divmod(other, unwrap(self))

    def __rpow__(self, other, modulo=None):
        return pow(try_unwrap(other), unwrap(self), try_unwrap(modulo))

    def __rlshift__(self, other):
        return other << unwrap(self)

    def __rrshift__(self, other):
        return other >> unwrap(self)

    def __rand__(self, other):
        return other & unwrap(self)

    def __rxor__(self, other):
        return other ^ unwrap(self)

    def __ror__(self, other):
        return other | unwrap(self)

    def __repr__(self):
        return repr(unwrap(self))


class WiretappedMethod(Wiretap):
    def __new__[T](cls, obj: T, ledger=None, *args, **kwargs) -> T:
        instance = super().__new__(cls, obj, ledger)
        return instance

    def __call__(self, *args, **kwargs):
        obj = unwrap(self)
        result = obj(*args, **kwargs)
        ledger(self).log_method_call(
            obj.__self__,
            obj.__func__.__name__,
            args,
            kwargs,
            result
        )
        return result
