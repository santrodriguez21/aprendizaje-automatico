# 📖 Glosario de Términos y Notación Formal

Guía rápida de referencia con la notación formal, definiciones y conceptos fundamentales de la materia, organizados por temática.

---

## 📌 1. Fundamentos y Paradigmas de Aprendizaje (Clase 1)

| Símbolo / Término | Definición / Notación | Significado / Contexto de la Clase |
| :--- | :--- | :--- |
| **$T$ (Tarea)** | Labor específica | La labor que el sistema debe realizar (ej. clasificar un punto como Rojo/Azul). |
| **$P$ (Desempeño / Performance)** | Métrica cuantitativa | Medida para evaluar el éxito o precisión en la tarea $T$ (ej. Porcentaje de aciertos / Accuracy). |
| **$E$ (Experiencia)** | Datos / Interacciones | Conjunto de ejemplos históricos o datos etiquetados disponibles para entrenar. |
| **Definición de Tom Mitchell (1997)** | $(T, P, E)$ | *"Un programa aprende de la experiencia $E$ respecto a tareas $T$ y medida $P$, si su desempeño en $T$, medido por $P$, mejora con $E$."* |
| **Función Objetivo ($f / c / V$)** | $f: X \to Y$ | La función verdadera desconocida que el sistema busca aprender a partir de los datos. |
| **Aprendizaje Supervisado** | $\{ (x_i, y_i) \}$ | Se dispone de ejemplos con su etiqueta o clase objetivo conocida (*Ground Truth*). |
| **Aprendizaje No Supervisado** | $\{ x_i \}$ (sin etiquetas) | Busca descubrir patrones ocultos o agrupamientos naturales (*clustering*). |
| **Aprendizaje por Refuerzos** | Agente $\leftrightarrow$ Entorno | Un agente aprende a tomar acciones para maximizar una recompensa acumulada. |

---

## 🎯 2. Aprendizaje Conceptual y Espacios de Versiones (Clase 2 y Práctico 1)

| Símbolo / Término | Definición / Notación | Significado / Contexto de la Clase |
| :--- | :--- | :--- |
| **$X$ (Espacio de Instancias)** | $X = V(A_1) \times \dots \times V(A_n)$ | Espacio de todos los ejemplos posibles descritos por el conjunto de atributos. |
| **$x \in X$ (Instancia)** | $x = [a_1, a_2, \dots, a_n]$ | Un ejemplo particular del dominio. |
| **$c: X \to \{0, 1\}$** | Concepto / Función objetivo | Función booleana que clasifica cada instancia como positiva ($1$) o negativa ($0$). |
| **$D$ (Conjunto de Entrenamiento)** | $D = \{ [x_1, c(x_1)], \dots, [x_m, c(x_m)] \}$ | Muestra de ejemplos observados con sus clasificaciones. |
| **$H$ (Espacio de Hipótesis)** | $H = \{ h \mid h: X \to \{0, 1\} \}$ | Conjunto de todas las hipótesis que el modelo es capaz de expresar/representar. |
| **$h \in H$ (Hipótesis)** | $h = \langle v_1, v_2, \dots, v_n \rangle$ | Conjunción de restricciones sobre los atributos que estima el concepto $c$. |
| **$\emptyset$ (Restricción Nula)** | No acepta ningún valor | Restricción imposible en un atributo (anula toda la hipótesis conjuntiva). |
| **`?` (Comodín / Cualquier valor)** | Acepta cualquier valor | No impone ninguna restricción sobre ese atributo. |
| **$h_\emptyset$** | $\langle \emptyset, \emptyset, \dots, \emptyset \rangle$ | **Hipótesis más específica posible:** clasifica todas las instancias como negativas. |
| **$h_?$** | $\langle ?, ?, \dots, ? \rangle$ | **Hipótesis más general posible:** clasifica todas las instancias como positivas. |
| **$h_j \ge_g h_k$** | $\forall x \in X : (h_k(x) = 1 \implies h_j(x) = 1)$ | **Más general o igual:** $h_j$ clasifica como positivo a todo lo que $h_k$ clasifica como positivo. |
| **$h_j \le_g h_k$** | $h_k \ge_g h_j$ | **Más específica o igual.** |
| **$\text{Consistente}(h, D)$** | $\forall [x, c(x)] \in D : h(x) = c(x)$ | $h$ clasifica correctamente todos los ejemplos observados en $D$. |
| **$VS_{H,D}$ (Espacio de Versiones)** | $\{ h \in H \mid \text{Consistente}(h, D) \}$ | Subconjunto de todas las hipótesis de $H$ consistentes con $D$. |
| **$S_{H,D}$ (Límite Específico)** | Hipótesis consistentes minimales | Conjunto de hipótesis consistentes **más específicas** de $VS_{H,D}$. |
| **$G_{H,D}$ (Límite General)** | Hipótesis consistentes maximales | Conjunto de hipótesis consistentes **más generales** de $VS_{H,D}$. |
| **Teorema de Representación** | $VS_{H,D} = \{ h \in H \mid \exists s \in S, \exists g \in G : s \le_g h \le_g g \}$ | Toda hipótesis consistente está acotada entre algún elemento de $S$ y uno de $G$. |
| **Algoritmo Find-S** | Bottom-Up voraz | Inicia en $h_\emptyset$ y generaliza mínimamente solo ante ejemplos positivos. |
| **Algoritmo Candidate-Elimination** | Búsqueda bidireccional | Mantiene y ajusta simultáneamente los límites $S$ y $G$ con cada ejemplo de $D$. |

