"""
Script para el Ejercicio 2 - Práctico 2: Árboles de Decisión
Calcula y verifica la entropía del conjunto y la ganancia de información para a1 y a2.
"""

import math
import sys
import os

# Importar funciones del paquete local
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))
from algoritmos import entropy, information_gain, print_entropy_gain_table, ID3DecisionTree, print_tree_ascii


def main():
    dataset = [
        {'a1': 'V', 'a2': 'V', 'Clasif': 'Sí'},
        {'a1': 'V', 'a2': 'V', 'Clasif': 'Sí'},
        {'a1': 'V', 'a2': 'F', 'Clasif': 'No'},
        {'a1': 'F', 'a2': 'F', 'Clasif': 'Sí'},
        {'a1': 'F', 'a2': 'V', 'Clasif': 'No'},
        {'a1': 'F', 'a2': 'V', 'Clasif': 'No'},
    ]

    features = ['a1', 'a2']
    target = 'Clasif'

    print("=" * 70)
    print("EJERCICIO 2: CÁLCULO DE ENTROPÍA Y GANANCIA DE INFORMACIÓN")
    print("=" * 70)

    # a) Entropía base
    labels = [ex[target] for ex in dataset]
    h_s = entropy(labels)
    print(f"\na) Entropía del conjunto de entrenamiento H(S): {h_s:.4f} bits")

    # b) Ganancia para a1 y a2
    print("\nb) Ganancia de particionar por cada atributo:")
    print_entropy_gain_table(dataset, target, features)

    # Construcción completa del árbol
    tree = ID3DecisionTree().fit(dataset, target_attr=target)
    print("Árbol ID3 completo:")
    print_tree_ascii(tree)


if __name__ == '__main__':
    main()
