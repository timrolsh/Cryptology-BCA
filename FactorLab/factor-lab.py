import math
small_primes: list[int] = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]

"""
return a tuple (s, d) from n such that n - 1 = 2^s * d
"""


def factor_two(n: int) -> tuple[int, int]:
    s: int = 0
    n -= 1
    while n % 2 == 0:
        s += 1
        n = n // 2
    # at this point, d will be equal to s
    return (s, n)


"""
Return if a number is prime or not using the deterministic Miller-Rabin algorithm.
"""


def is_prime(n: int) -> bool:
    if n == 0 or n == 1:
        return False
    elif n == 2:
        return True
    s, d = factor_two(n)
    for a in range(2, int(min(n-2, 2 * math.log(n) ** 2))):
        x: int = a ** d % n
        for _ in range(s):
            y: int = x ** 2 % n
            if y == 1 and x != 1 and x != n - 1:
                return False
            x = y
        if x != 1:
            return False
    return True


"""
Naive algorithm for getting prime factorization of a number, try factoring using the first 12 prime numbers.
Returns a list. factor(60) = 2 ^ 2 * 3 ^ 1 * 5 ^ 1 Stored as a list, [2,2,3,1,5,1]
"""


def factor_naive(n: int) -> list[int]:
    output: list[int] = []
    for small_prime in small_primes:
        count: int = 0
        while n % small_prime == 0:
            count += 1
            n //= small_prime
        if count > 0:
            output += [small_prime, count]
    if n != 1:
        output += [n, 1]
    return output


"""
-1 indicates a failure to find a factor
The factor that pollard rho gives you isn't necessarily a prime factor.
"""


def factor_pollard_rho(n: int) -> int:
    if n == 1:
        return -1

    def g(x):
        return (x ** 2 + 1) % n
    x: int = 2
    y: int = 2
    d: int = 1
    while d == 1:
        x = g(x)
        y = g(g(y))
        d = math.gcd(abs(x - y), n)
    if d == n:
        return -1
    else:
        return d


"""
Get the prime factorization of a positive integer. Returns a list.
factor(60) = 2 ^ 2 * 3 ^ 1 * 5 ^ 1
Stored as a list, [2,2,3,1,5,1]
First 12 prime numbers: 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37
Start by using naive method, and if it doesn't return full prime factorization, use pollard rho to get additional prime factors.
"""


def factor(n: int) -> list[int]:
    # use naive method first, if the last factor is not prime, use the pollard rho method to keep factoring it
    final: list[int] = factor_naive(n)
    # naive may have not factored all the way
    final.pop()
    n = final.pop()
    while True:
        factor: int = factor_pollard_rho(n)
        # no additional prime factors
        if factor == -1:
            break
        final += [factor, 1]
        n //= factor
    final += [n, 1]
    return final
