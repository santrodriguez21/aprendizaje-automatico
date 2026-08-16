# Clase 2: Aprendizaje Conceptual, Find-S y Candidate Elimination

---

## 1. Definición del Problema: Aprendizaje Conceptual

El **aprendizaje conceptual** consiste en inferir una función booleana (concepto) a partir de ejemplos de entrenamiento etiquetados como positivos ($1$) o negativos ($0$).

* **Dominio de instancias ($X$):** Espacio de todos los ejemplos posibles descritos por un conjunto de atributos.
* **Función objetivo ($c$):** $c: X \to \{0, 1\}$, donde $c(x) = 1$ indica que la instancia $x$ es positiva y $c(x) = 0$ indica que es negativa.
* **Espacio de hipótesis ($H$):** Conjunto de todas las hipótesis candidatas que el modelo puede representar, donde cada $h \in H$ es una función $h: X \to \{0, 1\}$.
* **Conjunto de entrenamiento ($D$):** Conjunto de pares ordenados $[x_i, c(x_i)]$:
  $$D = \{ [x_1, c(x_1)], [x_2, c(x_2)], \dots, [x_n, c(x_n)] \}$$
* **Objetivo:** Encontrar una hipótesis $h \in H$ tal que $h(x) = c(x)$ para todo $x \in X$ (no solo para las instancias observadas en $D$, sino también para instancias futuras no vistas).

---

## 2. Ejemplo Guía: ¿Cuándo salva Pedro un examen?

Las instancias $x \in X$ se describen mediante 5 atributos discretos:
1. **Dedicación:** `Alta`, `Media`, `Baja` (3 valores)
2. **Dificultad:** `Alta`, `Media`, `Baja` (3 valores)
3. **Horario:** `Matutino`, `Nocturno` (2 valores)
4. **Humedad:** `Alta`, `Media`, `Baja` (3 valores)
5. **HumorDoc:** `Bueno`, `Malo` (2 valores)

### Conjunto de entrenamiento $D$:

| # Ej | Dedicación | Dificultad | Horario | Humedad | HumorDoc | $c(x)$ (Salva) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **$x_1$** | Alta | Alta | Nocturno | Media | Bueno | **SÍ** ($1$) |
| **$x_2$** | Baja | Media | Matutino | Alta | Malo | **NO** ($0$) |
| **$x_3$** | Media | Alta | Nocturno | Media | Malo | **SÍ** ($1$) |
| **$x_4$** | Media | Alta | Matutino | Alta | Bueno | **NO** ($0$) |

---

## 3. Representación de Hipótesis y Tamaño del Espacio

Cada hipótesis $h$ se representa como una **conjunción de restricciones** sobre los atributos:
* Un valor literal específico (ej. `Alta`, `Nocturno`).
* Un signo de interrogación `?`: Acepta cualquier valor para ese atributo (no restringe).
* Un símbolo nulo $\emptyset$: No acepta ningún valor para ese atributo.

**Notación vectorial:**
$$h = \langle \text{Dedicación}, \text{Dificultad}, \text{Horario}, \text{Humedad}, \text{HumorDoc} \rangle$$

### Hipótesis extremas:
* **Más específica ($h_\emptyset$):** $\langle \emptyset, \emptyset, \emptyset, \emptyset, \emptyset \rangle$ $\implies$ Clasifica **todo** como negativo (Pedro nunca salva).
* **Más general ($h_?$):** $\langle ?, ?, ?, ?, ? \rangle$ $\implies$ Clasifica **todo** como positivo (Pedro siempre salva).

### Conteo del espacio de hipótesis:
* **Espacio de instancias ($|X|$):**
  $$|X| = 3 \times 3 \times 2 \times 3 \times 2 = 108 \text{ instancias posibles}$$
* **Hipótesis sintácticamente distintas:**
  Cada atributo puede tomar sus valores posibles más `?` y $\emptyset$ (número de valores + 2):
  $$|H_{\text{sintáctico}}| = (3+2) \times (3+2) \times (2+2) \times (3+2) \times (2+2) = 5 \times 5 \times 4 \times 5 \times 4 = 2000$$
* **Hipótesis semánticamente distintas:**
  Cualquier hipótesis que contenga al menos un $\emptyset$ clasifica todas las instancias como negativas ($h(x)=0, \forall x$). Por ende, todas esas hipótesis son semánticamente equivalentes a una única hipótesis nula:
  $$|H_{\text{semántico}}| = 1 + (3+1) \times (3+1) \times (2+1) \times (3+1) \times (2+1) = 1 + (4 \times 4 \times 3 \times 4 \times 3) = 1 + 576 = 577$$

