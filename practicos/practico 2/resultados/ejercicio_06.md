# Ejercicio 6: Candidate-Elimination sobre el Espacio de Árboles de Decisión

**Práctico 2: Árboles de Decisión**  
**Curso:** Aprendizaje Automático

---

## Enunciado

Luego de ver árboles de decisión y aprendizaje conceptual, un alumno decide aplicar *‘lo mejor de ambos mundos’*: utiliza el algoritmo de **Candidate-Elimination** sobre el espacio de hipótesis de los **árboles de decisión**. 

- **a)** Encuentre los límites $S$ y $G$, luego de procesar los cuatro primeros ejemplos del ejercicio 3.
- **b)** ¿Es una buena opción la elegida por este alumno? ¿Por qué?

---

## Solución Detallada

### Parte a) Límites $S$ y $G$ sobre el Espacio de Árboles de Decisión ($H_{\text{DT}}$)

El espacio de hipótesis de los árboles de decisión discretos $H_{\text{DT}}$ es **completo**: es capaz de representar cualquier función booleana posible sobre el espacio de instancias $X$ (es decir, el conjunto potencia de $X$, $\mathcal{P}(X)$).

Instancias procesadas ($D = \{x_1^+, x_2^+, x_3^-, x_4^+\}$):
- Ejemplos positivos ($D^+$): $x_1, x_2, x_4$.
- Ejemplo negativo ($D^-$): $x_3$.

Al aplicar la definición formal de los límites del Espacio de Versiones ($VS_{H_{\text{DT}}, D}$):

---

#### 1. Límite Específico ($S$):
La hipótesis consistente más específica $S$ es aquella que predice **Sí** **únicamente para los ejemplos positivos observados** en $D$, y predice **No** para cualquier otra instancia del espacio $X$:

$$S = \{ s \}, \quad \text{donde } s(x) = \begin{cases} \text{Sí} & \text{si } x \in \{x_1, x_2, x_4\} \\ \text{No} & \text{en cualquier otro caso} \end{cases}$$

En forma de árbol de decisión / DNF:
$$s(x) \equiv (x = x_1) \lor (x = x_2) \lor (x = x_4)$$

---

#### 2. Límite General ($G$):
La hipótesis consistente más general $G$ es aquella que clasifica como **Sí** a todas las instancias del universo $X$, **excepto a los ejemplos negativos observados** en $D$:

$$G = \{ g \}, \quad \text{donde } g(x) = \begin{cases} \text{No} & \text{si } x \in \{x_3\} \\ \text{Sí} & \text{en cualquier otro caso} \end{cases}$$

En forma lógica:
$$g(x) \equiv \neg (x = x_3)$$

---

### Parte b) Análisis Crítico: ¿Es una buena opción?

> [!CAUTION]
> **NO, es una pésima opción.** Combinar un algoritmo de cálculo exacto del espacio de versiones (*Candidate-Elimination*) con un espacio de hipótesis completo y no restringido (*Árboles de Decisión*) genera dos problemas insalvables:

---

#### 1. Futilidad del Aprendizaje Libre de Sesgo (Imposibilidad de Generalizar)
- Un aprendiz sin **sesgo inductivo restrictivo** es incapaz de generalizar inductivamente más allá de los datos de entrenamiento observados (*Teorema de Mitchell sobre la futilidad del aprendizaje sin sesgo*).
- Para cualquier nueva instancia $x_{\text{test}} \notin D$:
  - La hipótesis más específica predice $s(x_{\text{test}}) = \mathbf{\text{No}}$.
  - La hipótesis más general predice $g(x_{\text{test}}) = \mathbf{\text{Sí}}$.
- En el espacio de versiones $VS_{H_{\text{DT}}, D}$, exactamente la mitad de las hipótesis consistentes votarán **Sí** y la otra mitad votará **No**. Por lo tanto, el sistema **nunca podrá clasificar con certeza ninguna instancia nueva no vista**.

---

#### 2. Explosión Combinatoria y Complejidad Intratable
- Con $|X| = 96$ instancias posibles, el tamaño del espacio de todas las funciones booleanas es:
$$|H_{\text{DT}}| = 2^{|X|} = 2^{96} \approx 7{,}92 \times 10^{28} \text{ hipótesis}$$
- Los límites intermedios y el número de hipótesis en el espacio de versiones crecen de forma combinatoria exponencial, haciendo que el almacenamiento y actualización de las hipótesis de $S$ y $G$ sea completamente inviable computacionalmente.

---

### 💡 Conclusión Comparativa: ¿Por qué ID3 sí funciona?

| Aspecto | Candidate-Elimination en $H_{\text{DT}}$ | Algoritmo ID3 |
|---|:---:|:---:|
| **Espacio $H$** | Completo ($2^{|X|}$) | Completo ($2^{|X|}$) |
| **Búsqueda** | Exhaustiva por límites $S$ y $G$ | Heurística voraz (*greedy*) guiada por Ganancia de Información |
| **Sesgo Inductivo** | Sin sesgo (Fútil) | **Sesgo Preferencial** (Navaja de Ockham: prefiere árboles cortos con atributos de alta ganancia cerca de la raíz) |
| **Capacidad de Generalizar** | $0\%$ en instancias nuevas | **Excelente**, selecciona una única hipótesis simple y predictiva |
