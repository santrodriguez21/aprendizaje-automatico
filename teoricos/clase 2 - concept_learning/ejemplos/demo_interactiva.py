"""
Demo interactiva de los algoritmos Find-S y Candidate-Elimination
utilizando el ejemplo clasico del teorico: "Cuando salva Pedro un examen?"
"""

import os
import sys

# Asegurar encoding UTF-8 en Windows si es necesario
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Agregar la raiz del repositorio al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from algoritmos import (
    FindS,
    CandidateElimination,
    print_step_by_step_trace,
    plot_version_space
)


def run_pedro_demo():
    print("=" * 80)
    print(" DEMO DIDACTICA: APRENDIZAJE CONCEPTUAL (CLASE 2)")
    print(" Problema: Cuando salva Pedro un examen?")
    print("=" * 80)

    # 1. Definicion del dominio de atributos
    domains = {
        'Dedicacion': ['Alta', 'Media', 'Baja'],
        'Dificultad': ['Alta', 'Media', 'Baja'],
        'Horario': ['Matutino', 'Nocturno'],
        'Humedad': ['Alta', 'Media', 'Baja'],
        'HumorDoc': ['Bueno', 'Malo']
    }

    # 2. Conjunto de entrenamiento D
    X = [
        ['Alta', 'Alta', 'Nocturno', 'Media', 'Bueno'],
        ['Baja', 'Media', 'Matutino', 'Alta', 'Malo'],
        ['Media', 'Alta', 'Nocturno', 'Media', 'Malo'],
        ['Media', 'Alta', 'Matutino', 'Alta', 'Bueno']
    ]
    y = ['SI', 'NO', 'SI', 'NO']

    print("\n[+] 1. CONJUNTO DE ENTRENAMIENTO (D):")
    print(f"{'#':<4} {'Dedicacion':<12} {'Dificultad':<12} {'Horario':<12} {'Humedad':<10} {'HumorDoc':<10} {'Pedro Salva?'}")
    print("-" * 75)
    for i, (row, label) in enumerate(zip(X, y), 1):
        print(f"x_{i:<2} {row[0]:<12} {row[1]:<12} {row[2]:<12} {row[3]:<10} {row[4]:<10} {label}")

    # 3. Ejecucion de Find-S
    print("\n" + "=" * 80)
    print(" [*] 2. ALGORITMO FIND-S (Busqueda de la hipotesis mas especifica)")
    print("=" * 80)
    fs = FindS(len(domains), list(domains.keys())).fit(X, y)
    for record in fs.history:
        step = record["step"]
        h = record["hypothesis"]
        action = record["action"]
        inst = record["instance"]
        print(f"Paso {step}: h_{step} = {h}")
        if inst:
            print(f"   Accion: {action} (Ejemplo: {inst}, {record['label']})")
    print(f"\n-> Hipotesis final Find-S: {fs.hypothesis}")

    # 4. Ejecucion de Candidate-Elimination
    print("\n" + "=" * 80)
    print(" [*] 3. ALGORITMO CANDIDATE-ELIMINATION (Espacio de Versiones)")
    print("=" * 80)
    ce = CandidateElimination(domains).fit(X, y)
    print_step_by_step_trace(ce)

    print("\n[OK] FRONTERAS FINALES DEL ESPACIO DE VERSIONES:")
    print(f"   Limite Especifico S_4 = {ce.S}")
    print(f"   Limite General    G_4 = {ce.G}")

    # 5. Clasificacion de nuevas instancias (Diapositiva 25)
    print("\n" + "=" * 80)
    print(" [*] 4. CLASIFICACION DE NUEVAS INSTANCIAS CON EL ESPACIO DE VERSIONES")
    print(" (Ejemplos planteados en la diapositiva 25)")
    print("=" * 80)

    test_cases = [
        ["Alta", "Alta", "Nocturno", "Media", "Malo"],
        ["Alta", "Baja", "Matutino", "Alta", "Bueno"],
        ["Alta", "Alta", "Nocturno", "Baja", "Bueno"],
        ["Alta", "Baja", "Nocturno", "Media", "Bueno"]
    ]

    for idx, test_inst in enumerate(test_cases, 1):
        res = ce.classify(test_inst)
        inst_str = ", ".join(f"{k}={v}" for k, v in zip(domains.keys(), test_inst))
        print(f"\nTest #{idx}: [{inst_str}]")
        print(f"   -> Clasificacion: {res['decision']}")
        print(f"   -> Detalle: {res['confidence']}")

    # 6. Guardar grafico en carpeta de salida (ignorada por git)
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_dir, exist_ok=True)
    output_img = os.path.join(output_dir, "espacio_de_versiones_pedro.png")
    plot_version_space(ce, title="Espacio de Versiones Final - Problema de Pedro", save_path=output_img)


if __name__ == "__main__":
    run_pedro_demo()
