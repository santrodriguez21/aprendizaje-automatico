"""
Script para el Ejercicio 3 - Práctico 2: Árboles de Decisión
Construye el árbol ID3 para el problema de Pedro en la playa, evalúa la incorporación
de la instancia 5 y predice sobre las instancias 6 a 9.
"""

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))
from algoritmos import ID3DecisionTree, print_tree_ascii, print_entropy_gain_table


def main():
    features = ['Cielo', 'Temp', 'Humedad', 'Viento', 'Tmp_Agua', 'Tiempo']
    target = 'Juega'

    # 1. Dataset de 4 ejemplos (Parte a)
    d4 = [
        {'Cielo': 'Soleado',  'Temp': 'Templado', 'Humedad': 'Normal', 'Viento': 'Fuerte', 'Tmp_Agua': 'Templada', 'Tiempo': 'Sin cambios', 'Juega': 'Sí'},
        {'Cielo': 'Soleado',  'Temp': 'Templado', 'Humedad': 'Alta',   'Viento': 'Fuerte', 'Tmp_Agua': 'Templada', 'Tiempo': 'Sin cambios', 'Juega': 'Sí'},
        {'Cielo': 'Lluvioso', 'Temp': 'Frío',     'Humedad': 'Alta',   'Viento': 'Fuerte', 'Tmp_Agua': 'Templada', 'Tiempo': 'Cambiante',   'Juega': 'No'},
        {'Cielo': 'Soleado',  'Temp': 'Templado', 'Humedad': 'Alta',   'Viento': 'Fuerte', 'Tmp_Agua': 'Fría',     'Tiempo': 'Cambiante',   'Juega': 'Sí'},
    ]

    print("=" * 75)
    print("EJERCICIO 3: ID3 SOBRE EL PROBLEMA DE PEDRO JUEGA AL FÚTBOL")
    print("=" * 75)

    print("\n--- Parte a: Evaluación con 4 instancias ---")
    print_entropy_gain_table(d4, target, features)
    tree_a = ID3DecisionTree().fit(d4, target_attr=target, features=features)
    print("\nÁrbol ID3 (Parte a):")
    print_tree_ascii(tree_a)

    # 2. Dataset con 5 ejemplos (Parte b)
    d5 = d4 + [
        {'Cielo': 'Soleado',  'Temp': 'Templado', 'Humedad': 'Normal', 'Viento': 'Suave',  'Tmp_Agua': 'Templada', 'Tiempo': 'Sin cambios', 'Juega': 'No'},
    ]

    print("\n--- Parte b: Evaluación con 5 instancias (incorporando #5) ---")
    print_entropy_gain_table(d5, target, features)
    tree_b = ID3DecisionTree().fit(d5, target_attr=target, features=features)
    print("\nÁrbol ID3 (Parte b):")
    print_tree_ascii(tree_b)

    # 3. Predicción sobre instancias 6, 7, 8, 9 (Parte c)
    test_instances = [
        {'#': 6, 'Cielo': 'Soleado',  'Temp': 'Templado', 'Humedad': 'Normal', 'Viento': 'Fuerte', 'Tmp_Agua': 'Fría',     'Tiempo': 'Cambiante'},
        {'#': 7, 'Cielo': 'Lluvioso', 'Temp': 'Frío',     'Humedad': 'Normal', 'Viento': 'Suave',  'Tmp_Agua': 'Templada', 'Tiempo': 'Sin cambios'},
        {'#': 8, 'Cielo': 'Soleado',  'Temp': 'Templado', 'Humedad': 'Normal', 'Viento': 'Suave',  'Tmp_Agua': 'Templada', 'Tiempo': 'Sin cambios'},
        {'#': 9, 'Cielo': 'Soleado',  'Temp': 'Frío',     'Humedad': 'Normal', 'Viento': 'Fuerte', 'Tmp_Agua': 'Templada', 'Tiempo': 'Sin cambios'},
    ]

    print("\n--- Parte c: Predicciones sobre instancias de test ---")
    for inst in test_instances:
        pred_a = tree_a.predict_one(inst)
        pred_b = tree_b.predict_one(inst)
        print(f"Instancia #{inst['#']}: Predicción Árbol (a) = '{pred_a}' | Predicción Árbol (b) = '{pred_b}'")


if __name__ == '__main__':
    main()