---

## 🌳 3. Árboles de Decisión y Algoritmo ID3 (Clase 3)

| Símbolo / Término | Definición / Notación | Significado / Contexto de la Clase |
| :--- | :--- | :--- |
| **Árbol de Decisión** | Estructura jerárquica | Nodos = atributos de prueba, Ramas = posibles valores, Hojas = clasificación. |
| **Forma Normal Disyuntiva (DNF)** | Disyunción de ramas positivas | Expresión lógica de la forma $(r_1) \lor (r_2) \lor \dots \lor (r_k)$ de las ramas que dan Sí. |
| **$\text{Entropía}(S)$** | $-\sum_{i=1}^c p_i \log_2(p_i)$ | Mide la impureza, incertidumbre o cantidad promedio de bits requeridos para codificar $S$. |
| **$p_+$ / $p_-$** | Proporciones de clases | Fracción de ejemplos positivos y negativos en $S$ ($\text{Entropía} = -p_+\log_2(p_+) - p_-\log_2(p_-)$). |
| **$\text{Ganancia}(S, A)$** | $\text{Ent}(S) - \sum_{v \in Valores(A)} \frac{\|S_v\|}{\|S\|} \text{Ent}(S_v)$ | **Ganancia de Información:** Reducción esperada en la entropía al particionar por el atributo $A$. |
| **$Valores(A)$** | Dominio del atributo | Conjunto de valores posibles que puede tomar el atributo $A$. |
| **$S_v$** | $\{ x \in S \mid x[A] = v \}$ | Subconjunto de ejemplos de $S$ donde el atributo $A$ tiene el valor $v$. |
| **Algoritmo ID3** | Top-Down voraz sin backtracking | Construye el árbol eligiendo recursivamente el atributo con mayor $\text{Ganancia}(S, A)$. |

---

## 🧠 4. Sesgo Inductivo y Principios de Búsqueda (Clases 2 y 3)

| Símbolo / Término | Definición / Notación | Significado / Contexto de la Clase |
| :--- | :--- | :--- |
| **$B$ (Sesgo Inductivo)** | $(B \land D \land x_i) \vdash L(D, x_i)$ | Conjunto mínimo de suposiciones que junto a $D$ permite deducir la clasificación de $x_i$. |
| **Sesgo Preferencial** | Preferencia de búsqueda | El espacio $H$ es completo (contiene todas las funciones), pero el algoritmo prefiere unas sobre otras (ej. ID3 prefiere árboles más cortos). |
| **Sesgo Restrictivo** | Restricción del lenguaje | El espacio $H$ es incompleto a priori (ej. Candidate-Elimination solo permite conjunciones). |
| **Navaja de Ockham** | Principio de parsimonia | *"Cuando se ofrecen varias explicaciones, es preferible la más simple que se ajuste a los datos."* (William de Ockham, S.XIV). |
