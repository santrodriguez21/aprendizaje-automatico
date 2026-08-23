"""
Demo interactiva de Aprendizaje Bayesiano (Naïve Bayes / CBS)
Muestra:
1. Inferencia Bayesiana con Teorema de Bayes (ejemplo clásico de test médico/dopaje).
2. Estimación de probabilidades y clasificación con Naïve Bayes (CBS).
3. Efecto del suavizado por m-estimador y Laplace frente a frecuencias cero.
4. Desglose explicativo paso a paso de predicciones.
"""

import sys
import os

# Permitir importar desde la raíz del proyecto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from algoritmos import (
    NaiveBayesClassifier,
    BayesOptimalClassifier,
    print_bayesian_trace,
    plot_prior_and_posterior
)


def main():
    print("=" * 80)
    print("🔮 DEMO INTERACTIVA: APRENDIZAJE BAYESIANO & NAÏVE BAYES (CBS)")
    print("=" * 80)

    # 1. Dataset de Clasificación de Películas (Examen 2025)
    movies_dataset = [
        {'Genero': 'accion',          'Director': 'Nolan',      'Actor': 'Hathaway', 'Critica': 'Buena'},
        {'Genero': 'ciencia ficcion', 'Director': 'Villeneuve', 'Actor': 'Damon',    'Critica': 'Buena'},
        {'Genero': 'drama',           'Director': 'Nolan',      'Actor': 'Damon',    'Critica': 'Regular'},
        {'Genero': 'ciencia ficcion', 'Director': 'Villeneuve', 'Actor': 'Ferguson', 'Critica': 'Regular'},
        {'Genero': 'drama',           'Director': 'Scott',      'Actor': 'Ferguson', 'Critica': 'Buena'},
        {'Genero': 'accion',          'Director': 'Scott',      'Actor': 'Hathaway', 'Critica': 'Mala'},
    ]

    target = 'Critica'
    features = ['Genero', 'Director', 'Actor']

    print(f"\n📊 1. Dataset de Entrenamiento: Críticas de Películas ({len(movies_dataset)} instancias)")
    for i, ex in enumerate(movies_dataset, 1):
        print(f"   #{i}: {ex['Genero']:<16} | {ex['Director']:<12} | {ex['Actor']:<10} -> {ex['Critica']}")

    # 2. Entrenar Naïve Bayes sin suavizado (m=0)
    print("\n🔨 2. Entrenando Clasificador Naïve Bayes estándar (m=0)...")
    nb_ml = NaiveBayesClassifier(m=0.0).fit(movies_dataset, target_attr=target, features=features)

    # 3. Consulta de prueba (Instancia #7 del Examen 2025)
    consulta = {'Genero': 'ciencia ficcion', 'Director': 'Nolan', 'Actor': 'Ferguson'}
    print(f"\n🔍 3. Consulta a evaluar: {consulta}")
    print_bayesian_trace(nb_ml, consulta)

    # 4. Comparación con m-estimador (m=1.0)
    print("\n" + "=" * 80)
    print("🧪 4. EFECTO DEL SUAVIZADO CON m-ESTIMADOR (m=1.0)")
    print("=" * 80)
    nb_m1 = NaiveBayesClassifier(m=1.0).fit(movies_dataset, target_attr=target, features=features)
    print_bayesian_trace(nb_m1, consulta)

    # 5. Ejemplo de Clasificador Bayesiano Óptimo (Ensamble de hipótesis ponderadas)
    print("\n" + "=" * 80)
    print("👑 5. CLASIFICADOR BAYESIANO ÓPTIMO (COMBINACIÓN DE HIPÓTESIS)")
    print("=" * 80)

    # Supongamos 3 hipótesis h1, h2, h3 con probabilidades a posteriori P(h|D)
    class DummyHypothesis:
        def __init__(self, pred_map):
            self.pred_map = pred_map
        def predict_one(self, x):
            return self.pred_map.get(x['Genero'], 'Buena')

    h1 = DummyHypothesis({'accion': 'Mala', 'ciencia ficcion': 'Buena', 'drama': 'Regular'})
    h2 = DummyHypothesis({'accion': 'Mala', 'ciencia ficcion': 'Regular', 'drama': 'Buena'})
    h3 = DummyHypothesis({'accion': 'Buena', 'ciencia ficcion': 'Regular', 'drama': 'Regular'})

    # P(h1|D) = 0.4, P(h2|D) = 0.4, P(h3|D) = 0.2
    boc = BayesOptimalClassifier(
        hypotheses=[h1, h2, h3],
        hypothesis_posteriors=[0.4, 0.4, 0.2]
    )

    opt_pred = boc.predict_one(consulta)
    opt_proba = boc.predict_proba_one(consulta)

    print(f"   Instancia: {consulta}")
    print(f"   Probabilidades del Clasificador Óptimo: {opt_proba}")
    print(f"   Predicción Óptima: '{opt_pred}'")

    print("\n✅ Demostración completada exitosamente.")


if __name__ == '__main__':
    main()
