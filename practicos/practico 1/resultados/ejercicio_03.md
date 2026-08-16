# Ejercicio 3: Espacio de Hipótesis con Disyunciones ($h_1 \lor h_2$)

**Práctico 1: Introducción y Aprendizaje Conceptual**  
**Curso:** Aprendizaje Automático

---

## Enunciado

Considere para el ejercicio anterior un espacio cuyas hipótesis tienen la siguiente forma: 
$$\langle x_1, x_2, x_3, x_4, x_5, x_6 \rangle \lor \langle y_1, y_2, y_3, y_4, y_5, y_6 \rangle$$

*Por ejemplo:* $h: \langle ?, \text{Frío}, \text{Alto}, ?, ?, ? \rangle \lor \langle \text{Soleado}, ?, \text{Alto}, ?, ?, \text{Sin cambios} \rangle$

### Preguntas:
a) ¿Cuál es el tamaño del espacio de hipótesis?  
b) Calcule el espacio de versiones.

---

## Solución Detallada

### Parte a) Tamaño del Espacio de Hipótesis

Sea $H_{\text{conj}}$ el espacio de hipótesis puramente conjuntivas del Ejercicio 2:
* Cantidad de hipótesis conjuntivas sintácticamente distintas: $N_{\text{sint}} = 5120$.
* Cantidad de hipótesis conjuntivas semánticamente distintas: $N_{\text{sem}} = 973$.

Una hipótesis en este nuevo espacio está formada por la disyunción de dos hipótesis conjuntivas $h = c_1 \lor c_2$.

#### 1. Conteo Sintáctico:
Dado que el operador lógico $\lor$ es conmutativo ($c_1 \lor c_2 \equiv c_2 \lor c_1$), se trata de combinaciones con repetición (pares no ordenados de hipótesis conjuntivas sintácticas):

$$|H_{\text{sintáctico}}| = \binom{N_{\text{sint}}}{2} + N_{\text{sint}} = \frac{N_{\text{sint}}(N_{\text{sint}} + 1)}{2}$$
$$|H_{\text{sintáctico}}| = \frac{5120 \times 5121}{2} = \mathbf{13{,}109{,}760 \text{ hipótesis sintácticas}}$$

*(Si se considera el orden en la tupla sintáctica: $5120^2 = 26{,}214{,}400$).*

#### 2. Conteo Semántico:
Semánticamente, consideramos pares no ordenados de hipótesis conjuntivas semánticas no nulas más la hipótesis nula:
* Cantidad de hipótesis conjuntivas semánticas: $N = 973$.
* Pares desordenados de hipótesis conjuntivas:
  $$\frac{N(N+1)}{2} = \frac{973 \times 974}{2} = 473{,}851$$

* **Equivalencias y redundancias semánticas a descontar:**
  Si $c_1 \le_g c_2$ (es decir, $c_1$ es más específica que $c_2$, lo que implica que todo ejemplo cubierto por $c_1$ ya está cubierto por $c_2$), entonces:
  $$c_1 \lor c_2 \equiv c_2$$
  Estas disyunciones redundantes no aportan nuevas funciones booleanas en el espacio semántico. Por lo tanto, el número exacto de conceptos semánticamente distintos es estrictamente menor a $473{,}851$, aunque este valor constituye una cota superior estándar.

---

### Parte b) Cálculo del Espacio de Versiones

Al aumentar la expresividad del lenguaje de hipótesis permitiendo una disyunción de dos términos ($c_1 \lor c_2$), el espacio de hipótesis $H$ deja de estar restringido a funciones puramente conjuntivas.

#### Impacto en los Límites $S$ y $G$:

1. **Límite Específico ($S$):**
   * En el espacio conjuntivo original, $S$ se vio forzado a generalizar los atributos `Humedad`, `Tmp. Agua` y `Tiempo` a `?` para cubrir conjuntamente a $d_1$, $d_2$ y $d_4$.
   * En el espacio disyuntivo, los ejemplos positivos pueden repartirse entre los dos términos disyuntivos:
     * Por ejemplo, podemos agrupar $\{d_1, d_2\}$ en el primer término y $\{d_4\}$ en el segundo término:
       $$c_1 = \langle \text{Soleado}, \text{Templado}, ?, \text{Fuerte}, \text{Templada}, \text{Sin cambios} \rangle$$
       $$c_2 = \langle \text{Soleado}, \text{Templado}, \text{Alta}, \text{Fuerte}, \text{Fría}, \text{Cambiante} \rangle$$
       $$h_S = c_1 \lor c_2$$
   * Como $c_1$ cubre a $d_1$ y $d_2$, y $c_2$ cubre a $d_4$, la disyunción $c_1 \lor c_2$ clasifica correctamente todos los ejemplos positivos y rechaza al negativo $d_3$.
   * **Conclusión:** El conjunto $S$ ahora contendrá hipótesis **mucho más específicas** que en el caso conjuntivo, conservando restricciones literales sobre `Tmp. Agua` y `Tiempo` en lugar de reemplazarlas por comodines `?`.

2. **Límite General ($G$):**
   * Las hipótesis más generales siguen acotadas por la necesidad de rechazar al ejemplo negativo $d_3 = [\text{Lluvioso}, \text{Frío}, \text{Alta}, \text{Fuerte}, \text{Templada}, \text{Cambiante}]$.
   * Las hipótesis $G$ del caso conjuntivo ($\langle \text{Soleado}, ?, ?, ?, ?, ? \rangle \lor \emptyset \equiv \langle \text{Soleado}, ?, ?, ?, ?, ? \rangle$) siguen perteneciendo a $G$.
   * Adicionalmente, aparecen combinaciones disyuntivas generales como:
     $$g = \langle \text{Soleado}, ?, ?, ?, ?, ? \rangle \lor \langle ?, \text{Templado}, ?, ?, ?, ? \rangle$$
     que cubren aún más instancias no vistas pero siguen siendo consistentes con $D$.
