# Ejercicio 6: Dataset Estudiantes - Preprocesamiento, Estandarización, Data Leakage y Validación Cruzada

**Práctico 3: Aprendizaje Bayesiano, Aprendizaje por Casos y Metodología**  
**Curso:** Aprendizaje Automático

---

## Enunciado

Considere el siguiente conjunto de datos de estudiantes, y considere el problema de aprender a clasificar cuáles aprobaron el año:

| # | Nombre | Turno | Edad | Nota anterior | Sexo | Estatura | Aprueba |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | Luisa | Vespertino | 16 | 10 | Fem | 1,79 | **Sí** |
| 2 | Ana | Vespertino | 15 | 3 | Masc | 1,65 | **Sí** |
| 3 | Juanjo | Matutino | 14 | 4 | Masc | ? | **No** |
| 4 | Pedro | Vespertino | 16 | 9 | Masc | ? | **Sí** |
| 5 | Ramiro | Vespertino | 15 | 3 | ? | 1,65 | **Sí** |
| 6 | Daniel | Matutino | 15 | 8 | Masc | ? | **No** |
| 7 | Eduardo | ? | 14 | 10 | Masc | ? | **Sí** |
| 8 | Aiala | ? | 15 | 9 | Fem | ? | **Sí** |
| 9 | Dina | Matutino | 15 | 7 | Fem | ? | **No** |
| 10 | Mathias | Vespertino | 14 | 11 | Masc | 1,79 | **Sí** |
| 11 | Diego | Matutino | 15 | 5 | Masc | ? | **Sí** |
| 12 | Santiago | Vespertino | 15 | 6 | Masc | 1,67 | **Sí** |
| 13 | Luis | Matutino | 15 | 6 | Masc | 1,72 | **No** |
| 14 | Alejandra | Vespertino | 16 | 6 | Fem | 1,73 | **Sí** |

- **a)** ¿Cómo completaría los atributos faltantes para cada uno de los atributos?
- **b)** ¿Qué sugeriría hacer con el atributo estatura?
- **c)** ¿Cuál sería el resultado de transformar el atributo «Turno» utilizando one-hot-encoding?
- **d)** Divida el conjunto de datos en entrenamiento y evaluación, utilizando estratificación.
- **e)** Estandarice los valores de edad y nota. Aplique la estandarización al conjunto de evaluación. ¿Es lo mismo esto que aplicar la estandarización a todo el dataset?
- **f)** Suponga un clasificador trivial que predice la clase mayoritaria en el conjunto de entrenamiento. Suponga ahora que nuestra tabla es el conjunto total de entrenamiento, y realice 3-fold cross validation. Reporte precisión, recall, medida F, así como la desviación estándar de cada una de ellas.

---

## Solución Detallada

### 💻 Código Ejecutable
Se incluye el script en Python para reproducir el preprocesamiento y la simulación de validación cruzada:
* 🐍 [**`scripts/ejercicio_06_estudiantes_preprocesamiento_cv.py`**](./scripts/ejercicio_06_estudiantes_preprocesamiento_cv.py)

---

### Parte a) Completitud de Atributos Faltantes

Analizamos la estrategia óptima para cada columna con valores ausentes:

