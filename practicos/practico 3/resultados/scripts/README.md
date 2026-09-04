# Scripts en Python: Práctico 3 (Aprendizaje Bayesiano, Aprendizaje por Casos y Metodología)

Colección de scripts ejecutables para verificar, reproducir cálculos paso a paso y evaluar clasificadores de las resoluciones del **Práctico 3**:

---

## 📋 Lista de Scripts

| Script | Ejercicio Asociado | Descripción |
| :--- | :---: | :--- |
| [**`ejercicio_02_mdl.py`**](./ejercicio_02_mdl.py) | Ejercicio 2 | Simulación de optimización del principio *Minimum Description Length* (MDL) comparando hipótesis consistentes complejas vs. simples con error. |
| [**`ejercicio_03_medios_pago.py`**](./ejercicio_03_medios_pago.py) | Ejercicio 3 | Implementación de 3-NN con normalización euclidiana mixta, Naive Bayes y Árbol ID3 para el dataset de inclusión financiera. |
| [**`ejercicio_04_naive_bayes_knn_spam.py`**](./ejercicio_04_naive_bayes_knn_spam.py) | Ejercicio 4 | Clasificador Naive Bayes para detección de spam, análisis de frecuencias nulas, suavizado de Laplace y clasificación 2-NN con distancia de Hamming. |
| [**`ejercicio_05_paltas_evaluacion.py`**](./ejercicio_05_paltas_evaluacion.py) | Ejercicio 5 | Matriz de confusión, cómputo de Acierto micro/macro, Precisión y Recall, y clasificador Naive Bayes con discretización. |
| [**`ejercicio_06_estudiantes_preprocesamiento_cv.py`**](./ejercicio_06_estudiantes_preprocesamiento_cv.py) | Ejercicio 6 | Pipeline de preprocesamiento, estandarización (evitando data leakage) y 3-fold cross-validation estratificado sobre clasificador mayoritario trivial. |
| [**`ejercicio_07_metricas_multiclase.py`**](./ejercicio_07_metricas_multiclase.py) | Ejercicio 7 | Análisis exhaustivo de matriz de confusión multiclase ($3 \times 3$), cálculo de TP, FP, FN, TN, Precisión, Recall, F1 por clase y Micro/Macro averages bajo desbalance severo. |
| [**`ejercicio_08_intervalos_confianza.py`**](./ejercicio_08_intervalos_confianza.py) | Ejercicio 8 | Estimación de desviación estándar binomial e intervalos de confianza al 95% para la tasa real de error con $N=100$ y $N=1000$. |

---

## 🚀 Ejecución de los Scripts

Para ejecutar cualquiera de los scripts desde la raíz del repositorio:

```bash
# Ejercicio 2
python "practicos/practico 3/resultados/scripts/ejercicio_02_mdl.py"

# Ejercicio 3
python "practicos/practico 3/resultados/scripts/ejercicio_03_medios_pago.py"

# Ejercicio 4
python "practicos/practico 3/resultados/scripts/ejercicio_04_naive_bayes_knn_spam.py"

# Ejercicio 5
python "practicos/practico 3/resultados/scripts/ejercicio_05_paltas_evaluacion.py"

# Ejercicio 6
python "practicos/practico 3/resultados/scripts/ejercicio_06_estudiantes_preprocesamiento_cv.py"

# Ejercicio 7
python "practicos/practico 3/resultados/scripts/ejercicio_07_metricas_multiclase.py"

# Ejercicio 8
python "practicos/practico 3/resultados/scripts/ejercicio_08_intervalos_confianza.py"
```
