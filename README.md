# RSA Decryption Solution

This repository contains the solution to the RSA decryption challenge.

## Problem
Given RSA parameters:
- Modulus n = 12407072677633161347
- Public exponent e = 65537  
- Ciphertext c = 6680131599371095691

Decrypt the ciphertext to recover the original message.

## Solution
The solution is implemented in `solution.py` which:

1. Factors the modulus n into prime factors p and q using Pollard's rho algorithm
2. Computes the totient φ(n) = (p-1)(q-1)
3. Computes the private exponent d as the modular inverse of e modulo φ(n)
4. Decrypts the ciphertext by computing m = c^d mod n
5. Converts the numeric message to readable text

## Usage
```bash
python3 solution.py
```

## Result
The decrypted message is: **FLAG{A}**

## Verification
The solution has been verified by:
- Factorization: n = 4030677697 × 3078160451 ✓
- Round-trip encryption: encrypting the decrypted message gives back the original ciphertext ✓