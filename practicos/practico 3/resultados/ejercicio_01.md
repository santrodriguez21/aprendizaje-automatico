# Ejercicio 1: Hipótesis MAP, ML y Clasificador Bayesiano Óptimo

**Práctico 3: Aprendizaje Bayesiano, Aprendizaje por Casos y Metodología**  
**Curso:** Aprendizaje Automático

---

## Enunciado

Suponga que cuenta con un conjunto de entrenamiento $D$ sin ruido, y se considera un espacio $H$ en donde las hipótesis *a priori*, cuanto más generales, mayor probabilidad tienen de ser el concepto objetivo. Indique si las siguientes afirmaciones son verdaderas o falsas. Justifique.

- **i.** Find-S da una hipótesis MAP.
- **ii.** Find-S da una hipótesis ML.
- **iii.** Candidate-Elimination con votación es un clasificador bayesiano óptimo.

---

## Fundamentación Teórica Previa

En el marco del **Aprendizaje Bayesiano** (Tom Mitchell, *Machine Learning*, Cap. 6), dado un espacio de hipótesis $H$ y un conjunto de datos observados $D$, el Teorema de Bayes establece la probabilidad posterior de una hipótesis $h \in H$:

$$P(h \mid D) = \frac{P(D \mid h) P(h)}{P(D)} = \frac{P(D \mid h) P(h)}{\sum_{h' \in H} P(D \mid h') P(h')}$$

Donde:
1. **$P(h)$ (Prior):** Probabilidad a priori de que $h$ sea el concepto objetivo antes de observar los datos.
2. **$P(D \mid h)$ (Verosimilitud / Likelihood):** Probabilidad de observar los datos $D$ dado que $h$ es la hipótesis correcta.
   - En un escenario **sin ruido** y determinístico:
     $$P(D \mid h) = \begin{cases} 1 & \text{si } h \text{ es consistente con todos los ejemplos en } D \\ 0 & \text{si } h \text{ es inconsistente con al menos un ejemplo en } D \end{cases}$$
3. **Hipótesis MAP (*Maximum A Posteriori*):**
   $$h_{\text{MAP}} = \arg\max_{h \in H} P(h \mid D) = \arg\max_{h \in H} P(D \mid h) P(h)$$
4. **Hipótesis ML (*Maximum Likelihood*):**
   $$h_{\text{ML}} = \arg\max_{h \in H} P(D \mid h)$$
5. **Clasificador Bayesiano Óptimo (*Bayes Optimal Classifier*):** Para clasificar una nueva instancia $x$, combina las predicciones de todas las hipótesis del espacio ponderadas por su probabilidad posterior:
   $$v_{\text{Bayes}} = \arg\max_{v_j \in V} \sum_{h_i \in H} P(v_j \mid h_i) P(h_i \mid D)$$

---

## Solución Detallada

### Parte i. Find-S da una hipótesis MAP

> **Respuesta:** **FALSA**

#### Justificación:
1. Para datos sin ruido, la verosimilitud $P(D \mid h)$ es $1$ para toda hipótesis perteneciente al Espacio de Versiones ($h \in VS_{H,D}$) y $0$ fuera de él. Por lo tanto, para cualquier hipótesis consistente:
   $$P(h \mid D) \propto P(D \mid h) P(h) = 1 \cdot P(h) = P(h)$$
2. La hipótesis MAP debe maximizar la probabilidad posterior, lo que equivale a maximizar la probabilidad a priori $P(h)$ entre todas las hipótesis en $VS_{H,D}$:
   $$h_{\text{MAP}} = \arg\max_{h \in VS_{H,D}} P(h)$$
3. El enunciado indica que **a mayor generalidad, mayor es la probabilidad a priori** ($h_1 \ge_g h_2 \implies P(h_1) \ge P(h_2)$). Por ende, las hipótesis con mayor probabilidad *a priori* en el espacio de versiones son las hipótesis **más generales** (aquellas en el conjunto límite $G$).
4. El algoritmo **Find-S** busca y devuelve por definición la hipótesis **más específica** del espacio de versiones (el conjunto $S$). Al ser la más específica, es la que tiene la **menor** probabilidad *a priori* dentro de $VS_{H,D}$ (o a lo sumo igual si $VS$ contiene una única hipótesis).
5. Por lo tanto, Find-S no garantiza encontrar una hipótesis MAP; por el contrario, selecciona la que minimiza $P(h)$ entre las consistentes.

---

### Parte ii. Find-S da una hipótesis ML

> **Respuesta:** **VERDADERA**

#### Justificación:
1. Una hipótesis de Máxima Verosimilitud (ML) busca maximizar únicamente la verosimilitud $P(D \mid h)$, sin considerar las probabilidades a priori:
   $$h_{\text{ML}} = \arg\max_{h \in H} P(D \mid h)$$
2. Al tratarse de un conjunto de entrenamiento $D$ **sin ruido** y asumiendo que el concepto objetivo pertenece a $H$, la máxima verosimilitud alcanzable es exactamente $1$.
3. El algoritmo Find-S siempre generaliza estrictamente lo necesario para cubrir todos los ejemplos positivos sin cubrir ningún ejemplo negativo (asumiendo consistencia del espacio de hipótesis). En consecuencia, la hipótesis $h_{\text{Find-S}}$ satisface:
   $$P(D \mid h_{\text{Find-S}}) = 1$$
4. Dado que $1$ es el valor máximo posible de la función de verosimilitud, $h_{\text{Find-S}}$ es una hipótesis de Máxima Verosimilitud (ML). Toda hipótesis consistente con datos no ruidosos es una hipótesis ML.

---

### Parte iii. Candidate-Elimination con votación es un clasificador bayesiano óptimo

> **Respuesta:** **FALSA**

#### Justificación:
1. El **Clasificador Bayesiano Óptimo** asigna a cada hipótesis $h_i \in H$ un peso igual a su probabilidad posterior $P(h_i \mid D)$. Como los datos son sin ruido, $P(h_i \mid D) = \frac{P(h_i)}{\sum_{h \in VS} P(h)}$ para $h_i \in VS$, y $0$ para $h_i \notin VS$.
   $$v_{\text{Bayes}}(x) = \arg\max_{v_j \in V} \sum_{h_i \in VS_{H,D}} P(v_j \mid h_i) P(h_i)$$
2. El esquema de **Candidate-Elimination con votación simple** asume que:
   - Todas las hipótesis tienen el mismo peso (un voto por hipótesis), lo cual es equivalente a suponer una distribución a priori **uniforme** ($P(h) = \text{cte}$).
   - O bien se calcula una votación ponderada únicamente a través de los límites $S$ y $G$, omitiendo la estructura y cantidad de hipótesis intermedias.
3. Dado que en este problema el prior **no es uniforme** (las hipótesis más generales tienen mayor probabilidad a priori), la votación no ponderada de Candidate-Elimination discrepará con el clasificador bayesiano óptimo. Las hipótesis más generales deberían tener mayor poder de voto que las más específicas.
4. Por lo tanto, la votación estándar de Candidate-Elimination no coincide con el clasificador bayesiano óptimo bajo este esquema de probabilidades a priori.
