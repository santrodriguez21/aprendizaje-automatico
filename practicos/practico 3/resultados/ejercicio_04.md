# Ejercicio 4: Filtro de Correo No Deseado (Spam) - Naive Bayes, Laplace y 2-NN

**Práctico 3: Aprendizaje Bayesiano, Aprendizaje por Casos y Metodología**  
**Curso:** Aprendizaje Automático

---

## Enunciado

Suponga que quiere implementar un detector de correo no deseado y cuenta con el siguiente conjunto de entrenamiento:

| # | Agendado | Idioma | Para | Venta | Deseado |
|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | Sí | Inglés | Sí | Sí | **Sí** |
| 2 | No | Otro | No | No | **Sí** |
| 3 | No | Español | No | Sí | **Sí** |
| 4 | Sí | Otro | Sí | No | **No** |
| 5 | No | Español | Sí | Sí | **No** |

Considere al ejemplo:

| # | Agendado | Idioma | Para | 'Venta' | Deseado |
|:---:|:---:|:---:|:---:|:---:|:---:|
| 6 | Sí | Inglés | No | Sí | **??** |

- **a)** ¿Cómo clasificaría un clasificador bayesiano sencillo al correo #6? ¿Con qué probabilidad?
- **b)** ¿Qué modificación debería hacer en la parte anterior, si le informan que el atributo «Idioma» puede tomar el valor «francés»?
- **c)** ¿Cómo implementaría un 2-NN? Ejemplifique su solución clasificando a #6.

---

## Solución Detallada

### 💻 Código Ejecutable
Se incluye el script en Python para verificar todos los cálculos de probabilidades y distancias:
* 🐍 [**`scripts/ejercicio_04_naive_bayes_knn_spam.py`**](./scripts/ejercicio_04_naive_bayes_knn_spam.py)

---

### Parte a) Clasificación con Clasificador Bayesiano Sencillo (Naive Bayes)

El clasificador **Naive Bayes** asigna la clase $v_{\text{NB}}$ que maximiza el producto de la probabilidad a priori por las probabilidades condicionales de cada atributo dada la clase:

$$v_{\text{NB}} = \arg\max_{v_j \in \{\text{Sí}, \text{No}\}} P(v_j) \prod_{i=1}^4 P(a_i = v_i \mid v_j)$$

Donde la instancia #6 tiene los atributos:
$$\mathbf{x_6} = \langle \text{Agendado}=\text{Sí}, \text{Idioma}=\text{Inglés}, \text{Para}=\text{No}, \text{Venta}=\text{Sí} \rangle$$

#### 1. Probabilidades a Priori $P(\text{Deseado})$:
- Total de ejemplos: $N = 5$.
- Deseados = Sí: $\{1, 2, 3\} \implies P(\text{Sí}) = \frac{3}{5} = 0{,}60$.
- Deseados = No: $\{4, 5\} \implies P(\text{No}) = \frac{2}{5} = 0{,}40$.

---

#### 2. Probabilidades Condicionales $P(a_i \mid \text{Deseado})$:

