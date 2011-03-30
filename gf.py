#!/usr/bin/python

__doc__ = """
I found this little pearl:
http://www.aimglobal.org/technologies/barcode/Galois_Math.pdf) on which I
based the following mess.
"""

from array import array

class GaloisField(object):
    def __init__(self, galois_field=256, primitive_polynomial_as_int=285):
        self.pp = primitive_polynomial_as_int
        self.gf = galois_field
        self.log = array('i', [0] * self.gf)
        self.alog = array('i', [0] * self.gf)
        self.fill_log_arrays()

    def fill_log_arrays(self):
        self.log[0] = 1 - self.gf
        self.alog[0] = 1
        for i in range(1, self.gf):
            self.alog[i] = self.alog[i-1] * 2
            if self.alog[i] >= self.gf:
                self.alog[i] ^= self.pp
            self.log[self.alog[i]] = i

    def add(self, a, b):
        return int(a) ^ int(b)

    def subtract(self, a, b):
        """The same as add in a GF"""
        return self.add(a, b)

    def multiply(self, a, b):
        if (a == 0) or (b == 0):
            return 0
        else:
            return self.alog[(self.log[a] + self.log[b]) % (self.gf - 1)]

    def alpha_power(self, a):
        return self.alog[a]

    def alpha_log(self, a):
        if a == 0:
            raise Exception("InvalidArgument")
        return self.log[a]

    def inverse(self, a):
        """Multiplicative inverse of a"""
        if a == 0:
            raise Exception("InvalidArgument")
        return self.alog[255 - self.log[a]]

    def quotient(self, a, b):
        if b == 0:
            raise Exception("b must be != 0")
        else:
            return self.alog[(self.log[a] - self.log[b] + (self.gf - 1)) % (self.gf - 1)]

    def build_monomial(self, degree, coefficient):
        if degree < 0:
            raise Exception("Degree must be positive")
        if coefficient == 0:
            return 0
        coefficients = array('i', [0] * (degree + 1))
        coefficients[0] = coefficient
        return GFPoly(self, coefficients)

    def get_zero(self):
        return GFPoly(self, array('i', [0]))

    def get_one(self):
        return GFPoly(self, array('i', [1]))


class GFPoly(object):
    def __init__(self, field, coefficients):
        """A polynomial in a GF256 Field"""
        self.length = len(coefficients)
        self.field = field

        if (self.length > 1) and (coefficients[0] == 0):
            first_non_zero = 1
            while (first_non_zero < self.length) and (coefficients[first_non_zero] == 0):
                first_non_zero += 1
            if first_non_zero == self.length:
                self.coefficients = self.field.get_zero().coefficients
            else:
                self.coefficients = array('i', coefficients[first_non_zero:])
        else:
            self.coefficients = array('i', coefficients)

    def __str__(self):
        return "GFPoly(" + str(self.coefficients.tolist()) + ")"

    def __repr__(self):
        return self.__str__()

    def get_coefficients(self):
        return self.coefficients

    def get_degree(self):
        return self.length - 1

    def is_zero(self):
        return self.coefficients[0] == 0

    def get_coefficient(self, degree):
        return self.coefficients[self.length - 1 - degree]

    def evaluate_at(self, m):
        if m == 0:
            return self.get_coefficient(0)
        if m == 1:
            result = 0
            for i in range(self.length):
                result = self.field.add(result, self.coefficients[i])
            return result
        result = self.coefficients[0]
        for i in [x + 1 for x in range(self.length)]:
            result = self.field.add(self.field.multiply(m, result),
                    self.coefficients[i])
        return result

    def __add__(self, other):
        if self.field != other.field:
            raise Exception("GFPolys do not have same Galois Field")

        if self.is_zero():
            return other
        if other.is_zero():
            return self

        diff = other.length - self.length
        if diff == 0:
            val = [self.field.add(x,y) for x,y in zip(self.coefficients, other.coefficients)]
        elif diff > 0:
            zr = array('i', [0] * diff)
            val = [self.field.add(x,y) for x,y in zip(zr + self.coefficients, other.coefficients)]
        else:
            zr = array('i', [0] * abs(diff))
            val = [self.field.add(x,y) for x,y in zip(self.coefficients, zr + other.coefficients)]

        val = GFPoly(self.field, val)
        return val

    def __mul__(self, other):
        if self.field != other.field:
            raise Exception("GFPolys do not have same Galois Field")
        if self.is_zero() or other.is_zero():
            return self.field.get_zero()

        a_coefficients = self.coefficients
        a_length = self.length
        b_coefficients = other.coefficients
        b_length = other.length
        product = array('i', [0] * (a_length + b_length - 1))

        for i in range(a_length):
            a_coeff = a_coefficients[i]
            for j in range(b_length):
                product[i + j] = self.field.add(product[i + j],
                        self.field.multiply(a_coeff, b_coefficients[j]))

        return GFPoly(self.field, product)

    def multiply_by_monomial(self, degree, coefficient):
        if degree < 0:
            raise Exception("Degree must be positive")

        if coefficient == 0:
            return self.field.get_zero()
        size = self.length
        product = array('i', [0] * (size + degree))
        for i in range(size):
            product[i] = self.field.multiply(self.coefficients[i],
                    coefficient)

        return GFPoly(self.field, product)

    def divide(self, other):
        if self.field != other.field:
            raise Exception("GFPolys do not have same Galois Field")
        if other.is_zero():
            raise Exception("Cannot divide by 0")

        quotient = self.field.get_zero()
        remainder = self

        denominator_leading_term = other.get_coefficient(other.get_degree())
        inverse_denominator_leading_term = self.field.inverse(denominator_leading_term)

        while remainder.get_degree() > other.get_degree() and (not
                remainder.is_zero()):
            degree_difference = remainder.get_degree() - other.get_degree()
            scale = self.field.multiply(
                    remainder.get_coefficient(remainder.get_degree()),
                    inverse_denominator_leading_term)
            term = other.multiply_by_monomial(degree_difference, scale)
            iteration_quotient = self.field.build_monomial(degree_difference, scale)

            quotient += iteration_quotient
            remainder += term
            #print "remainder(%d):" % remainder.get_degree(), remainder

        return quotient, remainder


def test_gf_add():
    gf = GaloisField()
    assert gf.add(141, 43) == 166
    assert gf.add(43, 178) == gf.subtract(43, 178)

def test_gf_alpha_power():
    gf = GaloisField()
    assert gf.alpha_power(0) == 1
    assert gf.alpha_power(1) == 2
    assert gf.alpha_power(9) == 58

def test_gf_multiply():
    gf = GaloisField(256, 301)
    assert gf.multiply(14, 33) == 227

def main():
    gf = GaloisField(256, 301)
    for n in range(9):
        print n, '\t', gf.alpha_power(n)


if __name__ == '__main__':
    main()
