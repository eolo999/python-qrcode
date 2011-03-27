#!/usr/bin/python

__doc__ = """
I found this little pearl (
http://www.aimglobal.org/technologies/barcode/Galois_Math.pdf) on which I
based the following mess.
"""

from array import array

GF = 256
# 285 is for QR Code only
PP = 285

log = array('i', [0]*GF)
alog = array('i', [0]*GF)

def fill_log_arrays():
    log[0] = 1 - GF
    alog[0] = 1
    for i in range(1, GF):
        alog[i] = alog[i-1] * 2
        if alog[i] >= GF:
            alog[i] ^= PP
        log[alog[i]] = i

def gf_sum(a, b):
    return a ^ b

def difference(a, b):
    """The same as gf_sum in a GF256"""
    return gf_sum(a, b)

def gf_product(a, b):
    if (a == 0) or (b == 0):
        return 0
    else:
        return alog[(log[a] + log[b]) % (GF - 1)]

def alpha_power(m):
    return alog[m]

def alpha_log(m):
    if m == 0:
        raise Exception("InvalidArgument")
    return log[m]

def inverse(m):
    """Multiplicative inverse of m"""
    if m == 0:
        raise Exception("InvalidArgument")
    return alog[255 - log[m]]

def quotient(a, b):
    """
    int Quotient (int A, int B) { // namely A divided by B
    if (B == 0) return (1-GF); // signifying an error!
    else if (A == 0) return (0);
    else return (ALog[(Log[A] - Log[B] + (GF-1)) % (GF-1)]);
    """
    if b == 0:
        raise Exception("b must be != 0")
    else:
        return alog[(log[a] - log[b] + (GF - 1)) % (GF - 1)]


def build_monomial(degree, coefficient):
    if degree < 0:
        raise Exception("Degree must be positive")
    if coefficient == 0:
        return 0
    coefficients = array('i', [0] * (degree + 1))
    coefficients[0] = coefficient
    return GF256Poly(coefficients)

def get_zero():
    return GF256Poly([0])

def get_one():
    return GF256Poly([1])

def test_build_monomial():
    assert build_monomial(3, 5).coefficients == array('i', [5,0,0,0])
    assert build_monomial(6, 0) == 0


class GF256Poly(object):
    def __init__(self, coefficients):
        """A polynomial in a GF256 Field"""
        self.length = len(coefficients)

        if (len(coefficients) > 1) and (coefficients[0] == 0):
            first_non_zero = 1
            while (first_non_zero < len(coefficients)) and (coefficients[first_non_zero] == 0):
                first_non_zero += 1
            if first_non_zero == self.length:
                self.coefficients = get_zero().coefficients
            else:
                self.coefficients = array('i', coefficients[first_non_zero:])
        else:
            self.coefficients = coefficients

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
                result = gf_sum(result, self.coefficients[i])
            return result
        result = self.coefficients[0]
        for i in [x+1 for x in range(self.length)]:
            result = gf_sum(gf_product(m, result),
                    self.coefficients[i])
        return result

    def add(self, other):
        if self.is_zero():
            return other
        if other.is_zero():
            return self

        if self.length > other.length:
            smaller_coefficients = self.coefficients
            larger_coefficients = other.coefficients
        else:
            larger_coefficients = self.coefficients
            smaller_coefficients = other.coefficients

        length_diff = abs(self.length - other.length)
        sum_diff = larger_coefficients[0:length_diff]

        for i in range(length_diff, len(larger_coefficients)):
            sum_diff[i] = gf_sum(
                    smaller_coefficients[i - length_diff],
                    larger_coefficients[i])

        return GF256Poly(sum_diff)

    def multiply(self, other):
        if self.is_zero() or other.is_zero():
            return get_zero()

        a_coefficients = self.coefficients
        a_length = self.length
        b_coefficients = other.coefficients
        b_length = other.length
        product = [0] * (a_length + b_length - 1)

        for i in range(a_length):
            a_coeff = a_coefficients[i]
            for j in range(b_length):
                product[i + j] = gf_sum(product[i + j],
                        gf_product(a_coeff, b_coefficients[j]))

        return GF256Poly(product)

    def multiply_by_monomial(self, degree, coefficient):
        if degree < 0:
            raise Exception("Degree must be positive")
        if coefficient == 0:
            return get_zero()
        size = self.length
        product = [0] * (size + degree)
        for i in range(size):
            product[i] = gf_product(self.coefficients[i],
                    coefficient)

        return GF256Poly(product)

    def divide(self, other):
        if other.is_zero():
            raise Exception("Cannot divide by 0")

        quotient = get_zero()
        remainder = self

        denominator_leading_term = other.get_coefficient(other.get_degree())
        inverse_denominator_leading_term = inverse(denominator_leading_term)

        while remainder.get_degree() >= other.get_degree() and not remainder.is_zero():
            degree_difference = remainder.get_degree() - other.get_degree()
            scale = gf_product(
                    remainder.get_coefficient(remainder.get_degree()),
                    inverse_denominator_leading_term)
            term = other.multiply_by_monomial(degree_difference, scale)
            iteration_quotient = build_monomial(degree_difference,
                    scale)

            quotient = quotient.add(iteration_quotient)
            remainder = remainder.add(term)

        return quotient, remainder


def test_gf_sum():
    assert gf_sum(141, 43) == 166
    assert gf_sum(43, 178) == difference(43, 178)

def test_power():
    fill_log_arrays()
    assert alpha_power(0) == 1
    assert alpha_power(1) == 2
    print alpha_power(8)
    assert alpha_power(9) == 58

def test_gf_product():
    """This must be the last test called as we are changing the prime
    polynomial"""
    global PP
    PP = 301
    fill_log_arrays()
    p = gf_product(14, 33)
    assert p == 227

def main():
    #fill_log_arrays()
    for n in range(9):
        print n, '\t', alpha_power(n)

fill_log_arrays()

if __name__ == '__main__':
    main()
