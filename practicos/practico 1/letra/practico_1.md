# Práctico 1: Introducción y Aprendizaje Conceptual

**Curso:** Aprendizaje Automático  
**Tema:** Fundamentos, Aprendizaje Conceptual, Find-S, Candidate Elimination y Espacio de Versiones

---

## Ejercicio 1: Fundamentos del Aprendizaje Automático

### a) Ámbito de Aplicabilidad
Dé dos ejemplos en los cuales las técnicas de Aprendizaje Automático sean útiles y dos en los cuales no lo sean. Dé una breve justificación en cada caso.

* **Útiles:**
  1. *Diagnóstico médico / Clasificación de imágenes médicas (ej. detección de tumores):* Existen patrones complejos y variabilidad visual difíciles de codificar mediante reglas estáticas manuales, pero se dispone de grandes volúmenes de datos históricos etiquetados.
  2. *Filtrado de spam y detección de fraude financiero:* La naturaleza del problema es dinámica y adversarial; los patrones evolucionan constantemente y el sistema debe adaptarse automáticamente a partir de nuevos ejemplos.
* **No útiles:**
  1. *Cálculo de la nómina salarial o liquidación de impuestos según normativa fija:* Es un problema determinista con reglas algorítmicas exactas y perfectamente especificadas donde no hay incertidumbre ni generalización a partir de datos.
  2. *Ordenamiento de una lista de enteros o búsqueda en grafos deterministas:* Existen algoritmos óptimos con garantías matemáticas exactas ($O(n \log n)$), haciendo innecesario e ineficiente un enfoque aproximado basado en aprendizaje.

---

### b) Formalización de una Aplicación $(T, P, E)$
Elija una aplicación que considere interesante. Descríbala informalmente, y luego especifique lo más precisamente posible la **tarea ($T$)**, la **medida de desempeño ($P$)**, y la **descripción de la función objetivo**.

* **Aplicación:** Sistema de recomendación personalizada de películas / series.
  * **Descripción informal:** Predecir qué películas le gustarán a un usuario en función de su historial previo de calificaciones, interacciones y preferencias similares de otros usuarios.
  * **Tarea ($T$):** Predecir la calificación estimada $\hat{r}_{u,m} \in [1, 5]$ que un usuario $u$ otorgará a una película $m$ no vista.
  * **Medida de Desempeño ($P$):** Error Cuadrático Medio (*Root Mean Squared Error* - RMSE) sobre un conjunto de evaluación de calificaciones reales reservadas:
    $$\text{RMSE} = \sqrt{\frac{1}{|D_{\text{test}}|} \sum_{(u,m) \in D_{\text{test}}} (r_{u,m} - \hat{r}_{u,m})^2}$$
  * **Función Objetivo:**
    $$f: \mathcal{U} \times \mathcal{M} \longrightarrow \mathbb{R}$$
    donde $\mathcal{U}$ es el espacio de usuarios, $\mathcal{M}$ el catálogo de películas y la salida representa el nivel de preferencia o rating esperado.

---

## Ejercicio 2: Aprendizaje Conceptual - Pedro Juega al Fútbol en la Playa

Se desea aprender bajo qué condiciones a Pedro le gusta ir a jugar al fútbol a la playa a partir del siguiente conjunto de datos:

### Conjunto de Entrenamiento $D$:

| # | Cielo | Temp | Humedad | Viento | Tmp. Agua | Tiempo | $c(x)$ (Juega) |
| :-: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | Soleado | Templado | Normal | Fuerte | Templada | Sin cambios | **Sí** ($1$) |
| **2** | Soleado | Templado | Alta | Fuerte | Templada | Sin cambios | **Sí** ($1$) |
| **3** | Lluvioso | Frío | Alta | Fuerte | Templada | Cambiante | **No** ($0$) |
| **4** | Soleado | Templado | Alta | Fuerte | Fría | Cambiante | **Sí** ($1$) |

### Dominios de los Atributos:
* **Cielo:** `Soleado`, `Lluvioso`, `Nublado` ($3$ valores)
* **Temperatura:** `Templado`, `Frío` ($2$ valores)
* **Humedad:** `Normal`, `Alta` ($2$ valores)
* **Viento:** `Fuerte`, `Suave` ($2$ valores)
* **Tmp. Agua:** `Templada`, `Fría` ($2$ valores)
* **Tiempo:** `Sin cambios`, `Cambiante` ($2$ valores)