---

## 4. Ordenamiento Parcial: De lo General a lo Específico

Dadas dos hipótesis $h_j, h_k \in H$:
* **Más general o igual ($h_j \ge_g h_k$):**
  $$h_j \ge_g h_k \iff \forall x \in X : (h_k(x) = 1 \implies h_j(x) = 1)$$
* **Más específica o igual ($h_j \le_g h_k$):**
  $$h_j \le_g h_k \iff h_k \ge_g h_j$$

En términos de conjuntos: si consideramos a una hipótesis como el conjunto de instancias que clasifica como positivas, $h_j \ge_g h_k$ equivale a que el conjunto de instancias positivas de $h_k$ es un subconjunto del conjunto de $h_j$ ($X_{h_k} \subseteq X_{h_j}$).

---

## 5. Algoritmo Find-S (Encontrar la hipótesis más específica)

### Idea:
Comienza con la hipótesis más restrictiva/específica posible ($\langle \emptyset, \emptyset, \emptyset, \emptyset, \emptyset \rangle$) y la generaliza mínimamente solo lo necesario para cubrir cada nuevo ejemplo **positivo**. **Ignora por completo los ejemplos negativos.**

### Pseudocódigo:
```text
Inicializar h <- <∅, ∅, ∅, ∅, ∅>
Para cada ejemplo de entrenamiento [x, c(x)]:
    Si c(x) == 1 (ejemplo positivo):
        Para cada restricción a_i en h:
            Si x no satisface a_i:
                Reemplazar a_i en h por la restricción inmediatamente más general satisfecha por x
Devolver h
```

### Traza con el ejemplo:
1. $h_0 = \langle \emptyset, \emptyset, \emptyset, \emptyset, \emptyset \rangle$
2. Llega $x_1 = [\text{Alta}, \text{Alta}, \text{Nocturno}, \text{Media}, \text{Bueno}], c(x_1)=\text{SÍ}$:
   $$h_1 = \langle \text{Alta}, \text{Alta}, \text{Nocturno}, \text{Media}, \text{Bueno} \rangle$$
3. Llega $x_2 = [\text{Baja}, \text{Media}, \text{Matutino}, \text{Alta}, \text{Malo}], c(x_2)=\text{NO}$:
   * Se ignora (es negativo).
   $$h_2 = h_1$$
4. Llega $x_3 = [\text{Media}, \text{Alta}, \text{Nocturno}, \text{Media}, \text{Malo}], c(x_3)=\text{SÍ}$:
   * Se compara $h_2$ con $x_3$:
     * Dedicación: `Alta` vs `Media` $\implies$ Generaliza a `?`
     * Dificultad: `Alta` vs `Alta` $\implies$ Mantiene `Alta`
     * Horario: `Nocturno` vs `Nocturno` $\implies$ Mantiene `Nocturno`
     * Humedad: `Media` vs `Media` $\implies$ Mantiene `Media`
     * HumorDoc: `Bueno` vs `Malo` $\implies$ Generaliza a `?`
   $$h_3 = \langle ?, \text{Alta}, \text{Nocturno}, \text{Media}, ? \rangle$$
5. Llega $x_4$ (Negativo) $\implies$ Se ignora.
6. **Resultado final:** $h = \langle ?, \text{Alta}, \text{Nocturno}, \text{Media}, ? \rangle$

### Limitaciones de Find-S:
* No detecta si el conjunto de datos es inconsistente o tiene ruido.
* No puede determinar si aprendió la función objetivo exacta o si existen otras hipótesis válidas.
* ¿Por qué preferir la hipótesis más específica frente a otras posibles? (Falta de visión global).

---

## 6. Espacio de Versiones (Version Space)

* **Consistencia:** Una hipótesis $h$ es **consistente** con el conjunto de entrenamiento $D$ si clasifica correctamente todas las instancias de $D$:
  $$\text{Consistente}(h, D) \iff \forall [x, c(x)] \in D : h(x) = c(x)$$
* **Espacio de Versiones ($VS_{H,D}$):** Es el subconjunto de todas las hipótesis de $H$ que son consistentes con $D$:
  $$VS_{H,D} = \{ h \in H \mid \text{Consistente}(h, D) \}$$

### Algoritmo List-Then-Eliminate:
1. Enumerar todas las hipótesis posibles en una lista: $VS \leftarrow H$.
2. Para cada ejemplo $[x, c(x)] \in D$, eliminar de $VS$ cualquier hipótesis donde $h(x) \ne c(x)$.
3. Devolver $VS$.
* **Problema:** Inviable en la práctica porque $|H|$ suele ser gigantesco o infinito.

