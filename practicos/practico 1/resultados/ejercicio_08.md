# Ejercicio 8: Espacio de Hipótesis Basado en Disyunciones Puras

**Práctico 1: Introducción y Aprendizaje Conceptual**  
**Curso:** Aprendizaje Automático

---

## Enunciado

Considere un espacio cuyas hipótesis son, en lugar de conjunciones, **disyunciones de restricciones sobre los atributos**. Así, por ejemplo, la hipótesis que representa que Pedro juega cuando el viento es suave o cuando está soleado es: 
$$\langle \text{Soleado}, \emptyset, \emptyset, \text{Suave}, \emptyset, \emptyset \rangle$$

### Preguntas:
a) Calcule la cantidad de posibles hipótesis sintáctica y semánticamente distintas.  
b) Especifique cómo son las reglas de generalización y especificación mínimas para este nuevo espacio.  
c) Aplique paso a paso el algoritmo de cálculo de $VS_{H,D}$, siendo $D$ el conjunto formado por los dos primeros ejemplos del ejercicio 2.  
d) Repita el paso previo considerando ahora únicamente a los ejemplos #3 y #4.

---

## Solución Detallada

### Parte a) Cantidad de Hipótesis Sintáctica y Semánticamente Distintas

Recordemos el número de valores posibles para los 6 atributos del problema de Pedro:
* Cielo (3), Temperatura (2), Humedad (2), Viento (2), Tmp. Agua (2), Tiempo (2).

Una hipótesis disyuntiva se evalúa como:
$$h(x) = 1 \iff (x[\text{Cielo}] = v_1) \lor (x[\text{Temp}] = v_2) \lor \dots \lor (x[\text{Tiempo}] = v_6)$$

#### 1. Hipótesis Sintácticamente Distintas:
Cada posición del vector admite los valores literales del atributo más el símbolo `?` y el símbolo $\emptyset$:
$$|H_{\text{sintáctico}}| = (3+2) \times (2+2)^5 = 5 \times 4^5 = \mathbf{5120}$$

#### 2. Hipótesis Semánticamente Distintas:
* **Hipótesis nula ($h_\emptyset$):** $\langle \emptyset, \emptyset, \emptyset, \emptyset, \emptyset, \emptyset \rangle \implies$ clasifica todas las instancias como negativas ($h(x)=0, \forall x$).
* **Hipótesis universal ($h_?$):** En un espacio disyuntivo, basta con que **un solo atributo** tenga el comodín `?` para que la disyunción sea siempre verdadera para cualquier instancia ($h(x) = 1, \forall x$). Por lo tanto, todas las hipótesis que contienen al menos un `?` colapsan semánticamente en una única hipótesis universal.
* **Hipótesis no triviales:** Cada atributo puede tomar un valor literal específico o el símbolo $\emptyset$ (número de valores + 1):
  $$|H_{\text{semántico}}| = 1 (\text{universal } h_?) + (3+1) \times (2+1)^5 = 1 + 4 \times 3^5 = 1 + 972 = \mathbf{973}$$

---

### Parte b) Reglas de Generalización y Especificación Mínimas

En un espacio disyuntivo, la relación de orden general se comporta de manera **dual** (inversa) respecto al espacio conjuntivo clásico:

* **Hipótesis más específica inicial ($S_0$):**
  $$S_0 = \{ \langle \emptyset, \emptyset, \emptyset, \emptyset, \emptyset, \emptyset \rangle \}$$
* **Hipótesis más general inicial ($G_0$):**
  $$G_0 = \{ \langle ?, \emptyset, \emptyset, \emptyset, \emptyset, \emptyset \rangle \} \equiv \{ \langle ?, ?, ?, ?, ?, ? \rangle \}$$

#### Inversión de Roles:
1. **Ante un ejemplo Positivo ($d = [x, 1]$):**
   * En $S$: No se generaliza agregando `?`, sino que se debe incorporar al menos una restricción que acepte a $x$ si ninguna de las existentes lo cubre.
   * En $G$: Se deben **remover** de las disyunciones aquellas ramas que no cubran ningún ejemplo positivo (especificación).
2. **Ante un ejemplo Negativo ($d = [x, 0]$):**
   * Para que una disyunción sea $0$, **todos** sus términos deben ser falsos simultáneamente.
   * Por lo tanto, ante un ejemplo negativo $x$, cualquier término disyuntivo en $h$ que sea satisfecho por $x$ debe ser **eliminado / reemplazado por $\emptyset$**.

---

### Parte c) Cálculo de $VS_{H,D}$ con los Ejemplos #1 y #2

* **Ejemplo 1:** $d_1 = [\text{Soleado}, \text{Templado}, \text{Normal}, \text{Fuerte}, \text{Templada}, \text{Sin cambios}]$ ($+$)
* **Ejemplo 2:** $d_2 = [\text{Soleado}, \text{Templado}, \text{Alta}, \text{Fuerte}, \text{Templada}, \text{Sin cambios}]$ ($+$)

Ambos ejemplos son positivos.
* $S$ debe cubrir ambos ejemplos. Las hipótesis atómicas más específicas son cada una de las condiciones individuales satisfechas por $d_1$ y $d_2$:
  $$S = \{ \langle \text{Soleado}, \emptyset, \emptyset, \emptyset, \emptyset, \emptyset \rangle, \; \langle \emptyset, \text{Templado}, \emptyset, \emptyset, \emptyset, \emptyset \rangle, \; \langle \emptyset, \emptyset, \emptyset, \text{Fuerte}, \emptyset, \emptyset \rangle, \; \langle \emptyset, \emptyset, \emptyset, \emptyset, \text{Templada}, \emptyset \rangle, \; \langle \emptyset, \emptyset, \emptyset, \emptyset, \emptyset, \text{Sin cambios} \rangle \}$$
* $G$ se mantiene con la hipótesis universal:
  $$G = \{ \langle ?, ?, ?, ?, ?, ? \rangle \}$$

---

### Parte d) Cálculo de $VS_{H,D}$ con los Ejemplos #3 y #4

* **Ejemplo 3:** $d_3 = [\text{Lluvioso}, \text{Frío}, \text{Alta}, \text{Fuerte}, \text{Templada}, \text{Cambiante}]$ ($-$)
* **Ejemplo 4:** $d_4 = [\text{Soleado}, \text{Templado}, \text{Alta}, \text{Fuerte}, \text{Fría}, \text{Cambiante}]$ ($+$)

1. **Al procesar el Negativo $d_3$:**
   * En $G$: Se deben eliminar todos los términos que se evalúen como verdaderos en $d_3$.
   * Por ende, $G$ solo puede contener disyunciones formadas por valores **distintos** a los de $d_3$:
     $$\text{Cielo} \ne \text{Lluvioso} \implies \text{Soleado} \lor \text{Nublado}$$
     $$\text{Temp} \ne \text{Frío} \implies \text{Templado}$$
     $$\text{Humedad} \ne \text{Alta} \implies \text{Normal}$$
     $$\text{Viento} \ne \text{Fuerte} \implies \text{Suave}$$
     $$\text{Tmp. Agua} \ne \text{Templada} \implies \text{Fría}$$
     $$\text{Tiempo} \ne \text{Cambiante} \implies \text{Sin cambios}$$
2. **Al procesar el Positivo $d_4$:**
   * $S$ incorpora los términos satisfechos por $d_4$ que no contradigan a $d_3$ (por ejemplo, $\text{Cielo} = \text{Soleado}$, $\text{Temp} = \text{Templado}$, $\text{Tmp. Agua} = \text{Fría}$).
