#!/usr/bin/env python3
"""
RSA Decryption Challenge Solver
Solves the math-200 RSA challenge by factoring n and decrypting the ciphertext.
"""

import math

def extended_gcd(a, b):
    """Extended Euclidean Algorithm to find modular inverse."""
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(e, phi_n):
    """Compute modular inverse of e modulo phi_n."""
    gcd, x, y = extended_gcd(e, phi_n)
    if gcd != 1:
        raise ValueError("Modular inverse does not exist")
    return (x % phi_n + phi_n) % phi_n

def trial_division(n):
    """Simple trial division to factor n."""
    print(f"Factoring n = {n}")
    
    # Check small primes first
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            p = i
            q = n // i
            print(f"Found factors: {p} and {q}")
            return p, q
    
    raise ValueError(f"Could not factor {n}")

def factor_n(n):
    """Factor the modulus n into prime factors using optimized methods."""
    print(f"Factoring n = {n}")
    
    # Try Pollard's rho algorithm for faster factorization
    def pollard_rho(n):
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
        
        return d
    
    # First try some optimization - check if n is close to a perfect square
    sqrt_n = int(math.sqrt(n))
    for i in range(max(2, sqrt_n - 1000), sqrt_n + 1000):
        if n % i == 0:
            p = i
            q = n // i
            print(f"Found factors: {p} and {q}")
            return p, q
    
    # Try Pollard's rho
    try:
        factor = pollard_rho(n)
        if factor != n and factor != 1:
            p = factor
            q = n // factor
            print(f"Found factors: {p} and {q}")
            return p, q
    except:
        pass
    
    # Fallback to trial division for small factors
    limit = min(100000, int(math.sqrt(n)) + 1)
    for i in range(2, limit):
        if n % i == 0:
            p = i
            q = n // i
            print(f"Found factors: {p} and {q}")
            return p, q
    
    raise ValueError(f"Could not factor {n}")

def solve_rsa():
    """Solve the RSA challenge."""
    # Given parameters
    n = 12407072677633161347
    e = 65537
    c = 6680131599371095691
    
    print("RSA Challenge Parameters:")
    print(f"n = {n}")
    print(f"e = {e}")
    print(f"c = {c}")
    print()
    
    # Step 1: Factor n
    p, q = factor_n(n)
    print(f"p = {p}")
    print(f"q = {q}")
    print(f"Verification: p * q = {p * q} (should equal n = {n})")
    print()
    
    # Step 2: Compute totient φ(n) = (p-1)(q-1)
    phi_n = (p - 1) * (q - 1)
    print(f"φ(n) = (p-1)(q-1) = {phi_n}")
    print()
    
    # Step 3: Compute private exponent d
    d = mod_inverse(e, phi_n)
    print(f"d = e^(-1) mod φ(n) = {d}")
    print(f"Verification: (e * d) mod φ(n) = {(e * d) % phi_n} (should be 1)")
    print()
    
    # Step 4: Decrypt the ciphertext
    m = pow(c, d, n)
    print(f"Decrypted message (numeric): m = {m}")
    print()
    
    # Step 5: Convert to string
    # Try different interpretations of the numeric message
    print(f"Decrypted message (numeric): m = {m}")
    print(f"Message in binary: {bin(m)}")
    print(f"Message in hex: {hex(m)}")
    print()
    
    # Try different encoding methods
    results = []
    
    # Method 1: Direct ASCII interpretation
    try:
        if m < 256:  # Single byte
            char = chr(m)
            if char.isprintable():
                results.append(f"Single ASCII char: '{char}'")
        
        # Multiple bytes from hex
        message_hex = hex(m)[2:]  # Remove '0x' prefix
        if len(message_hex) % 2 == 1:
            message_hex = '0' + message_hex  # Add leading zero if odd length
        
        message_bytes = bytes.fromhex(message_hex)
        message_str = message_bytes.decode('ascii', errors='ignore')
        results.append(f"From hex bytes: '{message_str}'")
        
    except Exception as e:
        print(f"Error in hex conversion: {e}")
    
    # Method 2: Direct string conversion
    try:
        message_str = str(m)
        results.append(f"Direct numeric: '{message_str}'")
    except:
        pass
    
    # Method 3: Try interpreting as little-endian bytes
    try:
        byte_data = m.to_bytes((m.bit_length() + 7) // 8, 'little')
        message_str = byte_data.decode('ascii', errors='ignore')
        if message_str.strip():
            results.append(f"Little-endian bytes: '{message_str}'")
    except:
        pass
    
    # Method 4: Try interpreting as big-endian bytes  
    try:
        byte_data = m.to_bytes((m.bit_length() + 7) // 8, 'big')
        message_str = byte_data.decode('ascii', errors='ignore')
        if message_str.strip():
            results.append(f"Big-endian bytes: '{message_str}'")
    except:
        pass
    
    print("Possible interpretations:")
    for i, result in enumerate(results, 1):
        print(f"{i}. {result}")
    
    # Choose the most likely interpretation (first printable result)
    if results:
        # Extract the message from the first valid result
        for result in results:
            if "'" in result:
                message = result.split("'")[1]
                if message and message.isprintable():
                    flag = f"FLAG{{{message}}}"
                    print(f"\nSelected flag: {flag}")
                    return flag
    
    return None

if __name__ == "__main__":
    solve_rsa()