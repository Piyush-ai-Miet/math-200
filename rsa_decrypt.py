#!/usr/bin/env python3
"""
RSA Decryption Solution
Solves the RSA decryption problem with given parameters:
n = 12407072677633161347
e = 65537
c = 6680131599371095691
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
    # For RSA, n = p * q where p and q are primes
    
    # First try small primes for efficiency
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
    for p in small_primes:
        if n % p == 0:
            return p, n // p
    
    # Try Pollard's rho algorithm
    factor = pollard_rho(n)
    if factor and factor != n:
        return factor, n // factor
    
    # Fall back to trial division for smaller range
    sqrt_n = int(math.sqrt(n))
    # Only check up to a reasonable limit to avoid infinite loops
    limit = min(sqrt_n, 10**6)
    
    for i in range(51, limit, 2):  # Start after small primes, check odd numbers
        if n % i == 0:
            p = i
            q = n // i
            return p, q
    
    return None, None


def extended_gcd(a, b):
    """Extended Euclidean Algorithm to find gcd and coefficients."""
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


def decrypt_rsa():
    """Main function to decrypt the RSA ciphertext."""
    # Given parameters
    n = 12407072677633161347
    e = 65537
    c = 6680131599371095691
    
    print(f"RSA Parameters:")
    print(f"n = {n}")
    print(f"e = {e}")
    print(f"c = {c}")
    print()
    
    # Step 1: Factor n into p and q
    print("Step 1: Factoring n...")
    p, q = factor_n(n)
    if p is None or q is None:
        raise ValueError("Could not factor n")
    
    print(f"p = {p}")
    print(f"q = {q}")
    print(f"Verification: p * q = {p * q} (should equal n)")
    print()
    
    # Step 2: Compute totient phi(n) = (p-1)(q-1)
    phi_n = (p - 1) * (q - 1)
    print(f"Step 2: Computing φ(n)")
    print(f"φ(n) = (p-1)(q-1) = ({p}-1)({q}-1) = {phi_n}")
    print()
    
    # Step 3: Compute private exponent d
    print("Step 3: Computing private exponent d...")
    d = mod_inverse(e, phi_n)
    print(f"d = {d}")
    print(f"Verification: (e * d) mod φ(n) = {(e * d) % phi_n} (should be 1)")
    print()
    
    # Step 4: Decrypt the ciphertext
    print("Step 4: Decrypting ciphertext...")
    m = pow(c, d, n)
    print(f"m = c^d mod n = {c}^{d} mod {n} = {m}")
    print()
    
    # Step 5: Convert numeric message to string
    print("Step 5: Converting to string...")
    print(f"Numeric message: {m}")
    
    # Try different approaches to convert the number to a meaningful message
    approaches = []
    
    # Approach 1: Direct byte conversion
    try:
        if m > 0:
            message_bytes = m.to_bytes((m.bit_length() + 7) // 8, 'big')
            message1 = message_bytes.decode('utf-8', errors='ignore')
            approaches.append(("Direct bytes (big endian)", message1))
    except:
        pass
    
    # Approach 2: Little endian
    try:
        if m > 0:
            message_bytes = m.to_bytes((m.bit_length() + 7) // 8, 'little')
            message2 = message_bytes.decode('utf-8', errors='ignore')
            approaches.append(("Direct bytes (little endian)", message2))
    except:
        pass
    
    # Approach 3: ASCII character values
    try:
        if m < 256:  # Single ASCII character
            message3 = chr(m)
            approaches.append(("Single ASCII character", message3))
    except:
        pass
    
    # Approach 4: Multiple ASCII characters (if number represents concatenated ASCII values)
    try:
        temp_m = m
        chars = []
        while temp_m > 0:
            chars.append(chr(temp_m % 256))
            temp_m //= 256
        if chars:
            message4 = ''.join(reversed(chars))
            approaches.append(("Multi-char ASCII (big endian)", message4))
            message5 = ''.join(chars)
            approaches.append(("Multi-char ASCII (little endian)", message5))
    except:
        pass
    
    # Show all approaches
    for desc, msg in approaches:
        print(f"{desc}: '{msg}'")
    
    # Choose the most reasonable message
    if approaches:
        # Use the first approach that gives a non-empty readable result
        message = approaches[0][1]
        for desc, msg in approaches:
            if msg and msg.isprintable() and len(msg.strip()) > 0:
                message = msg
                print(f"Selected: {desc} -> '{message}'")
                break
    else:
        message = str(m)
        print(f"Fallback to string representation: '{message}'")
    
    # Format as FLAG
    flag = f"FLAG{{{message}}}"
    print(f"\nFinal result: {flag}")
    return flag


if __name__ == "__main__":
    try:
        result = decrypt_rsa()
        print(f"\n{result}")
    except Exception as e:
        print(f"Error: {e}")