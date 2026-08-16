# Ejercicio 5: Teorema de Representación del Espacio de Versiones

**Práctico 1: Introducción y Aprendizaje Conceptual**  
**Curso:** Aprendizaje Automático

---

## Enunciado

Pruebe el teorema de la representación del espacio de versiones.

---

## Solución Formal

### Enunciado del Teorema

> **Teorema de Representación del Espacio de Versiones (Tom Mitchell, 1978 / 1997):**
> 
> Sea $X$ un conjunto de instancias, $H$ un espacio de hipótesis booleanas sobre $X$ parcialmente ordenado por la relación de generalidad $\ge_g$, y $D = \{ [x_1, c(x_1)], \dots, [x_m, c(x_m)] \}$ un conjunto de ejemplos de entrenamiento.
>
> Sean $S_{H,D}$ y $G_{H,D}$ los conjuntos frontera más específico y más general de $VS_{H,D}$, definidos como:
> $$S = \{ s \in H \mid \text{Consistente}(s, D) \land (\nexists s' \in H : \text{Consistente}(s', D) \land s' <_g s) \}$$
> $$G = \{ g \in H \mid \text{Consistente}(g, D) \land (\nexists g' \in H : \text{Consistente}(g', D) \land g' >_g g) \}$$
>
> Entonces, para toda hipótesis $h \in H$:
> $$h \in VS_{H,D} \iff \exists s \in S, \; \exists g \in G : s \le_g h \le_g g$$
> *(Es decir, toda hipótesis consistente está acotada entre algún elemento de $S$ y algún elemento de $G$).*

---

### Demostración Matemática

Debemos demostrar la doble implicación:
1. **Suficiencia ($\Leftarrow$):** Si $\exists s \in S, \exists g \in G$ tal que $s \le_g h \le_g g$, entonces $h \in VS_{H,D}$ ($h$ es consistente con $D$).
2. **Necesidad ($\Rightarrow$):** Si $h \in VS_{H,D}$, entonces $\exists s \in S, \exists g \in G$ tales que $s \le_g h \le_g g$.

---

#### 1. Demostración de la Suficiencia ($\Leftarrow$)

Supongamos que existen $s \in S$ y $g \in G$ tales que:
$$s \le_g h \le_g g$$

Debemos probar que $\text{Consistente}(h, D)$, es decir, que para todo par $[x, c(x)] \in D$, $h(x) = c(x)$.

* **Caso A: Ejemplo Positivo ($c(x) = 1$)**
  * Dado que $s \in S$, $s$ es consistente con $D$, luego $s(x) = 1$.
  * Por hipótesis, $s \le_g h$, lo que por definición de orden general significa:
    $$\forall x \in X : (s(x) = 1 \implies h(x) = 1)$$
  * Como $s(x) = 1$, se deduce inmediatamente que **$h(x) = 1 = c(x)$**.

* **Caso B: Ejemplo Negativo ($c(x) = 0$)**
  * Dado que $g \in G$, $g$ es consistente con $D$, luego $g(x) = 0$.
  * Por hipótesis, $h \le_g g$, lo que significa:
    $$\forall x \in X : (h(x) = 1 \implies g(x) = 1)$$
  * Aplicando la equivalencia por contrarrecíproca (contraposición lógica):
    $$\forall x \in X : (g(x) = 0 \implies h(x) = 0)$$
  * Como $g(x) = 0$, se deduce inmediatamente que **$h(x) = 0 = c(x)$**.

Por lo tanto, $h$ clasifica correctamente todos los ejemplos positivos y negativos de $D$. En consecuencia:
$$\text{Consistente}(h, D) \implies h \in VS_{H,D} \quad \blacksquare$$

---

#### 2. Demostración de la Necesidad ($\Rightarrow$)

Supongamos que $h \in VS_{H,D}$, es decir, $h$ es consistente con $D$. Debemos probar que existen $s \in S$ y $g \in G$ tales que $s \le_g h \le_g g$.

* **Existencia de $s \in S$ con $s \le_g h$:**
  * Si $h \in S$, tomamos $s = h$ y se cumple trivialmente $s \le_g h$.
  * Si $h \notin S$, como $h$ es consistente con $D$ pero no pertenece a $S$, por la definición de $S$ debe existir alguna hipótesis consistente $h_1 \in H$ tal que $h_1 <_g h$.
  * Si $h_1 \in S$, ya encontramos $s = h_1$. Si no, repetimos el proceso obteniendo una cadena descendente:
    $$\dots <_g h_2 <_g h_1 <_g h$$
  * Como el espacio de hipótesis $H$ considerado sobre atributos discretos es finito y acotado inferiormente por la hipótesis nula $\emptyset$, esta cadena debe tener un elemento minimal consistente, el cual por definición pertenece a $S$.
  * Por lo tanto, existe $s \in S$ tal que $s \le_g h$.

* **Existencia de $g \in G$ con $h \le_g g$:**
  * De manera análoga y dual, si $h \in G$, tomamos $g = h$.
  * Si $h \notin G$, por definición de $G$ existe una cadena ascendente de hipótesis consistentes más generales:
    $$h <_g g_1 <_g g_2 <_g \dots$$
  * Dado que $H$ es finito y acotado superiormente por la hipótesis universal `?`, la cadena alcanza un elemento maximal consistente, el cual pertenece a $G$.
  * Por lo tanto, existe $g \in G$ tal que $h \le_g g$.

Combinando ambos resultados, concluimos que existen $s \in S$ y $g \in G$ tales que:
$$s \le_g h \le_g g \quad \blacksquare$$

---

### Importancia Teórica y Práctica del Teorema
1. **Representación compacta:** Permite representar espacios de versiones gigantescos (incluso infinitos o combinatorios) utilizando únicamente dos conjuntos frontera ($S$ y $G$).
2. **Clasificación unánime:** Una nueva instancia se clasifica como positiva con certeza si y solo si es aceptada por todo $s \in S$, y como negativa con certeza si y solo si es rechazada por todo $g \in G$.
