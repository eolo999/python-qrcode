#!/usr/bin/python
"""Handles Galois Field calculation."""

class GaloisField(object):
    """Raw representation of a Galois Field and its algebric operations."""
    def __init__(self, galois_field=256, primitive_polynomial_as_int=285):
        self.primitive_poly = primitive_polynomial_as_int
        self.field = galois_field
        self.log = [0] * self.field
        self.alog = [0] * self.field
        self.fill_log_arrays()

    def fill_log_arrays(self):
        """Fills log and alog dicts."""
        self.log[0] = 1 - self.field
        self.alog[0] = 1
        for i in range(1, self.field):
            self.alog[i] = self.alog[i-1] * 2
            if self.alog[i] >= self.field:
                self.alog[i] ^= self.primitive_poly
            self.log[self.alog[i]] = i

    def add(self, op1, op2):
        """Sum operation in a Galois Field."""
        return int(op1) ^ int(op2)

    def subtract(self, op1, op2):
        """The same as add in a GF"""
        return self.add(op1, op2)

    def multiply(self, op1, op2):
        """Multiply two numbers in a Galois Field."""
        if (op1 == 0) or (op2 == 0):
            return 0
        else:
            return self.alog[(self.log[op1] + self.log[op2]) % (self.field - 1)]

    def alpha_power(self, num):
        """Power of a number in a Galois Field."""
        return self.alog[num]

    def alpha_log(self, num):
        """Log of a number in a Galois Field."""
        if num == 0:
            raise Exception("InvalidArgument")
        return self.log[num]

    def inverse(self, num):
        """Multiplicative inverse of num"""
        if num == 0:
            raise Exception("InvalidArgument")
        return self.alog[255 - self.log[num]]

    def quotient(self, op1, op2):
        """Divide two numbers in a Galois Field."""
        if op2 == 0:
            raise Exception("b must be != 0")
        else:
            return self.alog[(self.log[op1] -
                self.log[op2] + (self.field - 1)) % (self.field - 1)]

    def build_monomial(self, degree, coefficient):
        """Given a degree and its coefficient returns a GFPoly in the Galois
        Field."""
        if degree < 0:
            raise Exception("Degree must be positive")
        if coefficient == 0:
            return 0
        coefficients = [0] * (degree + 1)
        coefficients[0] = coefficient
        return GFPoly(self, coefficients)

    def get_zero(self):
        """Returns a *zero* GFPoly in the Galois Field."""
        return GFPoly(self, [0])

    def get_one(self):
        """Returns a *one* GFPoly in the Galois Field."""
        return GFPoly(self, [1])


class GFPoly(object):
    """A polynomial in a GF256 Field"""
    def __init__(self, field, coefficients):
        self.length = len(coefficients)
        self.field = field

        if (self.length > 1) and (coefficients[0] == 0):
            first_non_zero = 1
            while ((first_non_zero < self.length) and
                    (coefficients[first_non_zero] == 0)):
                first_non_zero += 1
            if first_non_zero == self.length:
                self.coefficients = self.field.get_zero().coefficients
            else:
                self.coefficients = coefficients[first_non_zero:]
        else:
            self.coefficients = coefficients
        self.length = len(coefficients)

    def __str__(self):
        return "GFPoly(" + str(self.coefficients) + ")"

    def __repr__(self):
        return self.__str__()

    def __add__(self, other):
        if self.field != other.field:
            raise Exception("GFPolys do not have same Galois Field")

        if self.is_zero():
            return other
        if other.is_zero():
            return self

        diff = other.length - self.length
        if diff == 0:
            val = [self.field.add(x, y) for x, y in
                    zip(self.coefficients, other.coefficients)]
        elif diff > 0:
            zeroes = [0] * diff
            val = [self.field.add(x, y) for x, y in
                    zip(zeroes + self.coefficients, other.coefficients)]
        else:
            zeroes = [0] * abs(diff)
            val = [self.field.add(x, y) for x, y in
                    zip(self.coefficients, zeroes + other.coefficients)]

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
        product = [0] * (a_length + b_length - 1)

        for i in range(a_length):
            a_coeff = a_coefficients[i]
            for j in range(b_length):
                product[i + j] = self.field.add(product[i + j],
                        self.field.multiply(a_coeff, b_coefficients[j]))

        return GFPoly(self.field, product)

    def __div__(self, other):
        if self.field != other.field:
            raise Exception("GFPolys do not have same Galois Field")
        if other.is_zero():
            raise Exception("Cannot divide by 0")

        quotient = self.field.get_zero()
        remainder = self

        den_leading_term = other.get_coefficient(other.get_degree())
        inverse_den_leading_term = self.field.inverse(den_leading_term)

        while remainder.get_degree() > other.get_degree() and (not
                remainder.is_zero()):
            degree_difference = remainder.get_degree() - other.get_degree()
            scale = self.field.multiply(
                    remainder.get_coefficient(remainder.get_degree()),
                    inverse_den_leading_term)
            term = other.multiply_by_monomial(degree_difference, scale)
            iter_quotient = self.field.build_monomial(degree_difference, scale)

            quotient += iter_quotient
            remainder += term
            #print "remainder(%d):" % remainder.get_degree(), remainder

        return quotient, remainder

    def get_coefficients(self):
        """Return a list containing GFPoly's coefficients."""
        return self.coefficients

    def get_degree(self):
        """Returns the GFPoly's degree."""
        return self.length - 1

    def is_zero(self):
        """Returns true if GFPoly's coefficients is equal to 0."""
        return self.coefficients[0] == 0

    def get_coefficient(self, degree):
        """Returns the cooefficient of the GFPoly's at a given degree."""
        return self.coefficients[self.length - 1 - degree]

    def evaluate_at(self, degree):
        if degree == 0:
            return self.get_coefficient(0)
        if degree == 1:
            result = 0
            for i in range(self.length):
                result = self.field.add(result, self.coefficients[i])
            return result
        result = self.coefficients[0]
        for i in [x + 1 for x in range(self.length)]:
            result = self.field.add(self.field.multiply(degree, result),
                    self.coefficients[i])
        return result

    def multiply_by_monomial(self, degree, coefficient):
        """Returns a new GFPoly obtained multiplying instance GFPoly by a
        GFPoly monomial of given degree and coefficien."""
        if degree < 0:
            raise Exception("Degree must be positive")

        if coefficient == 0:
            return self.field.get_zero()
        size = len(self.coefficients)
        product = [0] * (size + degree)
        for i in range(size):
            product[i] = self.field.multiply(self.coefficients[i],
                    coefficient)

        return GFPoly(self.field, product)

