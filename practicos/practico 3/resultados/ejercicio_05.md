# Ejercicio 5: Pedro Compra Paltas - Valores Faltantes, Matriz de Confusión, KNN y Naive Bayes

**Práctico 3: Aprendizaje Bayesiano, Aprendizaje por Casos y Metodología**  
**Curso:** Aprendizaje Automático

---

## Enunciado

Se quiere resolver el siguiente problema de clasificación: «¿Qué días Pedro compra paltas?», y se cuenta con el siguiente conjunto de entrenamiento:

| # | Precio ($/Kg) | Ciudad | Mes | Humor | Calidad | Peso (Kg) | ¿Compra? |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | 100 | Salto | Febrero | Bueno | Buena | 0,300 | **Sí** |
| 2 | 140 | Florida | Marzo | Malo | Media | 0,200 | **No** |
| 3 | 80 | Salto | Marzo | Malo | Buena | 0,500 | **Sí** |
| 4 | 160 | Durazno | Agosto | Bueno | **?** | 0,700 | **Sí** |
| 5 | 200 | Salto | Octubre | Bueno | Buena | 0,100 | **No** |

Donde $\text{Ciudad} \in \{\text{Salto}, \text{Florida}, \text{Durazno}\}$, $\text{Humor} \in \{\text{Bueno}, \text{Malo}\}$, $\text{Calidad} \in \{\text{Buena}, \text{Media}, \text{Mala}\}$, y $\text{Precio}$ y $\text{Peso}$ son atributos numéricos.

- **a)** Dé dos formas de manejar el valor faltante de la instancia 4.
- **b)** Considere un clasificador que responda afirmativamente únicamente a las paltas con peso mayor a 600 gramos y al conjunto de entrenamiento dado:
  - **i.** Dé la matriz de confusión.
  - **ii.** Calcule la estimación del acierto micro y macro.
  - **iii.** Dé la estimación de la precisión y el recall de la clase positiva.
- **c)** ¿Qué modificaciones le realizaría al corpus para aplicar el algoritmo KNN? Justifique.
- **d)** Explique una ventaja y una desventaja de aumentar el valor de $K$ en el algoritmo KNN.
- **e)** Dé el resultado de clasificar a la siguiente instancia según el algoritmo Naïve Bayes, discretizando a los atributos continuos como crea conveniente:

| # | Precio | Ciudad | Mes | Humor | Calidad | Peso | ¿Compra? |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 6 | 110 | Salto | Marzo | Malo | Buena | 0,250 | **?** |

---

## Solución Detallada

### 💻 Código Ejecutable
Se incluye el script en Python para reproducir las métricas de evaluación y los cálculos bayesianos:
* 🐍 [**`scripts/ejercicio_05_paltas_evaluacion.py`**](./scripts/ejercicio_05_paltas_evaluacion.py)

---

### Parte a) Dos Formas de Manejar el Valor Faltante de la Instancia 4

