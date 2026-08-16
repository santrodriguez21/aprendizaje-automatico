# Ejercicio 6: Aprendizaje Conceptual en el Plano Entero (Rectángulos)

**Práctico 1: Introducción y Aprendizaje Conceptual**  
**Curso:** Aprendizaje Automático

---

## Enunciado

Considere un espacio compuesto de puntos en el plano entero ($X = \mathbb{N} \times \mathbb{N}$), y un conjunto de hipótesis formadas por rectángulos alineados con los ejes:
$$H = \{ a \le x \le b, \; c \le y \le d \mid a, b, c, d \in \mathbb{N} \}$$

Dados los siguientes ejemplos observados en el plano:

```text
  y ^
  9 |                   - (5,9)
  8 |                                          
  7 |       - (2,7)                          
  6 |                       + (6,6)          
  5 |               + (4,5)             - (9,5)
  4 |   - (1,4)         + (5,4)              
  3 |                                          
  2 |                   - (5,2)              
  1 |                                          
  0 +---+---+---+---+---+---+---+---+---+---> x
    0   1   2   3   4   5   6   7   8   9
```

### Preguntas:
i. Encuentre los conjuntos $S$ y $G$. Dibújelos en el diagrama.  
ii. Si el alumno pudiera elegir el siguiente ejemplo para su entrenamiento, ¿cuál le convendría elegir? ¿Cuál seguramente no?  
iii. Si ud. desea enseñar el concepto $(3 \le x \le 5, \; 2 \le y \le 9)$: ¿cuál es la mínima cantidad de ejemplos que ud. debería dar?

---

## Solución Detallada

### Resumen de Ejemplos de Entrenamiento:
* **Positivos ($+$):** $P = \{ (4, 5), \; (5, 4), \; (6, 6) \}$
* **Negativos ($-$):** $N = \{ (1, 4), \; (2, 7), \; (5, 2), \; (5, 9), \; (9, 5) \}$

---

### Parte i) Cálculo de los Conjuntos Frontera $S$ y $G$

#### 1. Límite Específico ($S$):
El límite más específico $S$ corresponde al **rectángulo envolvente mínimo** que contiene a todos los ejemplos positivos observados en $P$:

* **Límites en $x$:**
  $$a_S = \min(x_+) = \min(4, 5, 6) = 4$$
  $$b_S = \max(x_+) = \max(4, 5, 6) = 6$$
* **Límites en $y$:**
  $$c_S = \min(y_+) = \min(5, 4, 6) = 4$$
  $$d_S = \max(y_+) = \max(5, 4, 6) = 6$$

$$\mathbf{S = \{ [4 \le x \le 6] \land [4 \le y \le 6] \}}$$

*(Verificación: $S$ clasifica como positivos a $(4,5), (5,4), (6,6)$ y excluye correctamente a todos los puntos negativos).*

---

#### 2. Límite General ($G$):
El límite general $G$ está formado por los rectángulos más amplios posibles que cubren a $S$ sin contener ningún punto negativo de $N$:

* **Restricciones impuestas por los puntos negativos cardinales:**
  * Para excluir $(1, 4)$: el borde izquierdo $a$ debe ser $> 1 \implies \mathbf{a \ge 2}$ ($x \ge 2$).
  * Para excluir $(9, 5)$: el borde derecho $b$ debe ser $< 9 \implies \mathbf{b \le 8}$ ($x \le 8$).
  * Para excluir $(5, 2)$: el borde inferior $c$ debe ser $> 2 \implies \mathbf{c \ge 3}$ ($y \ge 3$).
  * Para excluir $(5, 9)$: el borde superior $d$ debe ser $< 9 \implies \mathbf{d \le 8}$ ($y \le 8$).

* **Restricción impuesta por el punto negativo diagonal $(2, 7)$:**
  El punto $(2, 7)$ caería dentro de una caja con $[2 \le x \le 8] \land [3 \le y \le 8]$. Para excluirlo manteniendo a $S = [4 \le x \le 6] \land [4 \le y \le 6]$, tenemos dos especializaciones mínimas posibles:
  1. **Ajustar el borde izquierdo ($x$):** exigir $\mathbf{a \ge 3}$, lo que permite mantener el techo en $d \le 8$.
     $$g_1 = [3 \le x \le 8] \land [3 \le y \le 8]$$
  2. **Ajustar el borde superior ($y$):** exigir $\mathbf{d \le 6}$, lo que permite mantener el borde izquierdo en $a \ge 2$.
     $$g_2 = [2 \le x \le 8] \land [3 \le y \le 6]$$

