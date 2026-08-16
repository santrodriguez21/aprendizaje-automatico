"""
Ejercicio 4: Implementación de Find-S y Simulación de Aprendizaje Conceptual
=============================================================================
Práctico 1: Introducción y Aprendizaje Conceptual
Curso: Aprendizaje Automático

Contenido:
  a) Implementación del algoritmo Find-S.
  b) Verificación con los datos de 'Pedro salva un examen' del teórico.
  c) Simulación de Monte Carlo: generación aleatoria de instancias para aprender
     el concepto objetivo <?, Media, ?, ?, ?> y estimación del número promedio
     de ejemplos únicos totales y positivos necesarios.
"""

import itertools
import random
from typing import List, Tuple, Set
import numpy as np

# ==========================================
# 1. Definición del Espacio de Instancias
# ==========================================
ATRIBUTOS = {
    'Dedicacion': ['Alta', 'Media', 'Baja'],
    'Dificultad': ['Alta', 'Media', 'Baja'],
    'Horario': ['Matutino', 'Nocturno'],
    'Humedad': ['Alta', 'Media', 'Baja'],
    'HumorDoc': ['Bueno', 'Malo']
}

NOMBRES_ATRIBUTOS = list(ATRIBUTOS.keys())
N_ATTRS = len(NOMBRES_ATRIBUTOS)

# Espacio de instancias completo |X| = 3 * 3 * 2 * 3 * 2 = 108
TODAS_LAS_INSTANCIAS: List[Tuple[str, ...]] = list(
    itertools.product(*[ATRIBUTOS[k] for k in NOMBRES_ATRIBUTOS])
)


# ==========================================
# 2. Algoritmo Find-S (Parte a)
# ==========================================
def find_s(ejemplos: List[Tuple[Tuple[str, ...], int]]) -> List[str]:
    """
    Aprende la hipótesis conjuntiva más específica consistente con los ejemplos positivos.
    
    Args:
        ejemplos: Lista de tuplas (instancia, etiqueta) donde etiqueta es 1 (Sí) o 0 (No).
        
    Returns:
        Vector de hipótesis aprendida con valores literales o '?'.
    """
    # Inicialización con la hipótesis nula más específica
    h = ['∅'] * N_ATTRS
    
    for instancia, label in ejemplos:
        if label == 1:  # Find-S solo procesa ejemplos positivos
            if h == ['∅'] * N_ATTRS:
                h = list(instancia)
            else:
                for i in range(N_ATTRS):
                    if h[i] != instancia[i]:
                        h[i] = '?'
    return h


# ==========================================
# 3. Verificación con el Teórico (Parte b)
# ==========================================
def verificar_ejemplo_teorico() -> None:
    print("=" * 60)
    print("Parte b) Verificación de Find-S con el Teórico (Pedro Examen)")
    print("=" * 60)
    
    datos_teorico = [
        (('Alta', 'Alta', 'Nocturno', 'Media', 'Bueno'), 1),   # x1 (+)
        (('Baja', 'Media', 'Matutino', 'Alta', 'Malo'), 0),     # x2 (-)
        (('Media', 'Alta', 'Nocturno', 'Media', 'Malo'), 1),   # x3 (+)
        (('Media', 'Alta', 'Matutino', 'Alta', 'Bueno'), 0),   # x4 (-)
    ]
    
    h_resultado = find_s(datos_teorico)
    h_esperada = ['?', 'Alta', 'Nocturno', 'Media', '?']
    
    print(f"Hipótesis aprendida: {h_resultado}")
    print(f"Hipótesis esperada:  {h_esperada}")
    assert h_resultado == h_esperada, "Error: la hipótesis no coincide con el teórico."
    print("-> Verificación EXITOSA: Coincide exactamente con el teórico.\n")


# ==========================================
# 4. Simulación Monte Carlo (Parte c)
# ==========================================
CONCEPTO_OBJETIVO = ['?', 'Media', '?', '?', '?']

def clasificar_con_concepto(instancia: Tuple[str, ...], concepto: List[str]) -> int:
    """Evalúa si una instancia satisface una hipótesis conjuntiva."""
    for val_inst, val_conc in zip(instancia, concepto):
        if val_conc != '?' and val_conc != val_inst:
            return 0
    return 1

def simular_corrida() -> Tuple[int, int]:
    """
    Ejecuta una corrida de aprendizaje generando instancias aleatorias hasta que
    Find-S converge exactamente al concepto objetivo.
    """
    h = ['∅'] * N_ATTRS
    instancias_unicas_vistas: Set[Tuple[str, ...]] = set()
    positivos_unicos_vistos: Set[Tuple[str, ...]] = set()
    
    while h != CONCEPTO_OBJETIVO:
        # Muestreo aleatorio uniforme con reemplazo del universo X
        inst = random.choice(TODAS_LAS_INSTANCIAS)
        instancias_unicas_vistas.add(inst)
        
        label = clasificar_con_concepto(inst, CONCEPTO_OBJETIVO)
        if label == 1:
            positivos_unicos_vistos.add(inst)
            if h == ['∅'] * N_ATTRS:
                h = list(inst)
            else:
                for i in range(N_ATTRS):
                    if h[i] != inst[i]:
                        h[i] = '?'
                        
    return len(instancias_unicas_vistas), len(positivos_unicos_vistos)

def ejecutar_simulaciones(n_repeticiones: int = 10000) -> None:
    print("=" * 60)
    print(f"Parte c) Simulación Monte Carlo ({n_repeticiones:,} repeticiones)")
    print(f"Concepto Objetivo: {CONCEPTO_OBJETIVO}")
    print("=" * 60)
    
    totales_unicos = []
    positivos_unicos = []
    
    for _ in range(n_repeticiones):
        u_tot, u_pos = simular_corrida()
        totales_unicos.append(u_tot)
        positivos_unicos.append(u_pos)
        
    media_tot = np.mean(totales_unicos)
    std_tot = np.std(totales_unicos)
    media_pos = np.mean(positivos_unicos)
    std_pos = np.std(positivos_unicos)
    
    print(f"Instancias en el espacio X:            {len(TODAS_LAS_INSTANCIAS)}")
    print(f"Instancias positivas de c en X:        {len([x for x in TODAS_LAS_INSTANCIAS if clasificar_con_concepto(x, CONCEPTO_OBJETIVO) == 1])}")
    print("-" * 60)
    print(f"Promedio de ejemplos ÚNICOS TOTALES:   {media_tot:.2f} ± {std_tot:.2f}")
    print(f"Promedio de ejemplos ÚNICOS POSITIVOS: {media_pos:.2f} ± {std_pos:.2f}")
    print("=" * 60)


if __name__ == '__main__':
    verificar_ejemplo_teorico()
    ejecutar_simulaciones(10000)
