# Migrate matlab code to Python language (Build)

## times, .*

- Multiplication

Multiply Two Vectors

Create two vectors, A and B, and multiply them element by element.

```m
A = [1 0 3];
B = [2 3 7];
C = A.*B
C = 1×3

     2     0    21
```
in terms of python

```python
>>> A = np.array([1, 0, 3])
>>> B = np.array([2, 3, 7])
>>> C = A*B
>>> C
array([ 2,  0, 21])
```

## rdivide, ./

- Right array division

Divide Two Numeric Arrays

Create two numeric arrays, A and B, and divide the second array, B, into the first, A.

```m
A = [2 4 6 8; 3 5 7 9];
B = 10*ones(2,4);
x = A./B
x = 2×4

    0.2000    0.4000    0.6000    0.8000
    0.3000    0.5000    0.7000    0.9000
```

in terms of python

```python
>>> import numpy as np
>>> A = np.array([[2.,4.,6.,8.],[3., 5., 7., 9.]])
>>> B = 10*np.ones((2,4))
>>> x = A/B
>>> x
array([[0.2, 0.4, 0.6, 0.8],
       [0.3, 0.5, 0.7, 0.9]])
>>>
```

## rand

- Uniformly distributed random numbers

Syntax

```m
X = rand
```

### Description

`X = rand` returns a single uniformly distributed random number in the interval `(0,1)`.

in terms of python

```python
>>> import random
>>> a = 0.0
>>> b = 1.0
>>> [a+(b-a) * random.random() for i in range(10)]
>>> [a+(b-a) * random.random() for i in range(10)]
[0.19608765041383325, 0.4775679507480528, 0.6144707320053053,
0.583680501234098, 0.7423328087806593, 0.392135477139825, 0.6745791071325355,
0.7064309580707314, 0.5447476270147292, 0.11138328222518479]
```