---

## 7. Límites $S$ (Específico) y $G$ (General)

Para no listar todas las hipótesis de $VS_{H,D}$, se representa el espacio de versiones utilizando únicamente sus dos fronteras:

* **Límite Específico ($S$):** Conjunto de hipótesis consistentes más específicas:
  $$S_{H,D} = \{ s \in H \mid \text{Consistente}(s, D) \land (\nexists s' \in H, \text{Consistente}(s', D) \land s' <_g s) \}$$
* **Límite General ($G$):** Conjunto de hipótesis consistentes más generales:
  $$G_{H,D} = \{ g \in H \mid \text{Consistente}(g, D) \land (\nexists g' \in H, \text{Consistente}(g', D) \land g' >_g g) \}$$

> **Teorema de Representación del Espacio de Versiones:**
> $$VS_{H,D} = \{ h \in H \mid \exists s \in S_{H,D}, \exists g \in G_{H,D} : s \le_g h \le_g g \}$$
> Toda hipótesis consistente se encuentra en el orden parcial "acotada" entre algún elemento de $S$ y algún elemento de $G$.

---

## 8. Algoritmo Candidate-Elimination

### Pseudocódigo:

```text
Inicializar S <- { <∅, ∅, ∅, ∅, ∅> }
Inicializar G <- { <?, ?, ?, ?, ?> }

Para cada ejemplo de entrenamiento d = [x, c(x)]:
    
    SI d es POSITIVO (c(x) == 1):
        1. Remover de G cualquier hipótesis g inconsistente con x (g(x) != 1).
        2. Para cada hipótesis s en S inconsistente con x (s(x) != 1):
            - Remover s de S.
            - Añadir a S todas las generalizaciones mínimas h de s tales que:
                * h sea consistente con x.
                * Alguna hipótesis en G sea más general o igual que h (∃g ∈ G: g >= h).
        3. Remover de S cualquier hipótesis que sea más general que otra hipótesis en S.

    SI d es NEGATIVO (c(x) == 0):
        1. Remover de S cualquier hipótesis s inconsistente con x (s(x) != 0).
        2. Para cada hipótesis g en G inconsistente con x (g(x) != 0):
            - Remover g de G.
            - Añadir a G todas las especificaciones mínimas h de g tales que:
                * h sea consistente con x.
                * Alguna hipótesis en S sea más específica o igual que h (∃s ∈ S: s <= h).
        3. Remover de G cualquier hipótesis que sea más específica que otra hipótesis en G.
```

---

## 9. Traza Paso a Paso de Candidate-Elimination (Ejemplo Pedro)

* **Inicial:**
  * $S_0 = \{ \langle \emptyset, \emptyset, \emptyset, \emptyset, \emptyset \rangle \}$
  * $G_0 = \{ \langle ?, ?, ?, ?, ? \rangle \}$

* **Paso 1: $x_1 = [\text{Alta}, \text{Alta}, \text{Nocturno}, \text{Media}, \text{Bueno}]$ (+)**
  * $G_1 = \{ \langle ?, ?, ?, ?, ? \rangle \}$
  * $S_1 = \{ \langle \text{Alta}, \text{Alta}, \text{Nocturno}, \text{Media}, \text{Bueno} \rangle \}$

* **Paso 2: $x_2 = [\text{Baja}, \text{Media}, \text{Matutino}, \text{Alta}, \text{Malo}]$ (-)**
  * $S_2 = S_1$
  * Para $G$: se debe especificar $\langle ?, ?, ?, ?, ? \rangle$ para rechazar $x_2$, pero manteniendo consistencia con $S_1$:
    * Dedicación $\ne$ Baja $\implies \langle \text{Alta}, ?, ?, ?, ? \rangle$
    * Dificultad $\ne$ Media $\implies \langle ?, \text{Alta}, ?, ?, ? \rangle$
    * Horario $\ne$ Matutino $\implies \langle ?, ?, \text{Nocturno}, ?, ? \rangle$
    * Humedad $\ne$ Alta $\implies \langle ?, ?, ?, \text{Media}, ? \rangle$
    * HumorDoc $\ne$ Malo $\implies \langle ?, ?, ?, ?, \text{Bueno} \rangle$
  * $G_2 = \{ \langle \text{Alta}, ?, ?, ?, ? \rangle, \langle ?, \text{Alta}, ?, ?, ? \rangle, \langle ?, ?, \text{Nocturno}, ?, ? \rangle, \langle ?, ?, ?, \text{Media}, ? \rangle, \langle ?, ?, ?, ?, \text{Bueno} \rangle \}$

* **Paso 3: $x_3 = [\text{Media}, \text{Alta}, \text{Nocturno}, \text{Media}, \text{Malo}]$ (+)**
  * En $G_2$: se eliminan las hipótesis inconsistentes con $x_3$ (aquellas que clasifican $x_3$ como negativo):
    * $\langle \text{Alta}, ?, ?, ?, ? \rangle$ falla (Dedicación es Media) $\implies$ Se remueve.
    * $\langle ?, ?, ?, ?, \text{Bueno} \rangle$ falla (Humor es Malo) $\implies$ Se remueve.
  * $G_3 = \{ \langle ?, \text{Alta}, ?, ?, ? \rangle, \langle ?, ?, \text{Nocturno}, ?, ? \rangle, \langle ?, ?, ?, \text{Media}, ? \rangle \}$
  * En $S$: se generaliza mínimamente con $x_3$:
  * $S_3 = \{ \langle ?, \text{Alta}, \text{Nocturno}, \text{Media}, ? \rangle \}$

* **Paso 4: $x_4 = [\text{Media}, \text{Alta}, \text{Matutino}, \text{Alta}, \text{Bueno}]$ (-)**
  * $S_4 = S_3$
  * En $G_3$:
    * $\langle ?, \text{Alta}, ?, ?, ? \rangle$ clasifica $x_4$ como positivo (error, porque $x_4$ es negativo) $\implies$ Se elimina/especifica. Al especificarlo contra $S_3$, se ramifica en los otros atributos presentes en $S_3$ (Horario: Nocturno, Humedad: Media), dando hipótesis que ya están o son más específicas.
  * **Fronteras finales:**
    * $$S_4 = \{ \langle ?, \text{Alta}, \text{Nocturno}, \text{Media}, ? \rangle \}$$
    * $$G_4 = \{ \langle ?, ?, \text{Nocturno}, ?, ? \rangle, \langle ?, ?, ?, \text{Media}, ? \rangle \}$$

---

## 10. Clasificación de Nuevas Instancias con $VS_{H,D}$

Una vez obtenido $VS_{H,D}$, para clasificar una instancia nueva $x_{nueva}$:
1. **Unánimemente Positiva:** Si **todas** las hipótesis de $S$ la clasifican como positiva ($s(x_{nueva}) = 1, \forall s \in S$), entonces todas las hipótesis intermedias y de $G$ también la clasificarán como positiva $\implies$ **Positiva con certeza**.
2. **Unánimemente Negativa:** Si **ninguna** hipótesis de $G$ la clasifica como positiva ($g(x_{nueva}) = 0, \forall g \in G$), entonces ninguna hipótesis de $VS$ la acepta $\implies$ **Negativa con certeza**.
3. **Ambigua / Desacuerdo:** Si algunas hipótesis del espacio de versiones la aceptan y otras la rechazan $\implies$ Se puede usar **votación por mayoría** o solicitar al usuario una etiqueta para ese ejemplo.

---

## 11. Sesgo Inductivo (Inductive Bias)

> **Definición formal:**
> Dado un algoritmo de aprendizaje $L$, un conjunto de instancias $X$, una función objetivo $c$, y un conjunto de ejemplos de entrenamiento $D = \{ [x, c(x)] \}$.
> El **sesgo inductivo** de $L$ es el conjunto mínimo de suposiciones/premisas adicionales $B$ tal que para cualquier instancia nueva $x_i \in X$:
> $$(B \land D \land x_i) \vdash L(D, x_i)$$
> *(Es decir, junto con los datos de entrenamiento, $B$ permite deducir lógicamente la clasificación).*

### Sesgo inductivo de nuestros algoritmos:
* **Candidate-Elimination:** El concepto objetivo $c$ está contenido en el espacio de hipótesis $H$ ($c \in H$) y las instancias de entrenamiento no contienen ruido.
* **Find-S:** Asume que $c \in H$, no hay ruido, y además asume una preferencia por la hipótesis más específica posible (sesgo de preferencia / búsqueda).

> [!IMPORTANT]
> **Sin sesgo inductivo, un algoritmo no puede generalizar.** Si el espacio de hipótesis permitiera todas las funciones booleanas posibles ($2^{|X|}$), no habría forma de predecir la etiqueta de ningún ejemplo no visto previamente.
