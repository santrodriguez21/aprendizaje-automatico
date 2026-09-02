# Contenidos Teóricos

Material conceptual, notas, diapositivas y ejemplos organizados por cada clase:

* 📖 [**`GLOSARIO.md`**](./GLOSARIO.md): **Glosario de Términos y Notación Formal** (organizado por temática: Fundamentos, Concept Learning, Árboles de Decisión, Bayes, Sesgos, Métricas Estadísticas, Metodología/Preprocesamiento y Aprendizaje Basado en Casos/Instancias).

---


### 📂 [Clase 1: ¿Qué es Aprender y Tipos de Aprendizaje?](./clase%201%20-%20tipos%20de%20aprendizaje/)
- 📄 [**`01-que-es-aprender-y-tipos-de-aprendizaje.md`**](./clase%201%20-%20tipos%20de%20aprendizaje/01-que-es-aprender-y-tipos-de-aprendizaje.md): Resumen conceptual, formalismo $(T, P, E)$ de Tom Mitchell y paradigmas (Supervisado, No Supervisado, Refuerzo).
- 📑 [**`1 - que es aprender y tipos de aprendizaje.pdf`**](./clase%201%20-%20tipos%20de%20aprendizaje/1%20-%20que%20es%20aprender%20y%20tipos%20de%20aprendizaje.pdf): Diapositivas originales de la clase.

---

### 📂 [Clase 2: Aprendizaje Conceptual, Find-S y Candidate Elimination](./clase%202%20-%20concept_learning/)
- 📄 [**`02-algoritmos-find-s-y-candidate-elimination.md`**](./clase%202%20-%20concept_learning/02-algoritmos-find-s-y-candidate-elimination.md): Teoría completa, formulación matemática, pseudocódigo y traza paso a paso.
- 📑 [**`2 - Algoritmos Find-S y Candidate Elimination.pdf`**](./clase%202%20-%20concept_learning/2%20-%20Algoritmos%20Find-S%20y%20Candidate%20Elimination.pdf): Diapositivas originales de la clase.
- 🧪 **Ejemplos prácticos e interactivos** ([`clase 2 - concept_learning/ejemplos/`](./clase%202%20-%20concept_learning/ejemplos/)):
  - 📓 [**`02_find_s_y_candidate_elimination.ipynb`**](./clase%202%20-%20concept_learning/ejemplos/02_find_s_y_candidate_elimination.ipynb): Notebook interactivo paso a paso con tablas de evolución y gráficos de retículas.
  - 🐍 [**`demo_interactiva.py`**](./clase%202%20-%20concept_learning/ejemplos/demo_interactiva.py): Script de consola para ejecutar y visualizar los algoritmos con el caso de Pedro.
  - 📊 Visualización provista por [**`algoritmos.concept_learning_visualizer`**](../../algoritmos/concept_learning_visualizer.py).

---

### 📂 [Clase 3: Árboles de Decisión y Algoritmo ID3](./clase%203%20-%20decision_trees/)
- 📄 [**`03-arboles-de-decision-e-id3.md`**](./clase%203%20-%20decision_trees/03-arboles-de-decision-e-id3.md): Representación de árboles (DNF), algoritmo ID3, entropía de Shannon, ganancia de información, sesgo inductivo (preferencial vs. restrictivo), navaja de Ockham y referencias académicas.
- 📑 [**`3_arboles_de_decision.pdf`**](./clase%203%20-%20decision_trees/3_arboles_de_decision.pdf): Diapositivas originales de la clase.
- 🧪 **Ejemplos prácticos e interactivos** ([`clase 3 - decision_trees/ejemplos/`](./clase%203%20-%20decision_trees/ejemplos/)):
  - 📓 [**`03_arboles_de_decision_e_id3.ipynb`**](./clase%203%20-%20decision_trees/ejemplos/03_arboles_de_decision_e_id3.ipynb): Notebook interactivo paso a paso con cálculo de entropía, ganancia, poda, atributos continuos y reglas DNF.
  - 🐍 [**`demo_id3.py`**](./clase%203%20-%20decision_trees/ejemplos/demo_id3.py): Script de consola para ejecutar y visualizar el árbol ID3 en formato ASCII.
  - 📊 Visualización provista por [**`algoritmos.decision_tree_visualizer`**](../../algoritmos/decision_tree_visualizer.py).

---

