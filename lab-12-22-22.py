"""
Tim Rolshud
Cryptology
December 22nd, 2022
Extended GCD Lab
"""

"""
Part A: 
Find the greatest common divisor of two positive integers given using the even/odd gcd algorithm.
"""
def gcd(a: int, b: int) -> int:
    # base cases: numbers are the same, one of numbers are 0, or one of numbers are 1
    if a == b:
        return a
    elif a == 0:
        return b
    elif b == 0:
        return a
    elif a == 1 or b == 1:
        return 1
    # a and b are even
    elif a % 2 == 0 and b % 2 == 0:
        return 2*gcd(a // 2, b // 2)
    # a is even, b is odd
    elif a % 2 == 0 and b % 2 == 1:
        return gcd(a // 2, b)
    # a is odd and b is even
    elif a % 2 == 1 and b % 2 == 0:
        return gcd(a, b // 2)
    # both a and b are odd
    else:
        return gcd(abs(a - b) // 2, min(a, b))


"""
Part B: 
"""

"""
Part C:
Given a,b, find x and y such that ax + by = gcd(a,b). 
Returns a tuple representing (x, y)
"""
def extended_gcd(a: int, b: int) -> tuple[int, int]:
    # base case: a is 0, x = 0, y = 1
    if a == 0:
        return (0, 1)
    x_iteration: int
    y_iteration: int
    x_iteration, y_iteration = extended_gcd(b % a, a)
    # recurse out, update iterations of x and y values
    x_final: int = y_iteration - (b // a) * x_iteration
    # the final y value will be the x value of the current iteration
    y_final: int = x_iteration
    return (x_final, y_final)
