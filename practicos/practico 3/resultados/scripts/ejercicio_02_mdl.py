"""
Script de verificación para el Ejercicio 2 (MDL)
Simula la selección de hipótesis bajo el principio de Minimum Description Length
"""

import math

def description_length(k, e, n, m):
    """
    L(h) = k * log2(n)
    L(D|h) = e * log2(m)
    MDL = L(h) + L(D|h)
    """
    l_h = k * math.log2(n) if n > 1 else 0
    l_d_given_h = e * math.log2(m) if m > 1 else 0
    return l_h + l_d_given_h, l_h, l_d_given_h

def main():
    print("=== SIMULACIÓN EJERCICIO 2: PRINCIPIO MDL ===")
    n = 10  # 10 atributos booleanos
    m = 20  # 20 ejemplos
    
    # Hipótesis 1: Consistente pero compleja (k=6 atributos, 0 errores)
    k1, e1 = 6, 0
    mdl1, lh1, ld1 = description_length(k1, e1, n, m)
    
    # Hipótesis 2: Simple pero con 1 error (k=1 atributo, 1 error)
    k2, e2 = 1, 1
    mdl2, lh2, ld2 = description_length(k2, e2, n, m)
    
    print(f"Parámetros: n = {n} atributos, m = {m} ejemplos")
    print(f"Hipótesis Compleja Consistente (k={k1}, e={e1}):")
    print(f"  L(h) = {lh1:.3f} bits, L(D|h) = {ld1:.3f} bits => MDL = {mdl1:.3f} bits")
    print(f"Hipótesis Simple con 1 error (k={k2}, e={e2}):")
    print(f"  L(h) = {lh2:.3f} bits, L(D|h) = {ld2:.3f} bits => MDL = {mdl2:.3f} bits")
    
    if mdl2 < mdl1:
        print("\n=> RESULTADO: MDL prefiere la hipótesis con 1 error porque su costo de descripción total es menor.")
        print(f"   Diferencia a favor de h_simple: {mdl1 - mdl2:.3f} bits.")
    else:
        print("\n=> RESULTADO: MDL prefiere la hipótesis consistente.")

if __name__ == "__main__":
    main()
