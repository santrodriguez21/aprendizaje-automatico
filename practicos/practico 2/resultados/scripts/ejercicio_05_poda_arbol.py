"""
Script para el Ejercicio 5 - Práctico 2: Poda de Árboles de Decisión
Simula el entrenamiento con instancias 1-5 y la evaluación del procedimiento de poda
contra el conjunto de validación (instancias 6-7).
"""

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))
from algoritmos import ID3DecisionTree, print_tree_ascii


def main():
    train_data = [
        {'Cielo': 'Soleado',  'Temp': 'Templado', 'Humedad': 'Normal', 'Viento': 'Fuerte', 'Tmp_Agua': 'Templada', 'Tiempo': 'Sin cambios', 'Juega': 'Sí'},
        {'Cielo': 'Soleado',  'Temp': 'Templado', 'Humedad': 'Alta',   'Viento': 'Fuerte', 'Tmp_Agua': 'Templada', 'Tiempo': 'Sin cambios', 'Juega': 'Sí'},
        {'Cielo': 'Lluvioso', 'Temp': 'Frío',     'Humedad': 'Alta',   'Viento': 'Fuerte', 'Tmp_Agua': 'Templada', 'Tiempo': 'Cambiante',   'Juega': 'No'},
        {'Cielo': 'Soleado',  'Temp': 'Templado', 'Humedad': 'Alta',   'Viento': 'Fuerte', 'Tmp_Agua': 'Fría',     'Tiempo': 'Cambiante',   'Juega': 'Sí'},
        {'Cielo': 'Soleado',  'Temp': 'Templado', 'Humedad': 'Normal', 'Viento': 'Suave',  'Tmp_Agua': 'Templada', 'Tiempo': 'Sin cambios', 'Juega': 'No'},
    ]

    val_data = [
        {'Cielo': 'Soleado',  'Temp': 'Templado', 'Humedad': 'Normal', 'Viento': 'Fuerte', 'Tmp_Agua': 'Fría',     'Tiempo': 'Suave',       'Juega': 'Sí'},
        {'Cielo': 'Lluvioso', 'Temp': 'Frío',     'Humedad': 'Normal', 'Viento': 'Suave',  'Tmp_Agua': 'Templada', 'Tiempo': 'Sin cambios', 'Juega': 'No'},
    ]

    features = ['Cielo', 'Temp', 'Humedad', 'Viento', 'Tmp_Agua', 'Tiempo']
    target = 'Juega'

    print("=" * 75)
    print("EJERCICIO 5: PODA BASADA EN VALIDACIÓN (REDUCED ERROR PRUNING)")
    print("=" * 75)

    tree = ID3DecisionTree().fit(train_data, target_attr=target, features=features)
    print("\n1. Árbol inicial entrenado con instancias 1 a 5:")
    print_tree_ascii(tree)

    print("\n2. Evaluación en conjunto de validación (instancias 6 y 7):")
    for i, ex in enumerate(val_data, 6):
        pred = tree.predict_one(ex)
        correct = (pred == ex[target])
        print(f"   Instancia #{i}: Real='{ex[target]}', Predicción Árbol='{pred}' -> {'Correcto ✅' if correct else 'Error ❌'}")

    print("\n3. Evaluación de poda en el nodo raíz (reemplazar por 'Sí'):")
    root_val_preds = ['Sí' for _ in val_data]
    acc_root = sum(p == ex[target] for p, ex in zip(root_val_preds, val_data)) / len(val_data)
    print(f"   Exactitud podando la raíz: {acc_root:.1%}")
    print(f"   Exactitud del árbol completo: 100.0%")
    print("   -> Como el árbol completo supera a la poda en la raíz (100% vs 50%), la raíz NO se poda.")


if __name__ == '__main__':
    main()
