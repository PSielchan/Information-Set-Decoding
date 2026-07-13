"""
Prange ISD Demonstrator

Demonstrator ataku Information Set Decoding (ISD) według algorytmu Prange'a
na kryptosystemie kodowym McEliece.

Autor: Piotr Sielchanowicz
"""

import random
import numpy as np
import galois

# 1. Parametry systemu

# Używamy ciała Galois GF(2^4) = GF(16)
M = 4
t = 2  # liczba błędów

GF16 = galois.GF(2**M)

# Tworzymy losowy wielomian nierozkładalny stopnia t=2 nad GF(16)
g = galois.irreducible_poly(GF16.order, t, method="random")

L = GF16.elements
n = len(L)

# print(f"Wielomian Goppy g(x): {g}")
# print(f"Długość kodu n = {n}, maksymalna liczba błędów t = {t}")


# 2. Generowanie macierzy kodu Goppy

def generate_goppa_matrices(g, L):
    """
    Generuje binarną macierz generującą G oraz weryfikacji parzystości H.
    """
    n = len(L)
    t = g.degree
    
    H_gf = GF16.Zeros((t, n))
    for j in range(n):
        g_val = g(L[j])
        g_inv = GF16(1) / g_val
        for i in range(t):
            H_gf[i, j] = g_inv * (L[j]**i)
            
    # Konwersja H_gf na postać binarną nad GF(2)
    H_bin_list = []
    for r in range(t):
        row_bits = []
        for c in range(n):
            val = int(H_gf[r, c])
            bits = [(val >> b) & 1 for b in range(M)]
            row_bits.append(bits)
        H_bin_list.extend(np.array(row_bits).T.tolist())
        
    GF2 = galois.GF(2)
    H_bin = GF2(H_bin_list)
    
    # Sprowadzamy do postaci zredukowanej schodkowej
    H_rref = H_bin.row_reduce()
    
    pivots = []
    r = 0
    for c in range(n):
        if r < H_rref.shape[0] and H_rref[r, c] == 1:
            pivots.append(c)
            r += 1
            
    free_cols = sorted(list(set(range(n)) - set(pivots)))
    k = len(free_cols)
    
    # Budujemy binarną macierz generującą G (jądro macierzy H_bin)
    G = GF2.Zeros((k, n))
    for i, free in enumerate(free_cols):
        G[i, free] = 1
        for r_idx, pivot in enumerate(pivots):
            G[i, pivot] = H_rref[r_idx, free]
            
    return G, H_bin, k


G, H_bin, k = generate_goppa_matrices(g, L)
GF2 = galois.GF(2)


# 3. Generowanie kluczy McEliece (Maskowanie S, G, P)

while True:
    S = GF2.Random((k, k))
    if np.linalg.matrix_rank(S) == k:
        S_inv = np.linalg.inv(S)
        break

P_indices = np.random.permutation(n)
P = GF2(np.eye(n, dtype=int)[P_indices])
P_inv = P.T

G_pub = S @ G @ P

print(f"Wymiary klucza publicznego: {G_pub.shape} (k = {k}, n = {n})")


# 4. Szyfrowanie i deszyfrowanie McEliece

# Szyfrowanie
message = GF2.Random(k)
error = GF2.Zeros(n)
error_positions = random.sample(range(n), t)
for pos in error_positions:
    error[pos] = 1

ciphertext = (message @ G_pub) + error

print(f"\nOryginalna wiadomość (m):  {message}")
print(f"Dodany błąd (e):           {error}")
print(f"Szyfrogram (c):            {ciphertext}")

# Deszyfrowanie kluczem prywatnym
def decrypt_mceliece(c):
    # Zdejmujemy permutację P
    c_prime = c @ P_inv
    
    # Przeszukujemy przestrzeń błędów o wadze <= t
    syndrom_target = H_bin @ c_prime
    
    corrected_c_prime = c_prime.copy()
    found = False
    
    # Sprawdzamy błędy wagi 1 i 2
    for i in range(n):
        e_test = GF2.Zeros(n)
        e_test[i] = 1
        if np.array_equal(H_bin @ e_test, syndrom_target):
            corrected_c_prime = c_prime ^ e_test
            found = True
            break
            
    if not found:
        for i in range(n):
            for j in range(i + 1, n):
                e_test = GF2.Zeros(n)
                e_test[i] = 1
                e_test[j] = 1
                if np.array_equal(H_bin @ e_test, syndrom_target):
                    corrected_c_prime = c_prime ^ e_test
                    found = True
                    break
                    
    # Wycinamy m' z odzyskanego słowa kodowego
    H_rref = H_bin.row_reduce()
    pivots = []
    r = 0
    for c_idx in range(n):
        if r < H_rref.shape[0] and H_rref[r, c_idx] == 1:
            pivots.append(c_idx)
            r += 1
    free_cols = sorted(list(set(range(n)) - set(pivots)))
    
    m_prime = corrected_c_prime[free_cols]
    
    # Zdejmujemy maskowanie S
    decrypted = m_prime @ S_inv
    return decrypted

# Test deszyfrowania

decrypted_msg = decrypt_mceliece(ciphertext)
print(f"Deszyfrowanie kluczem prywatnym:")
print(f"Wynik:                     {decrypted_msg}")


# -------------------------------------------------------------------------


# 5. Atak ISD Prange'a

def prange_attack(c, G_pub, error_weight, max_iterations=10000):
    k, n = G_pub.shape
    print("\n=== ISD PRANGE ATTACK ===")
    
    for iteration in range(1, max_iterations + 1):
        info_set = sorted(random.sample(range(n), k))
        G_I = G_pub[:, info_set]
        
        # Sprawdzamy odwracalność w GF(2) przy użyciu rzędu macierzy
        if np.linalg.matrix_rank(G_I) != k:
            continue
            
        G_I_inv = np.linalg.inv(G_I)
        
        c_I = c[info_set]
        m_candidate = c_I @ G_I_inv
        
        codeword_candidate = m_candidate @ G_pub
        error_candidate = c ^ codeword_candidate
        
        # Waga Hamminga wektora w galois
        weight = np.sum(error_candidate == 1)
        
        if weight == error_weight:
            print(f"SUCCESS! Atak powiódł się w {iteration} iteracji.")
            return m_candidate, error_candidate
            
    print("Atak nie powiódł się.")
    return None

recovered_m, _ = prange_attack(ciphertext, G_pub, t)
if recovered_m is not None:
    print(f"Odzyskana wiadomość przez ISD: {recovered_m}")
    print(f"Poprawność wiadomości:         {np.array_equal(message, recovered_m)}")