Por lo tanto, el límite general es:
$$\mathbf{G = \{ [3 \le x \le 8] \land [3 \le y \le 8], \; [2 \le x \le 8] \land [3 \le y \le 6] \}}$$

---

### Diagrama con $S$ y $G$:

```text
  y ^
  9 |                   N              
  8 |           + - - - - - - - - - +      <- Techo de g1
  7 |       N   |               (g1)|        
  6 |       + - | - +=======+ - - - |      <- Techo de g2 y S
  5 |       |   |   | +  (S)|       |   N
  4 |   N   |   |   +=======+   (g2)|      <- Piso de S
  3 |       + - + - - - - - - - - - +      <- Piso de G
  2 |                   N              
  1 |                                          
  0 +---+---+---+---+---+---+---+---+---+---> x
    0   1   2   3   4   5   6   7   8   9
            ^   ^   ^       ^       ^
          x>=2 x>=3 x=4    x=6     x<=8
          (g2) (g1)(S)    (S)     (G der)
```

N: Puntos negativos

---

### Parte ii) Selección Activa de Ejemplos (*Active Learning*)

#### ¿Cuál convendría elegir?
Conviene elegir un punto dentro de la **región de incertidumbre** (aquellos puntos contenidos dentro de $G$ pero que caen fuera de $S$), por ejemplo:
* **Punto $(3, 5)$:** 
  * Si el oráculo responde **Positivo (+)** $\implies$ expande el límite izquierdo de $S$ a $x=3$ y descarta a $g_2$.
  * Si el oráculo responde **Negativo (-)** $\implies$ reduce el límite general de $G$ a $x \ge 4$ para ambas hipótesis.
* **Punto $(5, 7)$:** Permite resolver la incertidumbre sobre la altura del borde superior ($y \le 8$ vs $y \le 6$).
* **Punto $(5, 3)$ o $(7, 5)$:** Permiten ajustar el piso inferior o la pared derecha.

#### ¿Cuál seguramente NO convendría elegir?
1. **Puntos dentro de $S$ (ej. $(5, 5)$ o $(4, 5)$):** Se sabe con $100\%$ de certeza que son **positivos** en todas las hipótesis consistentes del espacio de versiones. Su consulta aporta **cero información nueva**.
2. **Puntos fuera de $G$ (ej. $(0, 0)$, $(1, 4)$, $(10, 10)$ o $(5, 9)$):** Se sabe con $100\%$ de certeza que son **negativos** en todo $VS$. Tampoco aportan información.

---

### Parte iii) Cantidad Mínima de Ejemplos para Enseñar $(3 \le x \le 5, \; 2 \le y \le 9)$

Para fijar de forma unívoca y sin ambigüedad los 4 parámetros del concepto objetivo $c = [3 \le x \le 5] \land [2 \le y \le 9]$ en el reticulado entero:

1. **Ejemplos Positivos (para fijar $S$):**
   * Se requieren **2 ejemplos positivos** colocados en esquinas diagonalmente opuestas del rectángulo objetivo:
     * $x_1^+ = (3, 2)$
     * $x_2^+ = (5, 9)$
   * Con estos dos ejemplos, el rectángulo envolvente mínimo $S$ queda fijado exactamente en $[3 \le x \le 5] \land [2 \le y \le 9]$.

2. **Ejemplos Negativos (para colapsar $G$ sobre $S$):**
   * Se requiere **1 ejemplo negativo adyacente a cada uno de los 4 bordes** para evitar que $G$ se expanda más allá de los límites exactos:
     * Borde izquierdo ($x = 2$): $x_1^- = (2, 2)$
     * Borde derecho ($x = 6$): $x_2^- = (6, 2)$
     * Borde inferior ($y = 1$): $x_3^- = (3, 1)$
     * Borde superior ($y = 10$): $x_4^- = (3, 10)$

$$\text{Cantidad Mínima de Ejemplos} = 2 \text{ Positivos} + 4 \text{ Negativos} = \mathbf{6 \text{ ejemplos}}$$
