# Resoluciones: Práctico 3 (Aprendizaje Bayesiano, Aprendizaje por Casos y Metodología)

En este directorio se encuentran las soluciones detalladas, formalizaciones matemáticas, tablas, diagramas y scripts en Python para cada ejercicio del **Práctico 3**:

---

## 📑 Índice de Ejercicios

* 📄 [**`ejercicio_01.md`**](./ejercicio_01.md): Análisis de hipótesis MAP, Máxima Verosimilitud (ML) y Clasificador Bayesiano Óptimo sobre Find-S y Candidate-Elimination con sesgo a favor de hipótesis generales.
* 📄 [**`ejercicio_02.md`**](./ejercicio_02.md): Principio de Mínima Longitud de Descripción (MDL), formalización $k \log_2(n) + e \log_2(m)$, prevención de sobreajuste frente a consistencia y derivación de distribuciones para equivalencia con MAP.
* 📄 [**`ejercicio_03.md`**](./ejercicio_03.md): Inclusión financiera y medios de pago, tratamiento de variables continuas y faltantes en ID3, Naive Bayes y KNN, inducción de árbol ID3, clasificación 3-NN y predicción bayesiana.
* 📄 [**`ejercicio_04.md`**](./ejercicio_04.md): Detección de correo no deseado (Spam) con Naive Bayes, tratamiento de probabilidades nulas mediante suavizado de Laplace ($m$-estimate) e implementación de 2-NN con distancia de coincidencia.
* 📄 [**`ejercicio_05.md`**](./ejercicio_05.md): Problema de Pedro compra paltas, estrategias para valores faltantes, matriz de confusión de clasificador por umbral de peso, métricas de Acierto micro/macro, Precisión, Recall y Naive Bayes discretizado.
* 📄 [**`ejercicio_06.md`**](./ejercicio_06.md): Dataset de estudiantes y aprobación académica, análisis de imputación y descarte de atributos irrelevantes con alto porcentaje missing (`Estatura`), One-Hot Encoding, estandarización evitando *Data Leakage* y 3-fold Cross Validation estratificado con clasificador mayoritario.
* 📄 [**`ejercicio_07.md`**](./ejercicio_07.md): Metodología de validación cruzada con 5 folds para ajuste de hiperparámetros, muestreo estratificado aleatorio en datasets desbalanceados y ordenados, y análisis exhaustivo de matriz de confusión $3 \times 3$ con métricas por clase y promedios Macro vs Micro.
* 📄 [**`ejercicio_08.md`**](./ejercicio_08.md): Intervalos de confianza al 95% y estimación de la desviación estándar binomial para la tasa real de error con tamaños de muestra $N=100$ y $N=1000$ (análisis del factor $\sqrt{10}$).

---

## 💻 Scripts, Notebooks y Verificación

* 📓 [**`practico_3_laboratorio.ipynb`**](./practico_3_laboratorio.ipynb): **Notebook interactivo de Jupyter** con todos los experimentos, clasificadores, gráficos comparativos de métricas e intervalos de confianza.

En la carpeta [**`scripts/`**](./scripts/) se encuentran las implementaciones en Python para verificar y reproducir los cálculos y modelos:
- 🐍 [**`ejercicio_02_mdl.py`**](./scripts/ejercicio_02_mdl.py)
- 🐍 [**`ejercicio_03_medios_pago.py`**](./scripts/ejercicio_03_medios_pago.py)
- 🐍 [**`ejercicio_04_naive_bayes_knn_spam.py`**](./scripts/ejercicio_04_naive_bayes_knn_spam.py)
- 🐍 [**`ejercicio_05_paltas_evaluacion.py`**](./scripts/ejercicio_05_paltas_evaluacion.py)
- 🐍 [**`ejercicio_06_estudiantes_preprocesamiento_cv.py`**](./scripts/ejercicio_06_estudiantes_preprocesamiento_cv.py)
- 🐍 [**`ejercicio_07_metricas_multiclase.py`**](./scripts/ejercicio_07_metricas_multiclase.py)
- 🐍 [**`ejercicio_08_intervalos_confianza.py`**](./scripts/ejercicio_08_intervalos_confianza.py)

---

## 📄 Enunciados
- 📄 [**`Letra en Markdown (letra/practico_3.md)`**](../letra/practico_3.md)
- 📑 [**`Letra original en PDF (letra/practico_3.pdf)`**](../letra/practico_3.pdf)