### 📂 [Clase 4: Aprendizaje Bayesiano](./clase%204%20-%20aprendizaje%20bayesiano/)
- 📄 [**`04-aprendizaje-bayesiano.md`**](./clase%204%20-%20aprendizaje%20bayesiano/04-aprendizaje-bayesiano.md): Teorema de Bayes, hipótesis MAP y ML, Clasificador Bayesiano Óptimo, Naive Bayes, $m$-estimador, clasificación de texto y log-probabilidades.
- 📑 [**`4_bayes.pdf`**](./clase%204%20-%20aprendizaje%20bayesiano/4_bayes.pdf): Diapositivas originales de la clase.
- 🧪 **Ejemplos prácticos e interactivos** ([`clase 4 - aprendizaje bayesiano/ejemplos/`](./clase%204%20-%20aprendizaje%20bayesiano/ejemplos/)):
  - 📓 [**`04_aprendizaje_bayesiano_y_naive_bayes.ipynb`**](./clase%204%20-%20aprendizaje%20bayesiano/ejemplos/04_aprendizaje_bayesiano_y_naive_bayes.ipynb): Notebook interactivo paso a paso con Naive Bayes, $m$-estimador, Laplace, trazas y Clasificador Bayesiano Óptimo.
  - 🐍 [**`demo_bayes.py`**](./clase%204%20-%20aprendizaje%20bayesiano/ejemplos/demo_bayes.py): Script de consola para ejecutar inferencia bayesiana y trazas explicativas.
  - 📊 Visualización provista por [**`algoritmos.bayesian_visualizer`**](../../algoritmos/bayesian_visualizer.py).

---

### 📂 [Clase 5: Metodologías para Clasificación y Evaluación](./clase%205%20-%20metodolog%C3%ADas/)
- 📄 [**`05-metodologia-para-clasificacion.md`**](./clase%205%20-%20metodolog%C3%ADas/05-metodologia-para-clasificacion.md): Metodología de 4 fases (Preprocesamiento, Partición, Entrenamiento y Evaluación), manejo de faltantes, One-Hot, TF-IDF, estandarización/normalización, estratificación, SMOTE, NearMiss, selección de atributos (Filter, Wrapper, Embedded), validación cruzada $k$-fold, GridSearchCV, Pipelines y ColumnTransformer, matrices de confusión binarias y multiclase, teoría estadística de Tom Mitchell (intervalos de confianza al 95%), Precision, Recall, $F_1$, Macro/Micro average, curvas PR, índice de Jaccard multietiqueta y baselines.
- 📑 [**`5_metodologia.pdf`**](./clase%205%20-%20metodolog%C3%ADas/5_metodologia.pdf): Diapositivas originales de la clase.
- 🧪 **Código y Pipelines** ([`clase 5 - metodologías/`](./clase%205%20-%20metodolog%C3%ADas/)):
  - 📓 [**`demo_pipeline.ipynb`**](./clase%205%20-%20metodolog%C3%ADas/demo_pipeline.ipynb): Notebook práctico con Pipeline, ColumnTransformer, SimpleImputer, OneHotEncoder, StratifiedKFold y GridSearchCV.

---

### 📂 [Clase 6: Aprendizaje Basado en Casos e Instancias](./clase%206%20-%20aprendizaje%20basado%20en%20casos/)
- 📄 [**`06-aprendizaje-basado-en-casos.md`**](./clase%206%20-%20aprendizaje%20basado%20en%20casos/06-aprendizaje-basado-en-casos.md): Aprendizaje perezoso (*Lazy*) vs. ansioso (*Eager*), clasificador $k$-Nearest Neighbor ($k$-NN), distancia euclidiana, voto discreto y regresión, $k$-NN ponderado por distancia (Método de Shepard), selección de $k$ y LOOCV, la Maldición de la Dimensionalidad (ponderación y selección de ejes), estandarización/escalamiento, indexación espacial ($k\text{-d trees}$, Ball Trees), sesgo inductivo, Regresión Local Ponderada (RLP/LWR) con funciones núcleo (*kernel*) decrecientes, y Razonamiento Basado en Casos (CBR) con el ciclo de las 4R (*Retrieve, Reuse, Revise, Retain*).
- 📑 [**`6_casos.pdf`**](./clase%206%20-%20aprendizaje%20basado%20en%20casos/6_casos.pdf): Diapositivas originales de la clase.