---

### i. Tamaño del Espacio de Hipótesis ($H$)
Con la forma de hipótesis conjuntivas vista en el teórico:

* **Espacio de instancias ($|X|$):**
  $$|X| = 3 \times 2 \times 2 \times 2 \times 2 \times 2 = 96 \text{ instancias posibles}$$

* **Hipótesis sintácticamente distintas ($|H_{\text{sintáctico}}|$):**  
  Cada atributo puede tomar sus valores literales más los comodines `?` y $\emptyset$ ($\text{valores} + 2$):
  $$|H_{\text{sintáctico}}| = (3+2) \times (2+2) \times (2+2) \times (2+2) \times (2+2) \times (2+2) = 5 \times 4^5 = 5 \times 1024 = \mathbf{5120}$$

* **Hipótesis semánticamente distintas ($|H_{\text{semántico}}|$):**  
  Cualquier hipótesis con al menos un símbolo $\emptyset$ clasifica todas las instancias como negativas ($h(x)=0, \forall x$), colapsando en una única hipótesis nula $h_{\emptyset}$:
  $$|H_{\text{semántico}}| = 1 + (3+1) \times (2+1)^5 = 1 + 4 \times 3^5 = 1 + 4 \times 243 = 1 + 972 = \mathbf{973}$$

---

### ii. Cálculo del Espacio de Versiones ($VS_{H,D}$)

Aplicando el algoritmo **Candidate-Elimination**:

1. **Inicialización:**
   * $S_0 = \{ \langle \emptyset, \emptyset, \emptyset, \emptyset, \emptyset, \emptyset \rangle \}$
   * $G_0 = \{ \langle ?, ?, ?, ?, ?, ? \rangle \}$

2. **Ejemplo 1:** $d_1 = [\text{Soleado}, \text{Templado}, \text{Normal}, \text{Fuerte}, \text{Templada}, \text{Sin cambios}]$ (**+**)
   * $S_1 = \{ \langle \text{Soleado}, \text{Templado}, \text{Normal}, \text{Fuerte}, \text{Templada}, \text{Sin cambios} \rangle \}$
   * $G_1 = \{ \langle ?, ?, ?, ?, ?, ? \rangle \}$

3. **Ejemplo 2:** $d_2 = [\text{Soleado}, \text{Templado}, \text{Alta}, \text{Fuerte}, \text{Templada}, \text{Sin cambios}]$ (**+**)
   * Humedad varía (`Normal` vs `Alta` $\to `?`$):
   * $S_2 = \{ \langle \text{Soleado}, \text{Templado}, ?, \text{Fuerte}, \text{Templada}, \text{Sin cambios} \rangle \}$
   * $G_2 = \{ \langle ?, ?, ?, ?, ?, ? \rangle \}$

4. **Ejemplo 3:** $d_3 = [\text{Lluvioso}, \text{Frío}, \text{Alta}, \text{Fuerte}, \text{Templada}, \text{Cambiante}]$ (**-**)
   * Se especifican las hipótesis de $G$ para descartar $d_3$ manteniendo consistencia con $S_2$:
     * Cielo $\ne$ Lluvioso $\implies \langle \text{Soleado}, ?, ?, ?, ?, ? \rangle$
     * Temperatura $\ne$ Frío $\implies \langle ?, \text{Templado}, ?, ?, ?, ? \rangle$
     * Tiempo $\ne$ Cambiante $\implies \langle ?, ?, ?, ?, ?, \text{Sin cambios} \rangle$
   * $S_3 = S_2 = \{ \langle \text{Soleado}, \text{Templado}, ?, \text{Fuerte}, \text{Templada}, \text{Sin cambios} \rangle \}$
   * $G_3 = \{ \langle \text{Soleado}, ?, ?, ?, ?, ? \rangle, \langle ?, \text{Templado}, ?, ?, ?, ? \rangle, \langle ?, ?, ?, ?, ?, \text{Sin cambios} \rangle \}$

