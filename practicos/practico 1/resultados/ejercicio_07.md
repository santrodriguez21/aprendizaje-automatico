# Ejercicio 7: Concept Learning - Triángulo Rectángulo Isósceles

**Práctico 1: Introducción y Aprendizaje Conceptual**  
**Curso:** Aprendizaje Automático

---

## Enunciado

Se desea aprender un concepto que se supone es un triángulo rectángulo isósceles en el semiplano $\mathbb{R}^+ \times \mathbb{R}^+$, de la siguiente forma:

```text
  y ^
    |
  a | \
    |  \  Región Positiva (+)
    | + \   x + y <= a
    +----+---> x
    0    a

    a ∈ N⁺ ∪ {∞}
```

Cada hipótesis $h_a$ clasifica los puntos según la regla:
$$h_a(x, y) = 1 \iff x + y \le a, \quad \text{con } a \in \mathbb{N}^+ \cup \{\infty\}$$

### Preguntas:
a) Dé TODAS las hipótesis consistentes con el siguiente conjunto de entrenamiento:
* $(1, 0.5)$ positivo
* $(1.1, 5)$ negativo
* $(2, 0)$ positivo
* $(8, 0)$ negativo

Muestre cómo llega al resultado paso a paso.

b) ¿Qué punto elegiría Ud. como siguiente ejemplo? Dé 2 puntos que, por distintas razones, seguramente no elegiría. Justifique.  
c) Luego de entrenar en (a), decide participar en el concurso *"adivine la clasificación de esta coordenada"* con un premio de $100$ créditos. ¿Cuál es el conjunto de los puntos que SEGURAMENTE le hacen ganar el premio?  
d) ¿Qué sucede si se agrega el siguiente ejemplo: $(1, 1)$ negativo? ¿Qué haría Ud. en este caso?

---

## Solución Detallada

### Parte a) Conjunto de Hipótesis Consistentes Paso a Paso

Evaluamos la suma de coordenadas $s = x + y$ para cada ejemplo del conjunto de entrenamiento:

1. **Ejemplo 1:** $(1, 0.5)$ es **Positivo ($+$)**:
   $$1 + 0.5 = 1.5 \le a \implies a \ge 1.5$$
   Como $a \in \mathbb{N}^+$, esta condición implica que $a \ge 2$.

2. **Ejemplo 2:** $(1.1, 5)$ es **Negativo ($-$)**:
   $$1.1 + 5 = 6.1 > a \implies a < 6.1$$
   Dado que $a \in \mathbb{N}^+$, esta condición implica que $a \le 6$.

3. **Ejemplo 3:** $(2, 0)$ es **Positivo ($+$)**:
   $$2 + 0 = 2.0 \le a \implies a \ge 2.0 \implies a \ge 2$$

4. **Ejemplo 4:** $(8, 0)$ es **Negativo ($-$)**:
   $$8 + 0 = 8.0 > a \implies a < 8.0 \implies a \le 7$$

#### Consolidación de Restricciones:
$$a \ge \max(1.5, 2.0) = 2 \implies a \ge 2$$
$$a < \min(6.1, 8.0) = 6.1 \implies a \le 6$$

Por lo tanto, las hipótesis enteras consistentes son:
$$\mathbf{VS_{H,D} = \{ a = 2, \; a = 3, \; a = 4, \; a = 5, \; a = 6 \}}$$

* **Límite más específico:** $S = \{ a = 2 \}$
* **Límite más general:** $G = \{ a = 6 \}$

---

### Parte b) Elección Estratégica del Siguiente Ejemplo

* **Punto óptimo a elegir:**
  Un punto cuya suma de coordenadas $x + y$ se encuentre en el centro del espacio de versiones para realizar una **búsqueda binaria** óptima:
  * Elegimos por ejemplo $(2, 2)$ o $(4, 0)$, donde $x + y = 4.0$.
  * **Si es Positivo ($+$):** $a \ge 4 \implies$ Descarta inmediatamente $a \in \{2, 3\}$.
  * **Si es Negativo ($-$):** $a \le 3 \implies$ Descarta inmediatamente $a \in \{4, 5, 6\}$.
  * En ambos casos, divide el espacio de hipótesis $VS$ por la mitad en una sola consulta.

* **Dos puntos que SEGURAMENTE NO se elegirían:**
  1. **Punto $(0.5, 0.5)$:** Suma $x+y = 1.0$. Como $1.0 \le 2$ ($S$), es clasificado como **positivo por todas** las hipótesis de $VS$. No aporta información.
  2. **Punto $(10, 0)$ o $(5, 5)$:** Suma $x+y = 10.0$. Como $10.0 > 6$ ($G$), es clasificado como **negativo por todas** las hipótesis de $VS$. No aporta información.

---

### Parte c) Región de Puntos con Certeza Absoluta de Acierto

Para ganar con $100\%$ de seguridad el premio, debemos consultar puntos donde **todas las hipótesis de $VS$ coincidan en su clasificación**:

1. **Región Seguramente Positiva ($\mathcal{R}_+$):**
   Puntos clasificados como positivos por la hipótesis más restrictiva $S$ ($a=2$):
   $$\mathcal{R}_+ = \{ (x, y) \in \mathbb{R}^{+2} \mid x + y \le 2 \}$$

2. **Región Seguramente Negativa ($\mathcal{R}_-$):**
   Puntos clasificados como negativos por la hipótesis más amplia $G$ ($a=6$):
   $$\mathcal{R}_- = \{ (x, y) \in \mathbb{R}^{+2} \mid x + y > 6 \}$$

$$\mathbf{\mathcal{R}_{\text{segura}} = \{ (x, y) \in \mathbb{R}^{+2} \mid x + y \le 2 \} \cup \{ (x, y) \in \mathbb{R}^{+2} \mid x + y > 6 \}}$$

---

### Parte d) Inconsistencia ante el Ejemplo $(1, 1)$ Negativo

* Si se incorpora $(1, 1)$ como **Negativo ($-$)**:
  $$1 + 1 = 2 \implies 2 > a \implies a < 2 \implies a \le 1$$
* Sin embargo, el conjunto previo contenía $(2, 0)$ como **Positivo ($+$)**, lo cual exigía $a \ge 2$.
* **Consecuencia Teórica:**
  $$a \ge 2 \land a \le 1 \implies \text{Contradicción lógica} \implies \mathbf{VS = \emptyset}$$
  El espacio de versiones colapsa y queda completamente vacío.

#### ¿Qué hacer en este caso?
1. **Verificación de Calidad de Datos:** Revisar si el ejemplo $(1, 1)$ contiene un error de etiquetado (ruido) o error de medición.
2. **Relajación del Espacio de Hipótesis:** Considerar formas geométricas más flexibles (por ejemplo, triángulos no isósceles o con desplazamientos de origen).
3. **Cambio de Paradigma de Aprendizaje:** Abandonar la consistencia estricta de Candidate-Elimination y migrar a algoritmos probabilísticos o tolerantes al ruido (como Árboles de Decisión ID3 con ganancia de información, o clasificadores con margen blando / *Soft Margin*).
