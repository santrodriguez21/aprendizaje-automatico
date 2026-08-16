# Algoritmos de Machine Learning

Paquete modular de algoritmos y herramientas auxiliares de visualización implementados desde cero para el curso.

---

## 📦 Módulos Disponibles

### 1. Aprendizaje Conceptual (`algoritmos.concept_learning`)
- [**`Hypothesis`**](file:///c:/Users/santr/aprendizaje-automatico/aprendizaje-automatico/algoritmos/concept_learning.py): Representación vectorial de hipótesis con comodines (`?`), hipótesis nula (`Ø`), emparejamiento con instancias y orden parcial general/específico ($\ge_g, \le_g$).
- [**`FindS`**](file:///c:/Users/santr/aprendizaje-automatico/aprendizaje-automatico/algoritmos/concept_learning.py): Algoritmo de generalización mínima guiado por ejemplos positivos.
- [**`CandidateElimination`**](file:///c:/Users/santr/aprendizaje-automatico/aprendizaje-automatico/algoritmos/concept_learning.py): Algoritmo de cálculo del **Espacio de Versiones** ($S$ y $G$) y clasificación de nuevas instancias.

### 2. Visualizador de Aprendizaje Conceptual (`algoritmos.concept_learning_visualizer`)
- [**`plot_version_space`**](file:///c:/Users/santr/aprendizaje-automatico/aprendizaje-automatico/algoritmos/concept_learning_visualizer.py): Genera diagramas de red/grafo de los límites $S$ y $G$ con NetworkX/Matplotlib.
- [**`print_step_by_step_trace`**](file:///c:/Users/santr/aprendizaje-automatico/aprendizaje-automatico/algoritmos/concept_learning_visualizer.py): Imprime la evolución detallada paso a paso en consola.
- [**`print_ascii_version_space`**](file:///c:/Users/santr/aprendizaje-automatico/aprendizaje-automatico/algoritmos/concept_learning_visualizer.py): Renderiza una retícula en texto ASCII para cualquier entorno.

---

## 💡 Uso Rápido

```python
from algoritmos import (
    FindS,
    CandidateElimination,
    plot_version_space,
    print_step_by_step_trace
)

# 1. Definir dominios y datos
domains = {
    'Dedicacion': ['Alta', 'Media', 'Baja'],
    'Dificultad': ['Alta', 'Media', 'Baja'],
    'Horario': ['Matutino', 'Nocturno'],
    'Humedad': ['Alta', 'Media', 'Baja'],
    'HumorDoc': ['Bueno', 'Malo']
}

X = [
    ['Alta', 'Alta', 'Nocturno', 'Media', 'Bueno'],
    ['Baja', 'Media', 'Matutino', 'Alta', 'Malo'],
    ['Media', 'Alta', 'Nocturno', 'Media', 'Malo'],
    ['Media', 'Alta', 'Matutino', 'Alta', 'Bueno']
]
y = ['SI', 'NO', 'SI', 'NO']

# 2. Entrenar y visualizar Candidate-Elimination
ce = CandidateElimination(domains).fit(X, y)
print_step_by_step_trace(ce)
plot_version_space(ce, save_path="version_space.png")
```
