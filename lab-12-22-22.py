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
Implement the same even odd GCD algorithm except with the positive integers represented as strings. I will store the 
strings in a custom class called StringNumber, and do operator overloading in order to make subtracting these two 
StringNumber classes together. I also added methods to multiply by 2 and divide by 2, and then checking which value is
greater than the other, also done with operator overloading 
"""
class StringNumber():
    odds: str = "13579"
    evens: str = "02468"
    one: str = "1"
    empty_string: str = ""

    def __init__(self, string: str) -> None:
        self.string = string

    def isOdd(self) -> bool:
        return self.string[len(self.string) - 1] in StringNumber.odds

    def isEven(self) -> bool:
        return self.string[len(self.string) - 1] in StringNumber.evens

    def __gt__(self, other) -> bool:
        # if amount of digits in this number is greater than in other number, it is larger
        if len(self.string) > len(other.string):
            return True
        elif len(self.string) < len(other.string):
            return False
        else:
            for a in range(len(self.string)):
                digit_self: int = int(self.string[a])
                digit_other: int = int(other.string[a])
                if digit_self != digit_other:
                    return digit_self > digit_other
        # strings are equal, one is not greater than the other
        return False

    def __lt__(self, other) -> bool:
        return not self.__gt__(other)

    def __sub__(self, other):
        if self.string == other.string:
            return StringNumber("0")
        self_string: str
        other_string: str = other.string
        if self.__gt__(other):
            self_string = self.string
            other_string = other.string
        else:
            self_string = other.string
            other_string = self.string
        other_string = "0" * (len(self_string) -
                              len(other_string)) + other_string
        a: int = 1
        carry: int = 0
        final_string: str = StringNumber.empty_string
        while a <= len(other_string):
            difference: int = int(
                self_string[-1 * a]) - int(other_string[-1 * a]) - carry
            if difference < 0:
                carry = 1
                final_string = str(difference + 10) + final_string
            else:
                carry = 0
                final_string = str(difference) + final_string
            a += 1
        a = 0
        while final_string[a] == "0":
            a += 1
        return StringNumber(final_string[a:])

    def divide_2(self):
        if self.isOdd():
            self.__sub__(StringNumber.one)
        a: int = 0
        final_string: str = StringNumber.empty_string
        carry: str = StringNumber.empty_string
        while a < len(self.string):
            current_digit: int = int(carry + self.string[a])
            digit_quotient: int = current_digit // 2
            final_string += str(digit_quotient)
            carry = StringNumber.empty_string + \
                str(current_digit - digit_quotient * 2)
            a += 1
        return StringNumber(final_string)

    def mult_2(self):
        final_string: str = StringNumber.empty_string
        carry: int = 0
        a: int = len(self.string) - 1
        while a >= 0:
            product: int = int(self.string[a]) * 2 + carry
            if product >= 10 and a != 0:
                final_string = str(product - 10) + final_string
                carry = 1
            else:
                final_string = str(product) + final_string
                carry = 0
            a -= 1
        return StringNumber(final_string)

    def __eq__(self, other) -> bool:
        return self.string == other.string

    def __str__(self) -> str:
        return self.string

# define constants to use during algorithm
zero: StringNumber = StringNumber("0")
one: StringNumber = StringNumber("1")

"""
Same even odd GCD algorithm that uses strings instead of ints. Wrapper for the helper method which works wirh the 
StringNumber classes implemented earlier. 
"""
def gcd_str(a: str, b: str) -> str:
    return gcd_str_helper(StringNumber(a), StringNumber(b)).string

# recursive helper method for gcd algorithm with strings
def gcd_str_helper(a: StringNumber, b: StringNumber) -> StringNumber:
    # base cases: numbers are the same, one of numbers are 0, or one of numbers are 1
    if a == b:
        return a
    elif a == zero:
        return b
    elif b == zero:
        return a
    elif a == one or b == one:
        return one
    # a and b are even
    elif a.isEven() and b.isEven():
        return gcd_str_helper(a.divide_2(), b.divide_2()).mult_2()
    # a is even, b is odd
    elif a.isEven() and b.isOdd():
        return gcd_str_helper(a.divide_2(), b)
    # a is odd and b is even
    elif a.isOdd() and b.isEven():
        return gcd_str_helper(a, b.divide_2())
    # both a and b are odd
    else:
        return gcd_str_helper()((a-b).divide_2(), min(a, b))


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