1. **Imputación por Moda (Global o Condicionada por Clase):**
   - *Moda global:* El valor más frecuente de `Calidad` en los datos observados es **Buena** (3 de 4 instancias observadas: #1, #3, #5). Se reemplaza el valor faltante por `Calidad = Buena`.
   - *Moda por clase:* Para la clase `¿Compra? = Sí`, todos los ejemplos conocidos (#1 y #3) tienen `Calidad = Buena`. Por ende, la moda condicionada asigna también `Buena`.

2. **Tratamiento como Categoría Explícita o Imputación Probabilística:**
   - *Categoría «Desconocido»:* Crear un valor categórico adicional `Calidad = Faltante` o `?`, permitiendo que los algoritmos aprendan patrones asociados a la ausencia del dato.
   - *Distribución Fraccional (como en C4.5 / EM):* Distribuir la instancia 4 entre los valores posibles de `Calidad` en proporción a sus frecuencias observadas (ej. peso de $3/4$ para `Buena` y $1/4$ para `Media`).

---

### Parte b) Evaluación del Clasificador por Regla: $h(x) = \text{Sí} \iff \text{Peso} > 0{,}600\text{ Kg}$

Evaluamos cada instancia de entrenamiento:
- **Instancia 1:** Peso = 0,300 $\to$ Predicción = **No**, Real = **Sí** $\implies$ **Falso Negativo (FN)**
- **Instancia 2:** Peso = 0,200 $\to$ Predicción = **No**, Real = **No** $\implies$ **Verdadero Negativo (TN)**
- **Instancia 3:** Peso = 0,500 $\to$ Predicción = **No**, Real = **Sí** $\implies$ **Falso Negativo (FN)**
- **Instancia 4:** Peso = 0,700 $\to$ Predicción = **Sí**, Real = **Sí** $\implies$ **Verdadero Positivo (TP)**
- **Instancia 5:** Peso = 0,100 $\to$ Predicción = **No**, Real = **No** $\implies$ **Verdadero Negativo (TN)**

---

#### i. Matriz de Confusión

| | Predicho **Sí** | Predicho **No** | **Total Real** |
|:---:|:---:|:---:|:---:|
| **Real Sí** | $\text{TP} = 1$ | $\text{FN} = 2$ | $P = 3$ |
| **Real No** | $\text{FP} = 0$ | $\text{TN} = 2$ | $N = 2$ |
| **Total Predicho** | $1$ | $4$ | $\mathbf{5}$ |

---

#### ii. Estimación del Acierto Micro y Macro (Accuracy)

En una tarea de clasificación binaria:
- **Acierto Global / Micro-Accuracy:**
  $$\text{Accuracy}_{\text{micro}} = \frac{\text{TP} + \text{TN}}{\text{TP} + \text{TN} + \text{FP} + \text{FN}} = \frac{1 + 2}{5} = \frac{3}{5} = \mathbf{0{,}60 \quad (60\%)}$$
- **Acierto Macro (Macro-Accuracy):**
  Promedio del acierto por clase individual:
  - Clase Sí: $\text{Acc}_{\text{Sí}} = \frac{1 + 2}{5} = 0{,}60$
  - Clase No: $\text{Acc}_{\text{No}} = \frac{2 + 1}{5} = 0{,}60$
  $$\text{Accuracy}_{\text{macro}} = \frac{0{,}60 + 0{,}60}{2} = \mathbf{0{,}60 \quad (60\%)}$$

---

#### iii. Precisión y Recall de la Clase Positiva («Sí»)

- **Precisión ($\text{Precision}$):**
  $$\text{Precision} = \frac{\text{TP}}{\text{TP} + \text{FP}} = \frac{1}{1 + 0} = \mathbf{1{,}0 \quad (100\%)}$$

- **Sensibilidad / Exhaustividad ($\text{Recall}$):**
  $$\text{Recall} = \frac{\text{TP}}{\text{TP} + \text{FN}} = \frac{1}{1 + 2} = \frac{1}{3} \approx \mathbf{0{,}3333 \quad (33{,}33\%)}$$

- **Medida $F_1$:**
  $$F_1 = 2 \cdot \frac{\text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}} = 2 \cdot \frac{1 \cdot 1/3}{1 + 1/3} = \frac{2/3}{4/3} = \mathbf{0{,}50}$$

---

### Parte c) Modificaciones al Corpus para Aplicar KNN

1. **Normalización de Atributos Continuos:** `Precio` varía en $[80, 200]$ y `Peso` en $[0{,}100, 0{,}700]$. Sin normalizar, la diferencia de precios dominaría completamente la métrica de distancia euclidiana. Se debe aplicar escalado Min-Max:
   $$\text{Precio}' = \frac{\text{Precio} - 80}{200 - 80}, \quad \text{Peso}' = \frac{\text{Peso} - 0{,}100}{0{,}700 - 0{,}100}$$
2. **Codificación de Atributos Categóricos:**
   - *Nominales (`Ciudad`, `Humor`, `Mes`):* Codificación One-Hot (*One-Hot Encoding*) o uso de distancia de coincidencia binaria.
   - *Ordinales (`Calidad`):* Mapeo numérico ordenado ($\text{Mala} = 0$, $\text{Media} = 0{,}5$, $\text{Buena} = 1$).
3. **Imputación del Atributo Faltante:** Completar `Calidad` en la instancia 4 con su moda (`Buena`).

---

### Parte d) Ventaja y Desventaja de Aumentar el Valor de $K$ en KNN

- **Ventaja:**
  - **Mayor Robustez frente al Ruido y Outliers:** Al promediar sobre un vecindario más amplio, se suavizan las fronteras de decisión y se reduce drásticamente la varianza del modelo (*menor sobreajuste*).
- **Desventaja:**
  - **Aumento del Sesgo (Bias) y Sensibilidad al Desbalance de Clases:** Al considerar un $K$ muy grande, se pierden las estructuras locales finas del espacio de características y la clase mayoritaria en el dataset tiende a dominar sistemáticamente las votaciones, perjudicando la clasificación de regiones pequeñas o clases minoritarias.

---

### Parte e) Clasificación de la Instancia #6 con Naive Bayes

Instancia #6:
$$\mathbf{x_6} = \langle \text{Precio}=110, \text{Ciudad}=\text{Salto}, \text{Mes}=\text{Marzo}, \text{Humor}=\text{Malo}, \text{Calidad}=\text{Buena}, \text{Peso}=0{,}250 \rangle$$

#### 1. Esquema de Discretización:
- **Precio:** $\le 120$ (Bajo/Medio: 80, 100, 110) vs $> 120$ (Alto: 140, 160, 200). $\implies \mathbf{x_6} \to \text{Precio} \le 120$.
- **Peso:** $\le 0{,}350$ (Liviano: 0.100, 0.200, 0.250, 0.300) vs $> 0{,}350$ (Pesado: 0.500, 0.700). $\implies \mathbf{x_6} \to \text{Peso} \le 0{,}350$.
- Imputamos en #4: `Calidad = Buena`.

Dataset discretizado:
- Inst 1: $\langle \le 120, \text{Salto}, \text{Feb}, \text{Bueno}, \text{Buena}, \le 0{,}350 \rangle \to \mathbf{\text{Sí}}$
- Inst 2: $\langle > 120, \text{Florida}, \text{Marzo}, \text{Malo}, \text{Media}, \le 0{,}350 \rangle \to \mathbf{\text{No}}$
- Inst 3: $\langle \le 120, \text{Salto}, \text{Marzo}, \text{Malo}, \text{Buena}, > 0{,}350 \rangle \to \mathbf{\text{Sí}}$
- Inst 4: $\langle > 120, \text{Durazno}, \text{Agosto}, \text{Bueno}, \text{Buena}, > 0{,}350 \rangle \to \mathbf{\text{Sí}}$
- Inst 5: $\langle > 120, \text{Salto}, \text{Octubre}, \text{Bueno}, \text{Buena}, \le 0{,}350 \rangle \to \mathbf{\text{No}}$

---

#### 2. Probabilidades a Priori:
$$P(\text{Sí}) = \frac{3}{5} = 0{,}60, \quad P(\text{No}) = \frac{2}{5} = 0{,}40$$

---

#### 3. Probabilidades Condicionales para los Atributos de $\mathbf{x_6}$:

- **Dada la clase $\text{Sí}$ ($N_{\text{Sí}} = 3$, inst. 1, 3, 4):**
  - $P(\text{Precio} \le 120 \mid \text{Sí}) = \frac{2}{3}$ (inst. 1, 3)
  - $P(\text{Ciudad} = \text{Salto} \mid \text{Sí}) = \frac{2}{3}$ (inst. 1, 3)
  - $P(\text{Mes} = \text{Marzo} \mid \text{Sí}) = \frac{1}{3}$ (inst. 3)
  - $P(\text{Humor} = \text{Malo} \mid \text{Sí}) = \frac{1}{3}$ (inst. 3)
  - $P(\text{Calidad} = \text{Buena} \mid \text{Sí}) = \frac{3}{3} = 1{,}0$ (inst. 1, 3, 4)
  - $P(\text{Peso} \le 0{,}350 \mid \text{Sí}) = \frac{1}{3}$ (inst. 1)

  $$\text{Score}(\text{Sí}) = \frac{3}{5} \cdot \left( \frac{2}{3} \cdot \frac{2}{3} \cdot \frac{1}{3} \cdot \frac{1}{3} \cdot 1 \cdot \frac{1}{3} \right) = \frac{3}{5} \cdot \frac{4}{243} = \frac{4}{405} \approx \mathbf{0{,}009877}$$

- **Dada la clase $\text{No}$ ($N_{\text{No}} = 2$, inst. 2, 5):**
  - $P(\text{Precio} \le 120 \mid \text{No}) = \frac{0}{2} = 0$ (ambas instancias tienen Precio $> 120$)
  - $\text{Score}(\text{No}) = \mathbf{0{,}0}$

---

#### 4. Decisión Final:
- Bajo la estimación estándar:
  $$P(\text{Sí} \mid \mathbf{x}_6) = \mathbf{1{,}0 \quad (100\%)}, \quad P(\text{No} \mid \mathbf{x}_6) = 0{,}0$$

*(Con suavizado de Laplace, los scores resultan $\text{Score}_{\text{Lap}}(\text{Sí}) \approx 0{,}0048$ y $\text{Score}_{\text{Lap}}(\text{No}) \approx 0{,}0017 \implies P(\text{Sí} \mid \mathbf{x}_6) \approx 73{,}68\%$).*

> **Resultado:** Naive Bayes clasifica la instancia #6 como **¿Compra? = Sí**.
