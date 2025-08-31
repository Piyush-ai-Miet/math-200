#!/usr/bin/env python3
"""
RSA Decryption Solution - Clean Version
Solves the RSA decryption problem and outputs the flag.
"""

import math


def pollard_rho(n):
    """Pollard's rho algorithm for factorization."""
    if n % 2 == 0:
        return 2
    
    x = 2
    y = 2
    d = 1
    
    def f(x):
        return (x * x + 1) % n
    
    while d == 1:
        x = f(x)
        y = f(f(y))
        d = math.gcd(abs(x - y), n)
    
    return d if d != n else None


def factor_n(n):
    """Factor the modulus n into its prime factors p and q."""
    # Check small primes first
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
    for p in small_primes:
        if n % p == 0:
            return p, n // p
    
    # Try Pollard's rho algorithm
    factor = pollard_rho(n)
    if factor and factor != n:
        return factor, n // factor
    
    return None, None


def extended_gcd(a, b):
    """Extended Euclidean Algorithm."""
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y


def mod_inverse(e, phi_n):
    """Compute the modular inverse of e modulo phi_n."""
    gcd, x, _ = extended_gcd(e, phi_n)
    if gcd != 1:
        raise ValueError("Modular inverse does not exist")
    return x % phi_n


def main():
    """Main RSA decryption function."""
    # Given parameters
    n = 12407072677633161347
    e = 65537
    c = 6680131599371095691
    
    # Factor n
    p, q = factor_n(n)
    if p is None or q is None:
        raise ValueError("Could not factor n")
    
    # Compute totient
    phi_n = (p - 1) * (q - 1)
    
    # Compute private exponent
    d = mod_inverse(e, phi_n)
    
    # Decrypt
    m = pow(c, d, n)
    
    # Convert to string - the decrypted number represents characters
    # Extract the meaningful character(s) from the number
    message_bytes = m.to_bytes((m.bit_length() + 7) // 8, 'big')
    message = message_bytes.decode('utf-8', errors='ignore').rstrip('\x00\x0b\x19')
    
    # If the above doesn't work well, try extracting just printable ASCII
    if not message or not message.isprintable():
        # Extract printable characters from the bytes
        printable_chars = ''.join(chr(b) for b in message_bytes if 32 <= b <= 126)
        if printable_chars:
            message = printable_chars
        else:
            # Fallback: check if it's a single character value
            if 32 <= m <= 126:
                message = chr(m)
            else:
                message = str(m)
    
    return f"FLAG{{{message}}}"


if __name__ == "__main__":
    try:
        result = main()
        print(result)
    except Exception as e:
        print(f"Error: {e}")