5. **Ejemplo 4:** $d_4 = [\text{Soleado}, \text{Templado}, \text{Alta}, \text{Fuerte}, \text{Fría}, \text{Cambiante}]$ (**+**)
   * En $S$: Tmp. Agua varía (`Templada` vs `Fría` $\to `?`$) y Tiempo varía (`Sin cambios` vs `Cambiante` $\to `?`$):
     * $S_4 = \{ \langle \text{Soleado}, \text{Templado}, ?, \text{Fuerte}, ?, ? \rangle \}$
   * En $G$: Se elimina $\langle ?, ?, ?, ?, ?, \text{Sin cambios} \rangle$ porque clasifica a $d_4$ incorrectamente como negativo:
     * $G_4 = \{ \langle \text{Soleado}, ?, ?, ?, ?, ? \rangle, \langle ?, \text{Templado}, ?, ?, ?, ? \rangle \}$

#### Fronteras Finales del Espacio de Versiones:
$$\begin{aligned}
S &= \{ \langle \text{Soleado}, \text{Templado}, ?, \text{Fuerte}, ?, ? \rangle \} \\
G &= \{ \langle \text{Soleado}, ?, ?, ?, ?, ? \rangle, \langle ?, \text{Templado}, ?, ?, ?, ? \rangle \}
\end{aligned}$$

---

### iii. Clasificación de Nuevas Instancias

| # | Instancia | $S$ | $G$ | Clasificación Final |
| :-: | :--- | :-: | :-: | :---: |
| **5** | $\langle \text{Soleado}, \text{Templado}, \text{Normal}, \text{Fuerte}, \text{Fría}, \text{Cambiante} \rangle$ | **Sí** ($1$) | **Sí** ($1$) | **SÍ** (Unánime / Con certeza) |
| **6** | $\langle \text{Lluvioso}, \text{Frío}, \text{Normal}, \text{Suave}, \text{Templada}, \text{Sin cambios} \rangle$ | **No** ($0$) | **No** ($0$) | **NO** (Unánime / Con certeza) |
| **7** | $\langle \text{Soleado}, \text{Templado}, \text{Normal}, \text{Suave}, \text{Templada}, \text{Sin cambios} \rangle$ | **No** ($0$, falla Viento) | **Sí** ($1$) | **AMBIGUO** (Voto dividido / Incertidumbre) |
| **8** | $\langle \text{Soleado}, \text{Frío}, \text{Normal}, \text{Fuerte}, \text{Templada}, \text{Sin cambios} \rangle$ | **No** ($0$, falla Temp) | Parcial (1 Sí, 1 No) | **AMBIGUO** (Voto dividido / Incertidumbre) |

---

## Ejercicio 3: Espacio de Hipótesis con Disyunciones ($h_1 \lor h_2$)

Considere un espacio cuyas hipótesis tienen la forma:
$$h = \langle x_1, x_2, x_3, x_4, x_5, x_6 \rangle \lor \langle y_1, y_2, y_3, y_4, y_5, y_6 \rangle$$
*Ejemplo:* $h = \langle ?, \text{Frío}, \text{Alta}, ?, ?, ? \rangle \lor \langle \text{Soleado}, ?, \text{Alta}, ?, ?, \text{Sin cambios} \rangle$

### a) Tamaño del Espacio de Hipótesis
* Sea $N = |H_{\text{conjuntivo}}| = 973$ la cantidad de hipótesis conjuntivas semánticamente distintas.
* El número de pares desordenados de hipótesis conjuntivas es:
  $$\binom{N}{2} + N = \frac{N(N+1)}{2} = \frac{973 \times 974}{2} = \mathbf{473{,}851}$$
* *(Descontando redundancias semánticas donde $h_1 \le_g h_2 \implies h_1 \lor h_2 \equiv h_2$).*

### b) Cálculo del Espacio de Versiones
Al permitir disyunciones de dos conjunciones, el espacio de hipótesis $H$ tiene mayor expresividad. Con los 4 ejemplos de entrenamiento, el algoritmo puede separar los ejemplos positivos en dos subconjuntos y ajustarlos de manera más específica sin verse obligado a generalizar atributos en común cuando son explicados por cláusulas disyuntivas separadas.

