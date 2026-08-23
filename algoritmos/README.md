# Algoritmos de Machine Learning 📦🤖

Paquete modular de algoritmos y herramientas auxiliares de visualización implementados desde cero para el curso de **Aprendizaje Automático** (FING - UdelaR).

---

## 📦 Módulos Disponibles

### 1. Aprendizaje Conceptual (`algoritmos.concept_learning`)
- [**`Hypothesis`**](./concept_learning.py): Representación vectorial de hipótesis con comodines (`?`), hipótesis nula (`Ø`), emparejamiento con instancias y orden parcial general/específico ($\ge_g, \le_g$).
- [**`FindS`**](./concept_learning.py): Algoritmo de generalización mínima guiado por ejemplos positivos.
- [**`CandidateElimination`**](./concept_learning.py): Algoritmo para calcular el **Espacio de Versiones** ($S$ y $G$) y clasificación de nuevas instancias.
- **Visualizador:** [**`concept_learning_visualizer.py`**](./concept_learning_visualizer.py) (`plot_version_space`, `print_step_by_step_trace`, `print_ascii_version_space`).

---

### 2. Árboles de Decisión (`algoritmos.decision_tree`)
- [**`ID3DecisionTree`**](./decision_tree.py): Algoritmo **ID3** con soporte para:
  - Criterios de división: Ganancia de Información (`gain`) y Tasa de Ganancia (`gain_ratio`).
  - Hiperparámetro `min_info_gain` (umbral de ganancia mínima para división).
  - Hiperparámetro `max_depth` (profundidad máxima del árbol).
  - Atributos continuos (búsqueda dinámica del mejor punto de corte).
  - Manejo de valores no vistos y valores faltantes.
  - Exportación a reglas lógicas DNF (`tree.to_rules()`).
- Funciones auxiliares: `entropy()`, `information_gain()`, `gain_ratio()`, `split_information()`.
- **Visualizador:** [**`decision_tree_visualizer.py`**](./decision_tree_visualizer.py) (`print_tree_ascii`, `plot_decision_tree`, `print_entropy_gain_table`).

---

### 3. Aprendizaje Bayesiano (`algoritmos.bayesian`)
- [**`NaiveBayesClassifier`**](./bayesian.py): Clasificador Bayesiano Sencillo (CBS / Naïve Bayes) con:
  - Estimación de probabilidades a priori $P(c)$ y condicionales $P(a_i \mid c)$.
  - Suavizado por **$m$-estimador** (parámetro $m$) y **suavizado de Laplace** (`use_laplace=True`).
  - Inferencia en escala logarítmica para evitar *underflow* numérico.
  - Desglose explicativo de cálculos intermedios (`explain_prediction()`).
- [**`BayesOptimalClassifier`**](./bayesian.py): Clasificador Bayesiano Óptimo que pondera un ensamble de hipótesis según sus probabilidades a posteriori $P(h \mid D)$.
- **Visualizador:** [**`bayesian_visualizer.py`**](./bayesian_visualizer.py) (`print_bayesian_trace`, `plot_prior_and_posterior`).

---

## 💡 Ejemplos de Uso Rápido

### Árboles de Decisión (ID3)
```python
from algoritmos import ID3DecisionTree, print_tree_ascii, plot_decision_tree

# 1. Datos de entrenamiento (ejemplo Jugar Tenis)
dataset = [
    {'Cielo': 'Soleado', 'Humedad': 'Alta', 'Viento': 'Debil', 'Jugar': 'No'},
    {'Cielo': 'Soleado', 'Humedad': 'Alta', 'Viento': 'Fuerte', 'Jugar': 'No'},
    {'Cielo': 'Nublado', 'Humedad': 'Alta', 'Viento': 'Debil', 'Jugar': 'Si'},
    {'Cielo': 'Lluvia', 'Humedad': 'Normal', 'Viento': 'Debil', 'Jugar': 'Si'},
]

# 2. Entrenar árbol ID3
tree = ID3DecisionTree(min_info_gain=0.01).fit(dataset, target_attr='Jugar')

# 3. Visualizar en ASCII y gráfico
print_tree_ascii(tree)
plot_decision_tree(tree)

# 4. Reglas DNF
print(tree.to_rules())
```

---

### Naïve Bayes (CBS con $m$-estimador)
```python
from algoritmos import NaiveBayesClassifier, print_bayesian_trace, plot_prior_and_posterior

# 1. Entrenar clasificador con m-estimador (m=1.0)
nb = NaiveBayesClassifier(m=1.0).fit(dataset, target_attr='Jugar')

# 2. Predecir e inspeccionar traza explicativa
consulta = {'Cielo': 'Soleado', 'Humedad': 'Normal', 'Viento': 'Fuerte'}
pred = nb.predict_one(consulta)
print(f"Predicción: {pred}")

print_bayesian_trace(nb, consulta)
plot_prior_and_posterior(nb, consulta)
```
