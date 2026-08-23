# Ejercicio 2: Cálculo de Entropía y Ganancia de Información

**Práctico 2: Árboles de Decisión**  
**Curso:** Aprendizaje Automático

---

## Enunciado

Dado el siguiente conjunto de entrenamiento:

| # | $a_1$ | $a_2$ | Clasif |
|:---:|:---:|:---:|:---:|
| 1 | Verdadero ($V$) | Verdadero ($V$) | Sí ($+$) |
| 2 | Verdadero ($V$) | Verdadero ($V$) | Sí ($+$) |
| 3 | Verdadero ($V$) | Falso ($F$) | No ($-$) |
| 4 | Falso ($F$) | Falso ($F$) | Sí ($+$) |
| 5 | Falso ($F$) | Verdadero ($V$) | No ($-$) |
| 6 | Falso ($F$) | Verdadero ($V$) | No ($-$) |

- **a)** ¿Cuál es la entropía del conjunto de entrenamiento?
- **b)** ¿Cuál es la ganancia de particionar por cada uno de los atributos?

---

## Solución Detallada

### 💻 Código Ejecutable
Se incluye el script en Python para reproducir y verificar numéricamente todos los cálculos:
* 🐍 [**`scripts/ejercicio_02_entropia_ganancia.py`**](./scripts/ejercicio_02_entropia_ganancia.py)

---

### Parte a) Entropía del Conjunto de Entrenamiento $H(S)$

El conjunto $S$ contiene un total de $|S| = 6$ ejemplos:
- Ejemplos positivos ($+$): $3$ (instancias 1, 2, 4) $\implies p_+ = \frac{3}{6} = \frac{1}{2}$
- Ejemplos negativos ($-$) : $3$ (instancias 3, 5, 6) $\implies p_- = \frac{3}{6} = \frac{1}{2}$

Aplicando la fórmula de la **Entropía de Shannon**:

$$\text{Entropía}(S) = - p_+ \log_2(p_+) - p_- \log_2(p_-)$$

$$\text{Entropía}(S) = - \left(\frac{1}{2}\right) \log_2\left(\frac{1}{2}\right) - \left(\frac{1}{2}\right) \log_2\left(\frac{1}{2}\right)$$
$$\text{Entropía}(S) = - \left(\frac{1}{2}\right)(-1) - \left(\frac{1}{2}\right)(-1) = \frac{1}{2} + \frac{1}{2} = \mathbf{1{,}0 \text{ bit}}$$

> [!NOTE]
> Al haber exactamente la misma cantidad de ejemplos positivos y negativos ($50\% / 50\%$), la incertidumbre es máxima y la entropía vale exactamente $1{,}0$ bit.

---

### Parte b) Ganancia de Información al Particionar por $a_1$ y $a_2$

La ganancia de información se define como:

$$\text{Ganancia}(S, A) = \text{Entropía}(S) - \sum_{v \in \text{Val}(A)} \frac{|S_v|}{|S|} \text{Entropía}(S_v)$$

---

#### 1. Evaluación para el Atributo $a_1$:

El atributo $a_1$ toma dos valores posibles: $\{V, F\}$.

- **Rama $a_1 = V$** (instancias 1, 2, 3):
  - Total: $|S_{a_1=V}| = 3$ ejemplos ($2$ Sí, $1$ No).
  - $p_+ = \frac{2}{3}, \quad p_- = \frac{1}{3}$
  - $\text{Entropía}(S_{a_1=V}) = -\frac{2}{3} \log_2\left(\frac{2}{3}\right) - \frac{1}{3} \log_2\left(\frac{1}{3}\right) \approx 0{,}9183 \text{ bits}$

- **Rama $a_1 = F$** (instancias 4, 5, 6):
  - Total: $|S_{a_1=F}| = 3$ ejemplos ($1$ Sí, $2$ No).
  - $p_+ = \frac{1}{3}, \quad p_- = \frac{2}{3}$
  - $\text{Entropía}(S_{a_1=F}) = -\frac{1}{3} \log_2\left(\frac{1}{3}\right) - \frac{2}{3} \log_2\left(\frac{2}{3}\right) \approx 0{,}9183 \text{ bits}$

**Entropía residual ponderada:**
$$\sum_{v \in \{V, F\}} \frac{|S_v|}{|S|} \text{Entropía}(S_v) = \frac{3}{6}(0{,}9183) + \frac{3}{6}(0{,}9183) = 0{,}9183 \text{ bits}$$

**Ganancia de Información:**
$$\text{Ganancia}(S, a_1) = 1{,}0 - 0{,}9183 = \mathbf{0{,}0817 \text{ bits}}$$

---

#### 2. Evaluación para el Atributo $a_2$:

El atributo $a_2$ toma dos valores posibles: $\{V, F\}$.

- **Rama $a_2 = V$** (instancias 1, 2, 5, 6):
  - Total: $|S_{a_2=V}| = 4$ ejemplos ($2$ Sí, $2$ No).
  - $p_+ = \frac{2}{4} = \frac{1}{2}, \quad p_- = \frac{2}{4} = \frac{1}{2}$
  - $\text{Entropía}(S_{a_2=V}) = - \frac{1}{2}\log_2\left(\frac{1}{2}\right) - \frac{1}{2}\log_2\left(\frac{1}{2}\right) = 1{,}0 \text{ bit}$

- **Rama $a_2 = F$** (instancias 3, 4):
  - Total: $|S_{a_2=F}| = 2$ ejemplos ($1$ Sí, $1$ No).
  - $p_+ = \frac{1}{2}, \quad p_- = \frac{1}{2}$
  - $\text{Entropía}(S_{a_2=F}) = 1{,}0 \text{ bit}$

**Entropía residual ponderada:**
$$\sum_{v \in \{V, F\}} \frac{|S_v|}{|S|} \text{Entropía}(S_v) = \frac{4}{6}(1{,}0) + \frac{2}{6}(1{,}0) = 1{,}0 \text{ bit}$$

**Ganancia de Información:**
$$\text{Ganancia}(S, a_2) = 1{,}0 - 1{,}0 = \mathbf{0{,}0000 \text{ bits}}$$

---

### 📊 Resumen Comparativo

| Atributo | Entropía Residual | Ganancia de Información | Decisión ID3 |
|:---:|:---:|:---:|:---:|
| **$a_1$** | $0{,}9183$ | **$0{,}0817$ bits** | ⭐ **Elegido como Raíz** |
| **$a_2$** | $1{,}0000$ | **$0{,}0000$ bits** | Descartado en este paso |

> [!TIP]
> Dado que $\text{Ganancia}(S, a_1) > \text{Ganancia}(S, a_2)$, el algoritmo ID3 elige a **$a_1$** como el nodo raíz del árbol de decisión.