---

## Ejercicio 4: Implementación y Experimentación de Find-S

### a) y b) Implementación y Verificación con el Ejemplo de Pedro Salva Examen
* Implementar el algoritmo **Find-S** partiendo de $\langle \emptyset, \emptyset, \emptyset, \emptyset, \emptyset \rangle$.
* Comprobar que tras procesar los 4 ejemplos de Pedro salva examen, el algoritmo produce la hipótesis:
  $$h = \langle ?, \text{Alta}, \text{Nocturno}, \text{Media}, ? \rangle$$

### c) Simulación con Concepto Objetivo $c = \langle ?, \text{Media}, ?, ?, ? \rangle$
* Generar instancias uniformemente al azar del espacio $X$ ($|X| = 108$).
* En cada paso, clasificar la instancia con el concepto objetivo y actualizar la hipótesis con Find-S.
* Medir la cantidad de instancias únicas totales y únicas positivas requeridas para converger exactamente a $\langle ?, \text{Media}, ?, ?, ? \rangle$.

---

## Ejercicio 5: Teorema de Representación del Espacio de Versiones

> **Teorema:**  
> Sea $X$ un conjunto de instancias, $H$ un espacio de hipótesis conjuntivas y $D$ un conjunto de datos de entrenamiento. Todo $h \in H$ es consistente con $D$ si y solo si existen $s \in S$ y $g \in G$ tales que:
> $$s \le_g h \le_g g$$
> donde $S$ y $G$ son los límites más específico y más general de $VS_{H,D}$, respectivamente.

### Demostración:
1. **$(\Leftarrow)$ Suficiencia:**
   * Supongamos que $s \le_g h \le_g g$ con $s \in S$ y $g \in G$.
   * Como $s \in S$, $s$ es consistente con $D$, luego para todo ejemplo positivo $d^+ = [x, 1]$, $s(x) = 1$. Como $s \le_g h$, por definición de orden general $h(x) = 1$.
   * Como $g \in G$, $g$ es consistente con $D$, luego para todo ejemplo negativo $d^- = [x, 0]$, $g(x) = 0$. Como $h \le_g g$, se cumple que si $h(x)=1 \implies g(x)=1$, por contraposición $g(x)=0 \implies h(x)=0$.
   * Por ende, $h$ clasifica correctamente todos los ejemplos positivos y negativos de $D$, siendo consistente ($h \in VS_{H,D}$).
2. **$(\Rightarrow)$ Necesidad:**
   * Por la propia definición constructiva de $S$ (mínima cota superior de los positivos) y $G$ (máxima cota inferior de los negativos), cualquier hipótesis consistente $h$ debe cubrir al menos todo lo que cubre $S$ y a lo sumo lo que permite $G$.

---

## Ejercicio 6: Aprendizaje Conceptual en el Plano Entero (Rectángulos)

Considere un espacio $X = \mathbb{N} \times \mathbb{N}$ y un espacio de hipótesis formadas por rectángulos alineados con los ejes:
$$H = \{ [a \le x \le b] \land [c \le y \le d] \mid a, b, c, d \in \mathbb{N} \}$$

### Gráfica del Conjunto de Entrenamiento:

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
  0 +----------------------------------> x
    0   1   2   3   4   5   6   7   8   9