1. **`Nombre`:** Es un identificador único (clave primaria nominal). No tiene valores faltantes, pero debe **eliminarse** de las variables predictoras para evitar memorización espuria.
2. **`Turno` (faltante en #7 y #8):** Atributo categórico. En los 12 datos conocidos: `Vespertino` = 7, `Matutino` = 5. La **moda** es `Vespertino`. Por lo tanto, se imputa `Turno = Vespertino`. Alternativamente, se puede imputar por correlación con otras variables o crear una categoría `Desconocido`.
3. **`Sexo` (faltante en #5 «Ramiro»):** 
   - *Por conocimiento de dominio / Nombre:* «Ramiro» es un nombre típicamente masculino $\implies \text{Sexo} = \text{Masc}$.
   - *Por criterio estadístico:* La moda global observada es `Masc` (9 Masc vs 4 Fem). Imputación: `Masc`.
4. **`Estatura` (faltante en 7 de 14 instancias: #3, #4, #6, #7, #8, #9, #11):** Si se decidiera imputar (ver parte b), se calcularía la media o mediana de los valores observados por sexo ($\bar{x}_{\text{Fem}} \approx 1{,}72\text{m}$, $\bar{x}_{\text{Masc}} \approx 1{,}69\text{m}$).

---

### Parte b) Recomendación sobre el Atributo «Estatura»

> **Recomendación:** **Eliminar por completo el atributo `Estatura` del dataset.**

#### Justificación:
1. **Severa tasa de valores ausentes ($50\%$):** La mitad exacta del dataset carece de este valor. Imputar la mitad de las observaciones introduce un volumen inaceptable de ruido artificial.
2. **Nula relevancia conceptual / Causalidad nula:** En el dominio de la educación y el rendimiento académico, la estatura física de un estudiante carece de fundamento teórico o correlación real con la aprobación del año. Conservarla solo aportaría ruido y riesgo de sobreajuste (*curse of dimensionality*).

---

### Parte c) Transformación de «Turno» con One-Hot Encoding

El atributo `Turno` posee dos categorías posibles en los datos: $\{\text{Matutino}, \text{Vespertino}\}$ (y eventualmente $\text{Desconocido}$ si no se imputa).

Al aplicar **One-Hot Encoding** (con imputación previa):
Se generan dos variables binarias indicadoras ($0$ ó $1$):

| # | Turno Original | Turno_Matutino | Turno_Vespertino |
|:---:|:---:|:---:|:---:|
| 1 | Vespertino | 0 | 1 |
| 2 | Vespertino | 0 | 1 |
| 3 | Matutino | 1 | 0 |
| ... | ... | ... | ... |
| 7 | *(Imputado Vesp)* | 0 | 1 |

*(Nota: En modelos lineales, para evitar la colinealidad exacta o «dummy variable trap», se descarta una de las columnas quedando una única variable binaria `Turno_Vespertino` $\in \{0, 1\}$).*

---

### Parte d) División del Dataset en Entrenamiento y Evaluación con Estratificación

#### 1. Distribución Original de la Variable Objetivo (`Aprueba`):
- Total de instancias: $N = 14$.
- **Sí:** 10 instancias ($71{,}43\%$) $\to$ {#1, #2, #4, #5, #7, #8, #10, #11, #12, #14}.
- **No:** 4 instancias ($28{,}57\%$) $\to$ {#3, #6, #9, #13}.

#### 2. Partición Estratificada (ejemplo ratio 70% Train / 30% Test):
Para mantener rigurosamente la proporción $71{,}4\% / 28{,}6\%$:
- **Conjunto de Entrenamiento ($N_{\text{train}} = 10$, $71{,}4\%$ del total):**
  - **7 instancias Sí** (ej. {#1, #2, #4, #5, #7, #8, #10})
  - **3 instancias No** (ej. {#3, #6, #9})
  - Proporción Train: $70\%$ Sí / $30\%$ No.
- **Conjunto de Evaluación / Test ($N_{\text{test}} = 4$, $28{,}6\%$ del total):**
  - **3 instancias Sí** (ej. {#11, #12, #14})
  - **1 instancia No** (ej. {#13})
  - Proporción Test: $75\%$ Sí / $25\%$ No.

---

### Parte e) Estandarización y Prevención de *Data Leakage*

La **estandarización (Z-score)** transforma una variable $X$ mediante:
$$z = \frac{x - \mu}{\sigma}$$

#### 1. Procedimiento Correcto:
1. Se calculan la media $\mu_{\text{train}}$ y la desviación estándar $\sigma_{\text{train}}$ **únicamente utilizando las instancias del conjunto de entrenamiento**.
2. Se estandariza el conjunto de entrenamiento usando $(\mu_{\text{train}}, \sigma_{\text{train}})$.
3. Se transforman las instancias del **conjunto de evaluación** utilizando los parámetros aprendidos del entrenamiento:
   $$z_{\text{test}} = \frac{x_{\text{test}} - \mu_{\text{train}}}{\sigma_{\text{train}}}$$

#### 2. ¿Es lo mismo que estandarizar todo el dataset junto?

> **NO, en absoluto.**

- Si se estandariza todo el conjunto de datos antes de hacer la partición, la media y varianza globales incorporan información del conjunto de evaluación.
- Esto constituye un fenómeno de **Fuga de Información (*Data Leakage*)**, que vicia la independencia estadística de la prueba y genera estimaciones artificialmente optimistas e irreales sobre la verdadera capacidad de generalización del modelo.

---

### Parte f) 3-Fold Cross Validation con Clasificador Mayoritario Trivial

Configuración de la Validación Cruzada con 14 instancias estratificadas en 3 folds (tamaños 5, 5, 4):

- **Fold 1 ($n=5$):** 3 Sí, 2 No.
- **Fold 2 ($n=5$):** 3 Sí, 2 No.
- **Fold 3 ($n=4$):** 4 Sí, 0 No.

#### Comportamiento del Clasificador Mayoritario:
En cada iteración $k$, el conjunto de entrenamiento contiene la gran mayoría de instancias pertenecientes a la clase **«Sí»** (7 Sí vs 2 No en folds 1 y 2; 6 Sí vs 4 No en fold 3).
Por lo tanto, el modelo trivial **siempre predice «Sí» para todas las instancias de prueba**.

---

#### Evaluación Fold por Fold:

1. **Fold 1 (Test: 3 Sí, 2 No):**
   - Predicciones: 5 Sí $\implies \text{TP} = 3$, $\text{FP} = 2$, $\text{FN} = 0$, $\text{TN} = 0$.
   - $\text{Precision}_1 = \frac{3}{3 + 2} = \mathbf{0{,}6000}$
   - $\text{Recall}_1 = \frac{3}{3 + 0} = \mathbf{1{,}0000}$
   - $F_{1,1} = 2 \cdot \frac{0{,}60 \cdot 1}{0{,}60 + 1} = \frac{1{,}2}{1{,}6} = \mathbf{0{,}7500}$

2. **Fold 2 (Test: 3 Sí, 2 No):**
   - Predicciones: 5 Sí $\implies \text{TP} = 3$, $\text{FP} = 2$, $\text{FN} = 0$, $\text{TN} = 0$.
   - $\text{Precision}_2 = \mathbf{0{,}6000}$
   - $\text{Recall}_2 = \mathbf{1{,}0000}$
   - $F_{1,2} = \mathbf{0{,}7500}$

3. **Fold 3 (Test: 4 Sí, 0 No):**
   - Predicciones: 4 Sí $\implies \text{TP} = 4$, $\text{FP} = 0$, $\text{FN} = 0$, $\text{TN} = 0$.
   - $\text{Precision}_3 = \frac{4}{4 + 0} = \mathbf{1{,}0000}$
   - $\text{Recall}_3 = \frac{4}{4 + 0} = \mathbf{1{,}0000}$
   - $F_{1,3} = \mathbf{1{,}0000}$

---

#### Métricas Globales (Promedio y Desviación Estándar Muestral con $N=3$):

- **Precisión:**
  $$\bar{P} = \frac{0{,}6000 + 0{,}6000 + 1{,}0000}{3} = \mathbf{0{,}7333 \quad (73{,}33\%)}$$
  $$s_P = \sqrt{\frac{(0{,}60 - 0{,}7333)^2 \cdot 2 + (1{,}00 - 0{,}7333)^2}{3 - 1}} = \mathbf{0{,}2309}$$

- **Recall:**
  $$\bar{R} = \frac{1{,}0000 + 1{,}0000 + 1{,}0000}{3} = \mathbf{1{,}0000 \quad (100\%)}$$
  $$s_R = \mathbf{0{,}0000}$$

- **Medida $F_1$:**
  $$\bar{F}_1 = \frac{0{,}7500 + 0{,}7500 + 1{,}0000}{3} = \mathbf{0{,}8333}$$
  $$s_{F_1} = \sqrt{\frac{(0{,}75 - 0{,}8333)^2 \cdot 2 + (1{,}00 - 0{,}8333)^2}{2}} = \mathbf{0{,}1443}$$

| Métrica | Promedio ($\mu$) | Desviación Estándar ($s$) | Reporte Final ($\mu \pm s$) |
| :--- | :---: | :---: | :---: |
| **Precisión** | $0{,}7333$ | $0{,}2309$ | $\mathbf{0{,}7333 \pm 0{,}2309}$ |
| **Recall** | $1{,}0000$ | $0{,}0000$ | $\mathbf{1{,}0000 \pm 0{,}0000}$ |
| **Medida $F_1$** | $0{,}8333$ | $0{,}1443$ | $\mathbf{0{,}8333 \pm 0{,}1443}$ |
