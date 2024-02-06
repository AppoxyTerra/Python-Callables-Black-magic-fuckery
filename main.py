from typing import Any, Callable, Iterable, Self

class BetterCallables:
	def __init__(self, *funcs: Callable):
		self._funcs = funcs
	def __repr__(self) -> str:
		return f'<CallChain {tuple(i.__name__ for i in self._funcs)}>'
	@property
	def __name__(self) -> str:
		return self.__repr__()
	def __or__(self, __value: Any):
		return __value(self)
	def __ror__(self, __value: Any):
		return self.__call__(__value)
	def __rand__(self, __value: Any):
		return self.__call__(__value)
	def __invert__(self):
		return ExpandedCallable(self)
	def __radd__(self, other: Self | Callable):
		if isinstance(other, Callable):
			other = BetterCallables(other)
		return BetterCallables(*other._funcs, *self._funcs)
	def __add__(self, other: Self | Callable):
		if isinstance(other, Callable):
			other = BetterCallables(other)
		return BetterCallables(*self._funcs, *other._funcs)
	def __call__(self, *__args, **__kwargs):
		# stdout.write(f"CALL[{tuple(i.__name__ for i in self._funcs)}](" + ', '.join(str(i) for i in __args) + ')\n')
		r = self._funcs[-1](*__args, **__kwargs)
		for f in reversed(self._funcs[:-1]):
			r = f(r)
		return r

class ExpandedCallable:
	def __init__(self, func) -> None:
		self._func = func
	def __ror__(self, __value: Iterable[Any]):
		return self._func(*__value)

# On transforme avec de la black-magic-fuckery quelques fonctions
print = BetterCallables(print)
input = BetterCallables(input)
call = BetterCallables(lambda x: x())
map = BetterCallables(map)
list = BetterCallables(list)
sorted = BetterCallables(sorted)

print("Commencons gentillement: Pas besoin de comprendre comment fonctionne BetterCallables")
f1 = BetterCallables(lambda x: x*2)
f2 = BetterCallables(lambda x: x+1)
print( (f1 + f2)(5) ) # <=> f1(f2(5))
print( (f2 + f1)(5) ) # <=> f2(f1(5))

print(
	"Puis on devient magicien,"\
	"et les Monsieur 'A monad is a monoid in the category of endofuntors' (devs haskell) on peur:"
)
'Taper un liste d\'entiers:' | print
(int, str.split + input | call) | ~map | sorted | list | print