```

* **Ejemplos Positivos (+):** $(4,4)$, $(5,3)$, $(6,5)$
* **Ejemplos Negativos (-):** $(1,3)$, $(2,6)$, $(5,1)$, $(5,8)$, $(9,4)$

---

### i. Conjuntos $S$ y $G$
* **Límite Específico ($S$):** Es el rectángulo envolvente mínimo (*Bounding Box*) que contiene a todos los ejemplos positivos:
  * $x_{\min} = \min(4, 5, 6) = 4, \quad x_{\max} = \max(4, 5, 6) = 6$
  * $y_{\min} = \min(4, 3, 5) = 3, \quad y_{\max} = \max(4, 3, 5) = 5$
  $$S = \{ [4 \le x \le 6] \land [3 \le y \le 5] \}$$

* **Límite General ($G$):** Son los rectángulos máximos que cubren a $S$ sin contener ningún ejemplo negativo:
  * Restricciones impuestas por los negativos:
    * $(1,3) \implies x \ge 2$
    * $(2,6) \implies x \ge 3 \lor y \le 5$
    * $(5,1) \implies y \ge 2$
    * $(5,8) \implies y \le 7$
    * $(9,4) \implies x \le 8$
  $$G = \{ [2 \le x \le 8] \land [2 \le y \le 7] \}$$

---

### ii. Selección Activa de Ejemplos (*Active Learning*)
* **¿Cuál convendría elegir?**  
  Un punto ubicado en la **región de incertidumbre** (dentro de $G$ pero fuera de $S$), por ejemplo $(3, 4)$ o $(7, 4)$. La respuesta del oráculo dividirá y reducirá significativamente el espacio de versiones.
* **¿Cuál seguramente NO convendría elegir?**  
  * Puntos dentro de $S$ (ej. $(5,4)$) $\to$ Ya se sabe con certeza que son positivos ($100\%$ de las hipótesis consistentes los aceptan).
  * Puntos fuera de $G$ (ej. $(0,0)$ o $(10,10)$) $\to$ Ya se sabe con certeza que son negativos. No aportan información nueva.

---

### iii. Cantidad Mínima de Ejemplos para Enseñar $(3 \le x \le 5, 2 \le y \le 9)$
Para fijar de forma unívoca los 4 límites de un rectángulo discreto:
* Se requieren al menos **2 ejemplos positivos** en vértices opuestos (ej. $(3,2)$ y $(5,9)$) para fijar el rectángulo envolvente $S$.
* Se requieren **4 ejemplos negativos inmediatamente adyacentes** a cada lado ($(2,y)$, $(6,y)$, $(x,1)$, $(x,10)$) para colapsar $G$ exactamente sobre $S$.
* **Mínimo:** **6 ejemplos estratégicamente seleccionados**.

---

## Ejercicio 7: Triángulo Rectángulo Isósceles

Se desea aprender un concepto que es un triángulo rectángulo isósceles en el primer cuadrante $\mathbb{R}^+ \times \mathbb{R}^+$ apoyado en los ejes:
$$h_a(x, y) = 1 \iff x + y \le a, \quad \text{con } a \in \mathbb{N}^+ \cup \{\infty\}$$

```text
  y ^
    | \
  a |  \  Región Positiva (+)
    |   \   x + y <= a
    | +  \
    +-----+-----> x
    0     a
