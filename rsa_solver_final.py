#!/usr/bin/env python3
"""
RSA Challenge Solution for math-200
Final clean implementation
"""

import math

def extended_gcd(a, b):
    """Extended Euclidean Algorithm."""
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(e, phi_n):
    """Compute modular inverse."""
    gcd, x, y = extended_gcd(e, phi_n)
    if gcd != 1:
        raise ValueError("Modular inverse does not exist")
    return (x % phi_n + phi_n) % phi_n

def factor_rsa_modulus(n):
    """Factor RSA modulus using optimized methods."""
    # Check near perfect square
    sqrt_n = int(math.sqrt(n))
    for i in range(max(2, sqrt_n - 1000), sqrt_n + 1000):
        if n % i == 0:
            return i, n // i
    
    # Pollard's rho algorithm
    def pollard_rho(n):
        if n % 2 == 0:
            return 2
        x = y = 2
        d = 1
        f = lambda x: (x * x + 1) % n
        
        while d == 1:
            x = f(x)
            y = f(f(y))
            d = math.gcd(abs(x - y), n)
        return d
    
    factor = pollard_rho(n)
    if factor != n and factor != 1:
        return factor, n // factor
    
    raise ValueError("Could not factor n")

def solve_rsa_challenge():
    """Solve the RSA challenge and return the flag."""
    # Challenge parameters
    n = 12407072677633161347
    e = 65537
    c = 6680131599371095691
    
    # Factor n
    p, q = factor_rsa_modulus(n)
    
    # Compute private key
    phi_n = (p - 1) * (q - 1)
    d = mod_inverse(e, phi_n)
    
    # Decrypt
    m = pow(c, d, n)
    
    # Convert to flag format
    # Interpret as ASCII bytes
    hex_str = hex(m)[2:]
    if len(hex_str) % 2 == 1:
        hex_str = '0' + hex_str
    
    message_bytes = bytes.fromhex(hex_str)
    message = message_bytes.decode('ascii', errors='ignore')
    
    return f"FLAG{{{message}}}"

if __name__ == "__main__":
    flag = solve_rsa_challenge()
    print(flag)
    
    # Save to file
    with open("flag.txt", "w") as f:
        f.write(flag)
    print(f"Flag saved to flag.txt")