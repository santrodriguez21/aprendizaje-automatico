"""
Script de resolución y verificación para el Ejercicio 8: Intervalos de Confianza y Error Real
Cálculo de Desviación Estándar e Intervalos de Confianza al 95% para proporciones binomiales
"""

import math
from scipy import stats

def calcular_intervalo_error(n, r, nivel_confianza=0.95):
    """
    n: total de instancias
    r: aciertos
    k = n - r: errores
    """
    k = n - r
    error_s = k / n
    acc_s = r / n
    
    # Desviación estándar del estimador de error
    sigma = math.sqrt((error_s * (1 - error_s)) / n)
    
    # Valor crítico z para dos colas
    alpha = 1 - nivel_confianza
    z = stats.norm.ppf(1 - alpha / 2)  # 1.95996 para 95%
    
    margen_error = z * sigma
    ic_inf = max(0.0, error_s - margen_error)
    ic_sup = min(1.0, error_s + margen_error)
    
    return {
        "n": n, "r": r, "k": k,
        "acc": acc_s, "error_s": error_s,
        "sigma": sigma, "z": z, "margen": margen_error,
        "ic_inf": ic_inf, "ic_sup": ic_sup
    }

def main():
    print("=== EJERCICIO 8: INTERVALOS DE CONFIANZA PARA LA TASA REAL DE ERROR ===")
    
    # Caso a: n = 100, r = 83
    res_a = calcular_intervalo_error(100, 83)
    print("\n--- PARTE A) N = 100, 83 Aciertos ---")
    print(f"  Error muestral error_S(h) = {res_a['k']}/{res_a['n']} = {res_a['error_s']:.4f} ({res_a['error_s']*100:.1f}%)")
    print(f"  Desviacion Estandar (sigma) = sqrt({res_a['error_s']:.4f} * {1-res_a['error_s']:.4f} / {res_a['n']}) = {res_a['sigma']:.5f} ({res_a['sigma']*100:.3f}%)")
    print(f"  Valor critico z_(0.975) = {res_a['z']:.4f} ~= 1.96")
    print(f"  Margen de error = {res_a['z']:.4f} * {res_a['sigma']:.5f} = {res_a['margen']:.4f} ({res_a['margen']*100:.2f}%)")
    print(f"  Intervalo de Confianza 95%: [{res_a['ic_inf']:.4f}, {res_a['ic_sup']:.4f}] => [{res_a['ic_inf']*100:.2f}%, {res_a['ic_sup']*100:.2f}%]")
    
    # Caso b: n = 1000, r = 830
    res_b = calcular_intervalo_error(1000, 830)
    print("\n--- PARTE B) N = 1000, 830 Aciertos ---")
    print(f"  Error muestral error_S(h) = {res_b['k']}/{res_b['n']} = {res_b['error_s']:.4f} ({res_b['error_s']*100:.1f}%)")
    print(f"  Desviacion Estandar (sigma) = sqrt({res_b['error_s']:.4f} * {1-res_b['error_s']:.4f} / {res_b['n']}) = {res_b['sigma']:.5f} ({res_b['sigma']*100:.3f}%)")
    print(f"  Margen de error = {res_b['z']:.4f} * {res_b['sigma']:.5f} = {res_b['margen']:.4f} ({res_b['margen']*100:.2f}%)")
    print(f"  Intervalo de Confianza 95%: [{res_b['ic_inf']:.4f}, {res_b['ic_sup']:.4f}] => [{res_b['ic_inf']*100:.2f}%, {res_b['ic_sup']*100:.2f}%]")
    
    # Comparación
    factor_reduccion = res_a['sigma'] / res_b['sigma']
    print(f"\n--- COMPARACION ---")
    print(f"  Relacion de desviaciones estandar: {res_a['sigma']:.5f} / {res_b['sigma']:.5f} = {factor_reduccion:.4f} (Exactamente sqrt(10) ~= {math.sqrt(10):.4f})")
    print(f"  El intervalo con N=1000 es aproximadamente 3.16 veces mas estrecho que con N=100.")

if __name__ == "__main__":
    main()
