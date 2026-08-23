"""
Demo interactiva de Árboles de Decisión (Algoritmo ID3)
Muestra:
1. Cálculo de Entropía y Ganancia de Información paso a paso.
2. Construcción y visualización del árbol en formato ASCII.
3. Extracción de reglas lógicas en Forma Normal Disyuntiva (DNF).
4. Manejo de atributos numéricos continuos.
5. Inferencia y predicción con nuevas instancias.
"""

import sys
import os

# Permitir importar desde la raíz del proyecto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from algoritmos import (
    ID3DecisionTree,
    print_tree_ascii,
    plot_decision_tree,
    print_entropy_gain_table,
    entropy,
    information_gain
)


def main():
    print("=" * 80)
    print("🌲 DEMO INTERACTIVA: ÁRBOLES DE DECISIÓN & ALGORITMO ID3")
    print("=" * 80)

    # 1. Dataset clásico de Jugar al Tenis (Tom Mitchell)
    tennis_dataset = [
        {'Cielo': 'Soleado',  'Temperatura': 'Caluroso', 'Humedad': 'Alta',   'Viento': 'Debil',  'Jugar': 'No'},
        {'Cielo': 'Soleado',  'Temperatura': 'Caluroso', 'Humedad': 'Alta',   'Viento': 'Fuerte', 'Jugar': 'No'},
        {'Cielo': 'Nublado',  'Temperatura': 'Caluroso', 'Humedad': 'Alta',   'Viento': 'Debil',  'Jugar': 'Si'},
        {'Cielo': 'Lluvia',   'Temperatura': 'Templado', 'Humedad': 'Alta',   'Viento': 'Debil',  'Jugar': 'Si'},
        {'Cielo': 'Lluvia',   'Temperatura': 'Frio',     'Humedad': 'Normal', 'Viento': 'Debil',  'Jugar': 'Si'},
        {'Cielo': 'Lluvia',   'Temperatura': 'Frio',     'Humedad': 'Normal', 'Viento': 'Fuerte', 'Jugar': 'No'},
        {'Cielo': 'Nublado',  'Temperatura': 'Frio',     'Humedad': 'Normal', 'Viento': 'Fuerte', 'Jugar': 'Si'},
        {'Cielo': 'Soleado',  'Temperatura': 'Templado', 'Humedad': 'Alta',   'Viento': 'Debil',  'Jugar': 'No'},
        {'Cielo': 'Soleado',  'Temperatura': 'Frio',     'Humedad': 'Normal', 'Viento': 'Debil',  'Jugar': 'Si'},
        {'Cielo': 'Lluvia',   'Temperatura': 'Templado', 'Humedad': 'Normal', 'Viento': 'Debil',  'Jugar': 'Si'},
        {'Cielo': 'Soleado',  'Temperatura': 'Templado', 'Humedad': 'Normal', 'Viento': 'Fuerte', 'Jugar': 'Si'},
        {'Cielo': 'Nublado',  'Temperatura': 'Templado', 'Humedad': 'Alta',   'Viento': 'Fuerte', 'Jugar': 'Si'},
        {'Cielo': 'Nublado',  'Temperatura': 'Caluroso', 'Humedad': 'Normal', 'Viento': 'Debil',  'Jugar': 'Si'},
        {'Cielo': 'Lluvia',   'Temperatura': 'Templado', 'Humedad': 'Alta',   'Viento': 'Fuerte', 'Jugar': 'No'},
    ]

    features = ['Cielo', 'Temperatura', 'Humedad', 'Viento']
    target = 'Jugar'

    print(f"\n📊 1. Dataset de Entrenamiento: Jugar al Tenis ({len(tennis_dataset)} instancias)")
    print_entropy_gain_table(tennis_dataset, target, features)

    # 2. Entrenar Árbol ID3
    print("🔨 2. Entrenando Árbol de Decisión con ID3...")
    tree = ID3DecisionTree(criterion='gain', min_info_gain=0.0).fit(tennis_dataset, target_attr=target)

    # 3. Visualizar en ASCII
    print("\n📜 3. Estructura del Árbol Entrenado (ASCII):")
    print("-" * 60)
    print_tree_ascii(tree)
    print("-" * 60)

    # 4. Reglas lógicas DNF
    print("\n📐 4. Reglas Lógicas (Forma Normal Disyuntiva / DNF):")
    for rule in tree.to_rules():
        print(f"   • {rule}")

    # 5. Inferencia con nueva instancia
    nueva_instancia = {'Cielo': 'Soleado', 'Temperatura': 'Frio', 'Humedad': 'Alta', 'Viento': 'Debil'}
    prediccion = tree.predict_one(nueva_instancia)
    probas = tree.predict_proba_one(nueva_instancia)

    print(f"\n🎯 5. Inferencia para nueva instancia:")
    print(f"   Instancia: {nueva_instancia}")
    print(f"   Predicción: '{prediccion}' (Probabilidades: {probas})")

    # 6. Ejemplo con Atributos Continuos (Examen 2021)
    print("\n" + "=" * 80)
    print("📈 6. EJEMPLO CON ATRIBUTOS NUMÉRICOS CONTINUOS (Examen 2021)")
    print("=" * 80)

    boardgame_dataset = [
        {'Genero': 'Estrategia', 'Dificultad': 30, 'Apto': 'No'},
        {'Genero': 'Aventura',   'Dificultad': 45, 'Apto': 'Si'},
        {'Genero': 'Estrategia', 'Dificultad': 32, 'Apto': 'Si'},
        {'Genero': 'Cartas',     'Dificultad': 25, 'Apto': 'Si'},
        {'Genero': 'Cartas',     'Dificultad': 70, 'Apto': 'No'},
    ]

    cont_tree = ID3DecisionTree(
        continuous_attributes={'Dificultad'},
        min_info_gain=0.01
    ).fit(boardgame_dataset, target_attr='Apto')

    print("\n📜 Árbol resultante con corte continuo sobre 'Dificultad':")
    print("-" * 60)
    print_tree_ascii(cont_tree)
    print("-" * 60)

    print("\n✅ Demostración completada exitosamente.")


if __name__ == '__main__':
    main()
