"""

"""

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
	def __iter__(self):
		return iter(self.elements)

class BCall:
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
			other = BCall(other)
		return BCall(*self._funcs, *other._funcs)
	def __add__(self, other: Self | Callable):
		if isinstance(other, Callable):
			other = BCall(other)
		return BCall(*other._funcs, *self._funcs)
	def __call__(self, *__args, **__kwargs):
		# stdout.write(f"CALL[{tuple(i.__name__ for i in self._funcs)}](" + ', '.join(str(i) for i in __args) + ')\n')
		r = self._funcs[-1](*__args, **__kwargs)
		for f in std__reversed(self._funcs[:-1]):
			r = f(r)
		return r

class ExpandedCallable(BCall):
	def __init__(self, func) -> None:
		self._func = func
	def __ror__(self, __value: Iterable[Any]):
		return self._func(*__value)

@BCall
def transform_dct(dct: dict[str, Any]):
	for k in dct:
		if not (k.startswith('std__') or k.startswith('_')) and callable(dct[k]):
			dct[k] = BCall(dct[k])
def transform_globals():
	transform_dct(globals())

print = BCall(print)
input = BCall(input)
call = BCall(lambda x: x())
std__map = map
@BCall
def map(func):
	def map_wrapper(ls):
		return std__map(func, ls)
	return BCall(map_wrapper)
std__join = str.join
@BCall
def join(join_str: str):
	def join_wrapper(ls):
		return std__join(join_str, ls)
	return BCall(join_wrapper)
list = BCall(list)
sorted = BCall(sorted)
reversed = BCall(reversed)
def log(a):
	print(a)
	return a

# print(int & str.split + input | call)
print(input & input | call)