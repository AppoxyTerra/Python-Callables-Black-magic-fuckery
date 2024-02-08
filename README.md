
# Black Magic Fuckery

Just some python function concat. system and more.

## Class `BCall`

This is the heart of this module.

You can make an instance of it from python functions in two ways:

1. Create a variable, and list functions in the constructor:
	```python
	# input will be called first, then the returned value of input will be passed to print 
	print_input = BCall(input, print)
	```
2. Create a function, and decorate it with `BCall`:
	```python
	@BCall
	def f(x):
		return x * 12 + 1/x
	```

Then, you can do cool stuff with operators:

- Function concatenation:
	```python
	print((f + g)(5))
	# Is equivalent to:
	r = f(5)
	r = g(r)
	print(r)
	```
- Function piping:
	```python
	# To do the exact same thing as in the two previous examples:
	print(f(5) | g)
	```
- Expand argument:
	```python
	[1, 2, 3] | ~print
	# is equivalent to:
	print(1, 2, 3)
	# whereas
	[1, 2, 3] | print
	# is equivalent to:
	print([1, 2, 3])
	```
- Associate functions in parallel:
	```python
	print(input & input | call)
	# Each input gives its own output and everything is packed together in a list. 
	```

## Tools

You can use `transform_dct` to transform every function of a dictionnary,
into its own BCall so that it supports all the cool features.

`transform_globals` uses `transform_dct` with the whole global scope.
