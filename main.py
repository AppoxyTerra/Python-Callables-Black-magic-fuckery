from typing import Any, Callable, Iterable, Self

std__reversed = reversed

class CallGroup:
	""" This is a simple identifier/helper (to avoid confusion with functions that return tuples) """
	def __init__(self, *elements):
		self.elements = []
		for i in elements:
			if isinstance(i, CallGroup):
				self.elements.extend(i.elements)
			else:
				self.elements.append(i)
	# def __reversed__(self):
	# 	return CallGroup(*reversed(self.elements))
	# def __call__(self, *a, **k):
	# 	return list(f(*a, **k) for f in self.elements)
	# def __iter__(self):
	# 	return iter(self.elements)

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
		if isinstance(__value, CallGroup):
			ls = []
			for element in __value.elements:
				try:
					ls.append(self.__call__(element))
				except TypeError:
					ls.append(element)
			return ls
		else:
			return self.__call__(__value)
	def __and__(self, __value: Any):
		return CallGroup(self, __value)
	def __rand__(self, __value: Any):
		return CallGroup(__value, self)
	def __invert__(self):
		return ExpandedCallable(self)
	def __radd__(self, other: Self | Callable):
		if isinstance(other, Callable):
			other = BetterCallables(other)
		return BetterCallables(*self._funcs, *other._funcs)
	def __add__(self, other: Self | Callable):
		if isinstance(other, Callable):
			other = BetterCallables(other)
		return BetterCallables(*other._funcs, *self._funcs)
	def __call__(self, *__args, **__kwargs):
		# stdout.write(f"CALL[{tuple(i.__name__ for i in self._funcs)}](" + ', '.join(str(i) for i in __args) + ')\n')
		r = self._funcs[-1](*__args, **__kwargs)
		for f in std__reversed(self._funcs[:-1]):
			r = f(r)
		return r

class ExpandedCallable(BetterCallables):
	def __init__(self, func) -> None:
		self._func = func
	def __ror__(self, __value: Iterable[Any]):
		return self._func(*__value)

# On transforme avec de la black-magic-fuckery quelques fonctions
print = BetterCallables(print)
input = BetterCallables(input)
call = BetterCallables(lambda x: x())
std__map = map
@BetterCallables
def map(func):
	def map_wrapper(ls):
		return std__map(func, ls)
	return BetterCallables(map_wrapper)
std__join = str.join
@BetterCallables
def join(join_str: str):
	def join_wrapper(ls):
		return std__join(join_str, ls)
	return BetterCallables(join_wrapper)
list = BetterCallables(list)
sorted = BetterCallables(sorted)
reversed = BetterCallables(reversed)
def log(a):
	print(a)
	return a

# print(int & str.split + input | call)
F = (
	input
+	log
+	str.split
+	log
+	map(int)
+	log
+	sorted
+	log
+	map(str)
+	log
+	join('\n')
)
F() | print