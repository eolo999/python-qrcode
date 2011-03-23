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

def get_log(n):
    return log[n]

def fill_log_arrays():
    log[0] = 1 - GF
    alog[0] = 1
    for i in range(1, GF):
        alog[i] = alog[i-1] * 2
        if alog[i] >= GF:
            alog[i] ^= PP;
        log[alog[i]] = i

def sum(a, b):
    return a ^ b

def difference(a, b):
    return a ^ b

def product(a, b):
    if (a == 0) or (b == 0):
        return 0
    else:
        return alog[(log[a] + log[b]) % (GF - 1)]

def alpha_power(m):
    if m == 0:
        return 1
    else:
        result = 1
        for i in range(0,m):
            result = product(result, 2)
        return result

#        result = 0
#        while m > 0:
#            result += product(n, n)
#            m -= 1
#        return result

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

def test_sum():
    assert sum(141, 43) == 166
    assert sum(43, 178) == difference(43, 178)

def test_power():
    fill_log_arrays()
    assert alpha_power(0) == 1
    assert alpha_power(1) == 2
    print alpha_power(8)
    assert alpha_power(9) == 58

def test_product():
    """This must be the last test called as we are changing the prime
    polynomial"""
    global PP
    PP = 301
    fill_log_arrays()
    p = product(14, 33)
    assert p == 227

def main():
    fill_log_arrays()
    for n in range(9):
        print n, '\t', alpha_power(n)

if __name__ == '__main__':
    main()