- **Para la clase $\text{Deseado} = \text{Sí}$ ($N_{\text{Sí}} = 3$ ejemplos: #1, #2, #3):**
  - $P(\text{Agendado}=\text{Sí} \mid \text{Sí}) = \frac{1}{3}$ (ejemplo #1)
  - $P(\text{Idioma}=\text{Inglés} \mid \text{Sí}) = \frac{1}{3}$ (ejemplo #1)
  - $P(\text{Para}=\text{No} \mid \text{Sí}) = \frac{2}{3}$ (ejemplos #2, #3)
  - $P(\text{Venta}=\text{Sí} \mid \text{Sí}) = \frac{2}{3}$ (ejemplos #1, #3)

- **Para la clase $\text{Deseado} = \text{No}$ ($N_{\text{No}} = 2$ ejemplos: #4, #5):**
  - $P(\text{Agendado}=\text{Sí} \mid \text{No}) = \frac{1}{2}$ (ejemplo #4)
  - $P(\text{Idioma}=\text{Inglés} \mid \text{No}) = \frac{0}{2} = 0$ (ninguno)
  - $P(\text{Para}=\text{No} \mid \text{No}) = \frac{0}{2} = 0$ (ninguno)
  - $P(\text{Venta}=\text{Sí} \mid \text{No}) = \frac{1}{2}$ (ejemplo #5)

---

#### 3. Cálculo de Scores no Normalizados:

$$\text{Score}(\text{Sí}) = P(\text{Sí}) \cdot P(\text{Ag}=\text{Sí}|\text{Sí}) \cdot P(\text{Id}=\text{Ing}|\text{Sí}) \cdot P(\text{Pa}=\text{No}|\text{Sí}) \cdot P(\text{Ve}=\text{Sí}|\text{Sí})$$
$$\text{Score}(\text{Sí}) = \frac{3}{5} \cdot \frac{1}{3} \cdot \frac{1}{3} \cdot \frac{2}{3} \cdot \frac{2}{3} = \frac{4}{135} \approx \mathbf{0{,}02963}$$

$$\text{Score}(\text{No}) = P(\text{No}) \cdot P(\text{Ag}=\text{Sí}|\text{No}) \cdot P(\text{Id}=\text{Ing}|\text{No}) \cdot P(\text{Pa}=\text{No}|\text{No}) \cdot P(\text{Ve}=\text{Sí}|\text{No})$$
$$\text{Score}(\text{No}) = \frac{2}{5} \cdot \frac{1}{2} \cdot 0 \cdot 0 \cdot \frac{1}{2} = \mathbf{0{,}0}$$

---

#### 4. Normalización y Probabilidad Final:
$$P(\text{Sí} \mid \mathbf{x_6}) = \frac{\text{Score}(\text{Sí})}{\text{Score}(\text{Sí}) + \text{Score}(\text{No})} = \frac{4/135}{4/135 + 0} = \mathbf{1{,}0 \quad (100\%)}$$
$$P(\text{No} \mid \mathbf{x_6}) = \mathbf{0{,}0 \quad (0\%)}$$

> **Conclusión:** El clasificador clasifica al correo #6 como **Deseado = Sí** con probabilidad **$1{,}0$ ($100\%$)**.

---

### Parte b) Modificación ante la Incorporación de un Nuevo Valor («Francés»)

Si el atributo «Idioma» puede tomar el valor «francés» y aparece en una instancia a clasificar, la estimación frecuentista estándar daría $P(\text{francés} \mid \text{Sí}) = 0$ y $P(\text{francés} \mid \text{No}) = 0$, anulando todos los productos y arrojando una indeterminación $0/0$.

Para solucionar esto, se debe incorporar una técnica de suavizado de probabilidades como la **$m$-estimate** o la **Corrección de Laplace (Suavizado Aditivo)**:

$$\hat{P}(a_i = v_k \mid c) = \frac{n_k + m \cdot p}{n + m}$$

Donde:
- $n$: número de ejemplos de entrenamiento de la clase $c$.
- $n_k$: número de ejemplos de la clase $c$ que tienen el valor $v_k$.
- $p$: probabilidad a priori del valor (típicamente uniforme $p = 1/k$, siendo $k$ la cantidad de valores posibles del atributo).
- $m$: parámetro de peso equivalente de la muestra (haciendo $m = k$, obtenemos el suavizado de Laplace: $\frac{n_k + 1}{n + |V_{\text{Idioma}}|}$).

Al saber que «Idioma» toma valores en $\{\text{Inglés}, \text{Español}, \text{Otro}, \text{Francés}\}$ ($|V| = 4$), el denominador se ajusta a $n + 4$, garantizando que ningún término condicional sea estrictamente cero.

---

### Parte c) Implementación de 2-NN y Clasificación de #6

Para aplicar el algoritmo **2-NN** sobre variables categóricas / binarias:

1. **Función de Distancia (Distancia de Hamming / Coincidencia Simple):**
   Contamos la cantidad de atributos en los que dos instancias difieren:
   $$d(\mathbf{x}, \mathbf{y}) = \sum_{i=1}^4 \mathbb{I}(x_i \ne y_i)$$

2. **Cálculo de Distancias desde la Instancia #6 ($\langle \text{Sí}, \text{Inglés}, \text{No}, \text{Sí} \rangle$):**

| # | Instancia de Entrenamiento | Diferencias con #6 | Distancia $d(\mathbf{x}_6, \mathbf{x}_i)$ | Clase Real |
|:---:|:---|:---|:---:|:---:|
| **1** | $\langle \text{Sí}, \text{Inglés}, \text{Sí}, \text{Sí} \rangle$ | `Para` ($\text{Sí} \ne \text{No}$) | **1** | **Sí** |
| **2** | $\langle \text{No}, \text{Otro}, \text{No}, \text{No} \rangle$ | `Agendado`, `Idioma`, `Venta` | **3** | **Sí** |
| **3** | $\langle \text{No}, \text{Español}, \text{No}, \text{Sí} \rangle$ | `Agendado`, `Idioma` | **2** | **Sí** |
| **4** | $\langle \text{Sí}, \text{Otro}, \text{Sí}, \text{No} \rangle$ | `Idioma`, `Para`, `Venta` | **3** | **No** |
| **5** | $\langle \text{No}, \text{Español}, \text{Sí}, \text{Sí} \rangle$ | `Agendado`, `Idioma`, `Para` | **3** | **No** |

3. **Selección de los 2 Vecinos Más Cercanos ($K=2$):**
   - 1er vecino: **Instancia #1** ($d = 1$, Clase = **Sí**)
   - 2do vecino: **Instancia #3** ($d = 2$, Clase = **Sí**)

4. **Regla de Votación:**
   Ambos vecinos más cercanos pertenecen a la clase **Sí** (2 votos contra 0).

> **Resultado 2-NN:** Clasifica al correo #6 unánimemente como **Deseado = Sí**.
