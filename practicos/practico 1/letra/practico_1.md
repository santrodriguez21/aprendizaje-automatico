# Aprendizaje Automático
## Práctico 1: Introducción y Aprendizaje Conceptual

---

### Ejercicio 1
a) Dé dos ejemplos en los cuales las técnicas de Aprendizaje Automático sean útiles y dos en los cuales no lo sean. Dé una breve justificación en cada caso.

b) Elija una aplicación que considere interesante. Descríbala informalmente, y luego especifique lo más precisamente posible la tarea, la medida de performance, y la descripción de la función objetivo.

---

### Ejercicio 2
Se desea aprender bajo qué condiciones a Pedro le gusta ir a jugar al fútbol a la playa:

| # | Cielo | Temp | Humedad | Viento | Tmp. Agua | Tiempo | Juega |
| :-: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | Soleado | Templado | Normal | Fuerte | Templada | Sin cambios | Sí |
| 2 | Soleado | Templado | Alta | Fuerte | Templada | Sin cambios | Sí |
| 3 | Lluvioso | Frío | Alta | Fuerte | Templada | Cambiante | No |
| 4 | Soleado | Templado | Alta | Fuerte | Fría | Cambiante | Sí |

Con los siguientes posibles valores para cada atributo:
* **Cielo:** Soleado, Lluvioso, Nublado
* **Temperatura:** Templado, Frío
* **Humedad:** Normal, Alta
* **Viento:** Fuerte, Suave
* **Tmp.Agua:** Templada, Fría
* **Tiempo:** Sin cambios, Cambiante

i. Con la forma de las hipótesis vista en el teórico: ¿cuál es el tamaño del espacio $H$?  
ii. Calcule el espacio de versiones.  
iii. ¿Qué respuesta daría a las siguientes instancias?

| # | Cielo | Temp | Humedad | Viento | Tmp. Agua | Tiempo | Juega |
| :-: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 5 | Soleado | Templado | Normal | Fuerte | Fría | Cambiante | ? |
| 6 | Lluvioso | Frío | Normal | Suave | Templada | Sin cambios | ? |
| 7 | Soleado | Templado | Normal | Suave | Templada | Sin cambios | ? |
| 8 | Soleado | Frío | Normal | Fuerte | Templada | Sin cambios | ? |

---

### Ejercicio 3
Considere para el ejercicio anterior un espacio cuyas hipótesis tienen la siguiente forma: 
$$\langle x, x, x, x, x, x \rangle \lor \langle x, x, x, x, x, x \rangle$$

*Por ejemplo:* $h: \langle ?, \text{Frío}, \text{Alto}, ?, ?, ? \rangle \lor \langle \text{Soleado}, ?, \text{Alto}, ?, ?, \text{Sin cambios} \rangle$

a) ¿Cuál es el tamaño del espacio de hipótesis?  
b) Calcule el espacio de versiones.

---

### Ejercicio 4
a) Implemente el algoritmo FIND-S para el problema de cuándo Pedro salva un examen.  
b) Verifique su algoritmo contra el ejemplo visto en el teórico.  
c) Implemente un programa que genere instancias aleatorias, y luego las clasifique de acuerdo al concepto: 
$$\langle ?, \text{Media}, ?, ?, ? \rangle$$
¿Cuántos ejemplos únicos (sin repetidos) tiene que generar en promedio para aprender el concepto? ¿Cuántos ejemplos únicos positivos?

---

### Ejercicio 5
Pruebe el teorema de la representación del espacio de versiones.

---

### Ejercicio 6
Considere un espacio compuesto de puntos en el plano entero, y un conjunto de hipótesis formadas por rectángulos:
$$H = \{ a \le x \le b, \; c \le y \le d \mid a, b, c, d \in \mathbb{N} \}$$

Dados los siguientes ejemplos:

```text
  y ^
    |                               
    |               -               
    |                               
    |       -                       
  5 +                       +       
    |               +               -
    |   -           +               
    |                               
    |               -               
    +---+---+---+---+---+---+---+---+---> x
    0               5               
```

i. Encuentre los conjuntos $S$ y $G$. Dibújelos en el diagrama.  
ii. Si el alumno pudiera elegir el siguiente ejemplo para su entrenamiento, ¿cuál le convendría elegir? ¿Cuál seguramente no?  
iii. Si ud. desea enseñar el concepto $(3 \le x \le 5, \; 2 \le y \le 9)$: ¿cuál es la mínima cantidad de ejemplos que ud. debería dar?

---

### Ejercicio 7
Se desea aprender un concepto que se supone es un triángulo rectángulo isósceles en el semiplano $\mathbb{R}^+ \times \mathbb{R}^+$, de la siguiente forma:

```text
  y ^
    |
  a | \
    |  \
    | + \
    +----+---> x
    0    a

    a ∈ N⁺ ∪ {∞}
```

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

### Ejercicio 8
Considere un espacio cuyas hipótesis son, en lugar de conjunciones, disyunciones de restricciones sobre los atributos. Así, por ejemplo, la hipótesis que representa que Pedro juega cuando el viento es suave o cuando está soleado es: 
$$\langle \text{Soleado}, \emptyset, \emptyset, \text{Suave}, \emptyset, \emptyset \rangle$$

a) Calcule la cantidad de posibles hipótesis sintáctica y semánticamente distintas.  
b) Especifique cómo son las reglas de generalización y especificación mínimas para este nuevo espacio.  
c) Aplique paso a paso el algoritmo de cálculo de $VS_{H,D}$, siendo $D$ el conjunto formado por los dos primeros ejemplos del ejercicio 2.  
d) Repita el paso previo considerando ahora únicamente a los ejemplos #3 y #4.
