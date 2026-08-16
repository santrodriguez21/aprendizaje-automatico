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
  9 |                               
  8 |               - (5,8)         
  7 |                               
  6 |       - (2,6)                 
  5 |                       + (6,5) 
  4 |               + (4,4)         - (9,4)
  3 |   - (1,3)     + (5,3)         
  2 |                               
  1 |               - (5,1)         
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
* **Positivos ($+$):** $P = \{ (4,4), (5,3), (6,5) \}$
* **Negativos ($-$):** $N = \{ (1,3), (2,6), (5,1), (5,8), (9,4) \}$

---

### Parte i) Cálculo de los Conjuntos Frontera $S$ y $G$

#### 1. Límite Específico ($S$):
El límite más específico $S$ corresponde al **rectángulo envolvente mínimo (*Bounding Box*)** que contiene a todos los ejemplos positivos observados:

* Límites en $x$:
  $$a_S = \min(x_+) = \min(4, 5, 6) = 4$$
  $$b_S = \max(x_+) = \max(4, 5, 6) = 6$$
* Límites en $y$:
  $$c_S = \min(y_+) = \min(4, 3, 5) = 3$$
  $$d_S = \max(y_+) = \max(4, 3, 5) = 5$$

$$\mathbf{S = \{ [4 \le x \le 6] \land [3 \le y \le 5] \}}$$

---

#### 2. Límite General ($G$):
El límite general $G$ está formado por los rectángulos más amplios posibles que cubren a $S$ sin contener ningún ejemplo negativo de $N$:

* Restricciones impuestas por cada negativo $(x_n, y_n)$:
  * $(1, 3) \implies x \ge 2$ (el borde izquierdo $a$ no puede ser $\le 1$).
  * $(9, 4) \implies x \le 8$ (el borde derecho $b$ no puede ser $\ge 9$).
  * $(5, 1) \implies y \ge 2$ (el borde inferior $c$ no puede ser $\le 1$).
  * $(5, 8) \implies y \le 7$ (el borde superior $d$ no puede ser $\ge 8$).
  * $(2, 6) \implies$ este punto está arriba a la izquierda. Como $a \ge 2$ y $d \le 7$, el punto $(2,6)$ es descartado naturalmente si $a \ge 3$ o si $d \le 5$. Con $a=2$ y $d \le 5$, o $a=3$ y $d \le 7$.
  
Por ende, las hipótesis más generales en $G$ son:
$$\mathbf{G = \{ [2 \le x \le 8] \land [2 \le y \le 5], \; [3 \le x \le 8] \land [2 \le y \le 7] \}}$$

*(Si se asume una cota rectangular global simple, $G = \{ [2 \le x \le 8] \land [2 \le y \le 7] \}$ descartando $(2,6)$ mediante la esquina).*

---

### Diagrama con $S$ y $G$:

```text
  y ^
  8 |               - (5,8)         
  7 |   + - - - - - - - - - - +  <- Techo de G (y <= 7)
  6 |   |   - (2,6)           |     
  5 |   |           +======+  |  <- Techo de S (y = 5)
  4 |   |           | +  + |  |  - (9,4)
  3 | - | (1,3)     | +    |  |  <- Piso de S (y = 3)
  2 |   + - - - - - +======+ -+  <- Piso de G (y >= 2)
  1 |               - (5,1)         
  0 +---+---+---+---+---+---+---+---+---> x
    0   1   2   3   4   5   6   7   8
            ^       ^      ^   ^
          x>=2     x=4    x=6 x<=8
         (G izq)   (S)    (S) (G der)
```

---

### Parte ii) Selección Activa de Ejemplos (*Active Learning*)

#### ¿Cuál convendría elegir?
Conviene elegir un punto dentro de la **región de incertidumbre** (aquellos puntos contenidos dentro de $G$ pero que caen fuera de $S$), por ejemplo:
* **Punto $(3, 4)$:** Si el oráculo responde **Positivo**, expande inmediatamente el límite izquierdo de $S$ a $x=3$. Si responde **Negativo**, ajusta el límite de $G$ a $x \ge 4$.
* **Punto $(7, 4)$ o $(5, 6)$:** Permiten resolver las dudas sobre los límites derecho y superior respectivamente.

#### ¿Cuál seguramente NO convendría elegir?
1. **Puntos dentro de $S$ (ej. $(5, 4)$):** Se sabe con $100\%$ de certeza que son **positivos** en todas las hipótesis consistentes. Su consulta no aporta nada de información nueva.
2. **Puntos fuera de $G$ (ej. $(0, 0)$, $(10, 10)$ o $(5, 9)$):** Se sabe con certeza que son **negativos** en todo $VS$. Tampoco aportan información.

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