```

### Conjunto de Entrenamiento:
* $d_1 = (1, 0.5)$ (+): $1 + 0.5 = 1.5 \implies a \ge 1.5$
* $d_2 = (1.1, 5)$ (-): $1.1 + 5 = 6.1 \implies a < 6.1$
* $d_3 = (2, 0)$ (+): $2 + 0 = 2.0 \implies a \ge 2.0$
* $d_4 = (8, 0)$ (-): $8 + 0 = 8.0 \implies a < 8.0$

---

### a) Todas las Hipótesis Consistentes
Combinando las restricciones para $a \in \mathbb{N}^+$:
* De los positivos: $a \ge \max(1.5, 2.0) \implies a \ge 2$
* De los negativos: $a < \min(6.1, 8.0) \implies a \le 6$
* **Conjunto de hipótesis consistentes:**
  $$VS = \{ a = 2, a = 3, a = 4, a = 5, a = 6 \}$$
  $$S = \{ a = 2 \}, \qquad G = \{ a = 6 \}$$

---

### b) Elección de Nuevos Ejemplos
* **Punto óptimo a elegir:** Un punto con suma $x+y = 4.0$ (ej. $(2, 2)$ o $(4, 0)$). Si es positivo descarta $a \in \{2, 3\}$; si es negativo descarta $a \in \{4, 5, 6\}$, aplicando búsqueda binaria óptima sobre $VS$.
* **Puntos no informativos:**
  1. $(0.5, 0.5)$ con suma $1.0 \le 2$ $\to$ Siempre clasificado como positivo por todo $VS$.
  2. $(10, 10)$ con suma $20 > 6$ $\to$ Siempre clasificado como negativo por todo $VS$.

---

### c) Región con Certeza de Ganancia
Todos los puntos que caen dentro del límite más específico $S$ ($x + y \le 2$) o fuera del límite más general $G$ ($x + y > 6$):
$$\mathcal{R}_{\text{segura}} = \{ (x,y) \in \mathbb{R}^{+2} \mid x + y \le 2 \} \cup \{ (x,y) \in \mathbb{R}^{+2} \mid x + y > 6 \}$$

---

### d) Inconsistencia con el Ejemplo $(1, 1)$ Negativo
* El punto $(1, 1)$ tiene suma $1 + 1 = 2$.
* Si $(1, 1)$ fuese negativo $\implies a < 2 \implies a \le 1$.
* Pero ya teníamos $(2, 0)$ positivo $\implies a \ge 2$.
* **Consecuencia:** $a \ge 2 \land a \le 1 \implies \text{Contradicción} \implies VS = \emptyset$.
* **Acción a tomar:** Detectar posible ruido en la etiqueta del dato, relajar el supuesto del espacio de hipótesis estricto o utilizar algoritmos con tolerancia estadística al ruido (como ID3 o relajación de restricciones).

---

## Ejercicio 8: Espacio de Hipótesis Basado en Disyunciones Puras

Considere un espacio cuyas hipótesis son **disyunciones de restricciones sobre atributos**:
$$h = \langle v_1, v_2, v_3, v_4, v_5, v_6 \rangle \iff (A_1 = v_1) \lor (A_2 = v_2) \lor \dots \lor (A_6 = v_6)$$
*Ejemplo:* $\langle \text{Soleado}, \emptyset, \emptyset, \text{Suave}, \emptyset, \emptyset \rangle \iff (\text{Cielo} = \text{Soleado}) \lor (\text{Viento} = \text{Suave})$.

### a) Cantidad de Hipótesis Sintáctica y Semánticamente Distintas
* **Sintácticamente:** Igual que en el espacio conjuntivo:
  $$|H_{\text{sintáctico}}| = 5 \times 4^5 = \mathbf{5120}$$
* **Semánticamente:**
  En un espacio disyuntivo, cualquier hipótesis que contenga el comodín `?` en al menos un atributo clasifica **todas** las instancias como positivas ($h(x)=1, \forall x$), colapsando en una única hipótesis universal $h_?$.
  $$|H_{\text{semántico}}| = 1 + (3+1) \times (2+1)^5 = 1 + 4 \times 3^5 = \mathbf{973}$$

---

### b) Reglas de Generalización y Especificación Mínima
Los roles de los ejemplos positivos y negativos se **invierten** respecto al espacio conjuntivo:
* **Ejemplos Positivos:** Restringen las disyunciones posibles (especificación en $G$).
* **Ejemplos Negativos:** Obligan a incluir restricciones disyuntivas para no aceptar el ejemplo negativo (generalización en $S$).

---

### c) y d) Traza del Espacio de Versiones $VS_{H,D}$
* Se calculan los límites $S$ y $G$ para el conjunto $\{d_1, d_2\}$ y posteriormente para $\{d_3, d_4\}$ aplicando las reglas disyuntivas duales.

---

## Referencias Bibliográficas

1. **Mitchell, Tom M. (1997).** *Machine Learning*. McGraw-Hill Science/Engineering/Math.
   * **Capítulo 1:** *"Introduction"* (pp. 1–18) — Definición formal $(T, P, E)$ y diseño de sistemas de aprendizaje.
   * **Capítulo 2:** *"Concept Learning and the General-to-Specific Ordering"* (pp. 20–49) — Algoritmos Find-S, Candidate-Elimination, Espacio de Versiones, Teorema de Representación y Sesgo Inductivo.
2. **Valiant, Leslie G. (1984).** *A Theory of the Learnable*. Communications of the ACM, 27(11), 1134–1142.
   * Fundamentos de la teoría de aprendizaje computacional y aprendibilidad de conceptos geométricos y booleanos.
3. **Cohn, David A.; Ghahramani, Zoubin; Jordan, Michael I. (1996).** *Active Learning with Statistical Models*. Journal of Artificial Intelligence Research, 4, 129–145.
   * Selección óptima de consultas e instancias en la región de incertidumbre (*Active Learning*).
