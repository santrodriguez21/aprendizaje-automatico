"""
Ejercicio 2: Algoritmo Candidate-Elimination y Visualizador (Pedro Fútbol Playa)
================================================================================
Práctico 1: Introducción y Aprendizaje Conceptual
Curso: Aprendizaje Automático

Aprende el Espacio de Versiones (S y G) para el caso de fútbol playa,
muestra la traza paso a paso, clasifica las instancias 5 a 8 y genera
el gráfico visual de la retícula del Espacio de Versiones.
"""

import os
import sys

# Asegurar encoding UTF-8 en Windows
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Agregar la raíz del repositorio al path para importar algoritmos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..")))

from algoritmos import (
    CandidateElimination,
    print_step_by_step_trace,
    plot_version_space
)


def run_ejercicio_02():
    print("=" * 80)
    print(" EJERCICIO 2: CANDIDATE-ELIMINATION (PEDRO JUEGA AL FÚTBOL EN LA PLAYA)")
    print("=" * 80)

    # 1. Definición del dominio de atributos
    domains = {
        'Cielo': ['Soleado', 'Lluvioso', 'Nublado'],
        'Temp': ['Templado', 'Frío'],
        'Humedad': ['Normal', 'Alta'],
        'Viento': ['Fuerte', 'Suave'],
        'TmpAgua': ['Templada', 'Fría'],
        'Tiempo': ['Sin cambios', 'Cambiante']
    }

    # 2. Conjunto de entrenamiento D (Tabla del Ejercicio 2)
    X = [
        ['Soleado', 'Templado', 'Normal', 'Fuerte', 'Templada', 'Sin cambios'],
        ['Soleado', 'Templado', 'Alta', 'Fuerte', 'Templada', 'Sin cambios'],
        ['Lluvioso', 'Frío', 'Alta', 'Fuerte', 'Templada', 'Cambiante'],
        ['Soleado', 'Templado', 'Alta', 'Fuerte', 'Fría', 'Cambiante']
    ]
    y = ['SÍ', 'SÍ', 'NO', 'SÍ']

    print("\n[+] 1. CONJUNTO DE ENTRENAMIENTO (D):")
    print(f"{'#':<4} {'Cielo':<10} {'Temp':<10} {'Humedad':<10} {'Viento':<10} {'TmpAgua':<10} {'Tiempo':<12} {'Juega?'}")
    print("-" * 75)
    for i, (row, label) in enumerate(zip(X, y), 1):
        print(f"x_{i:<2} {row[0]:<10} {row[1]:<10} {row[2]:<10} {row[3]:<10} {row[4]:<10} {row[5]:<12} {label}")

    # 3. Ejecución de Candidate-Elimination
    ce = CandidateElimination(domains)
    ce.fit(X, y)

    # 4. Mostrar traza paso a paso con el visualizador
    print_step_by_step_trace(ce)

    print("\n[OK] FRONTERAS FINALES DEL ESPACIO DE VERSIONES:")
    print(f"   Límite Específico S_4 = {ce.S}")
    print(f"   Límite General    G_4 = {ce.G}")

    # 5. Clasificación de instancias de prueba 5 a 8 (Parte iii)
    print("\n" + "=" * 80)
    print(" [*] CLASIFICACIÓN DE NUEVAS INSTANCIAS DE PRUEBA (#5 a #8)")
    print("=" * 80)

    test_cases = [
        (5, ['Soleado', 'Templado', 'Normal', 'Fuerte', 'Fría', 'Cambiante']),
        (6, ['Lluvioso', 'Frío', 'Normal', 'Suave', 'Templada', 'Sin cambios']),
        (7, ['Soleado', 'Templado', 'Normal', 'Suave', 'Templada', 'Sin cambios']),
        (8, ['Soleado', 'Frío', 'Normal', 'Fuerte', 'Templada', 'Sin cambios'])
    ]

    for num, test_inst in test_cases:
        res = ce.classify(test_inst)
        inst_str = ", ".join(f"{k}={v}" for k, v in zip(domains.keys(), test_inst))
        print(f"\nInstancia #{num}: [{inst_str}]")
        print(f"   -> Clasificación: {res['decision']}")
        print(f"   -> Detalle:       {res['confidence']}")

    # 6. Generar y guardar el gráfico del Espacio de Versiones
    output_dir = os.path.join(os.path.dirname(__file__), "..", "output")
    os.makedirs(output_dir, exist_ok=True)
    output_img = os.path.join(output_dir, "espacio_de_versiones_ejercicio_02.png")
    
    print("\n" + "=" * 80)
    print(f" [*] GENERANDO GRÁFICO DEL ESPACIO DE VERSIONES...")
    plot_version_space(
        ce,
        title="Espacio de Versiones ($VS_{H,D}$) - Ejercicio 2 (Fútbol Playa)",
        save_path=output_img,
        show_plot=False
    )
    print(f" [OK] Gráfico guardado en: {output_img}")
    print("=" * 80)


if __name__ == '__main__':
    run_ejercicio_02()
