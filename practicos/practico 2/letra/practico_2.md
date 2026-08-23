# Aprendizaje Automático
## Práctico 2: Árboles de Decisión

---

## Ejercicio 1

Dé árboles de decisión que representen las siguientes funciones booleanas:

1. $p \land \neg q$
2. $p \oplus q$ ($p \text{ XOR } q$)
3. $p \lor (q \land r)$
4. $(p \land q) \lor (r \land s)$
5. $\neg (p \land q)$

---

## Ejercicio 2

Dado el siguiente conjunto de entrenamiento:

| # | $a_1$ | $a_2$ | Clasif |
|:---:|:---:|:---:|:---:|
| 1 | Verdadero | Verdadero | Sí |
| 2 | Verdadero | Verdadero | Sí |
| 3 | Verdadero | Falso | No |
| 4 | Falso | Falso | Sí |
| 5 | Falso | Verdadero | No |
| 6 | Falso | Verdadero | No |

- **a)** ¿Cuál es la entropía del conjunto de entrenamiento?
- **b)** ¿Cuál es la ganancia de particionar por cada uno de los atributos?

---

## Ejercicio 3

Volviendo al problema de aprender bajo qué condiciones a Pedro le gusta ir a jugar al fútbol a la playa:

| # | Cielo | Temp | Humedad | Viento | Tmp. Agua | Tiempo | Juega |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | Soleado | Templado | Normal | Fuerte | Templada | Sin cambios | Sí |
| 2 | Soleado | Templado | Alta | Fuerte | Templada | Sin cambios | Sí |
| 3 | Lluvioso | Frío | Alta | Fuerte | Templada | Cambiante | No |
| 4 | Soleado | Templado | Alta | Fuerte | Fría | Cambiante | Sí |

Donde:
- $\text{Cielo} \in \{\text{Soleado}, \text{Lluvioso}, \text{Nublado}\}$
- $\text{Temperatura} \in \{\text{Templado}, \text{Frío}\}$
- $\text{Humedad} \in \{\text{Normal}, \text{Alta}\}$
- $\text{Viento} \in \{\text{Fuerte}, \text{Suave}\}$
- $\text{Temp.Agua} \in \{\text{Templada}, \text{Fría}\}$
- $\text{Tiempo} \in \{\text{Sin cambios}, \text{Cambiante}\}$

- **a)** Halle el árbol de decisión utilizando el algoritmo ID3.
- **b)** Halle el árbol de decisión si ahora se agrega el siguiente ejemplo al conjunto de entrenamiento:

| # | Cielo | Temp | Humedad | Viento | Tmp. Agua | Tiempo | Juega |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 5 | Soleado | Templado | Normal | Suave | Templada | Sin cambios | No |

- **c)** ¿Qué respuesta daría a las siguientes instancias?

| # | Cielo | Temp | Humedad | Viento | Tmp. Agua | Tiempo | Juega |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 6 | Soleado | Templado | Normal | Fuerte | Fría | Cambiante | ? |
| 7 | Lluvioso | Frío | Normal | Suave | Templada | Sin cambios | ? |
| 8 | Soleado | Templado | Normal | Suave | Templada | Sin cambios | ? |
| 9 | Soleado | Frío | Normal | Fuerte | Templada | Sin cambios | ? |

- **d)** ¿Pertenece la solución al espacio de versiones obtenido con el algoritmo Candidate-Elimination en el práctico anterior? ¿Es esto siempre esperable?

---

## Ejercicio 4

Se desea construir un algoritmo para clasificar automáticamente la calidad de la fruta, de acuerdo a ciertas variables: color, tamaño, peso y mes de cosecha, y le proveen del siguiente conjunto de ejemplos:

| # | Color | Tamaño | Peso | Mes | Calidad |
|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | rojo | mediano | 200 | octubre | buena |
| 2 | rojo | grande | 150 | octubre | mala |
| 3 | rojo | mediano | 200 | noviembre | mala |
| 4 | rojo | mediano | 200 | — | buena |
| 5 | amarillo | grande | 150 | noviembre | buena |
| 6 | amarillo | mediano | 220 | noviembre | mala |

Donde:
- $\text{color} \in \{\text{amarillo}, \text{rojo}\}$
- $\text{tamaño} \in \{\text{grande}, \text{mediano}, \text{pequeño}\}$
- $\text{peso} \in [150, 250]$ (numérico continuo)
- $\text{mes} \in \{\text{octubre}, \text{noviembre}\}$
- $\text{calidad} \in \{\text{buena}, \text{mala}\}$

- **a)** Explique por qué no puede aplicar el algoritmo ID3 básico. Dé una solución a cada uno de los problemas encontrados.
- **b)** Dé un árbol de decisión a partir de los ejemplos dados, explicando su construcción paso a paso.

---

## Ejercicio 5

Se decide evitar el sobreajuste del modelo generado, modificando al ID3 para que, luego de construido el árbol, aplique un procedimiento de poda. 

El procedimiento consiste en evaluar a los nodos interiores, desde la raíz a las hojas, con un conjunto de validación. Cuando el resultado sobre el conjunto de validación es peor que simplemente predecir el valor más común de los ejemplos de entrenamiento en ese nodo, se elimina completamente el subárbol y se lo sustituye con una hoja con ese valor. En caso contrario, se procede a evaluar recursivamente a los nodos hijos.

Dé el árbol resultante de aplicar este método con los siguientes conjuntos de datos, donde las instancias 1 al 5 son de entrenamiento y el resto de validación:

| # | Cielo | Temp | Humedad | Viento | Tmp. Agua | Tiempo | Juega | Rol |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | Soleado | Templado | Normal | Fuerte | Templada | Sin cambios | Sí | Entrenamiento |
| 2 | Soleado | Templado | Alta | Fuerte | Templada | Sin cambios | Sí | Entrenamiento |
| 3 | Lluvioso | Frío | Alta | Fuerte | Templada | Cambiante | No | Entrenamiento |
| 4 | Soleado | Templado | Alta | Fuerte | Fría | Cambiante | Sí | Entrenamiento |
| 5 | Soleado | Templado | Normal | Suave | Templada | Sin cambios | No | Entrenamiento |
| 6 | Soleado | Templado | Normal | Fuerte | Fría | Suave | Sí | Validación |
| 7 | Lluvioso | Frío | Normal | Suave | Templada | Sin cambios | No | Validación |

---

## Ejercicio 6

Luego de ver árboles de decisión y aprendizaje conceptual, un alumno decide aplicar *‘lo mejor de ambos mundos’*: utiliza el algoritmo de Candidate-Elimination sobre el espacio de hipótesis de los árboles de decisión. 

- **a)** Encuentre los límites $S$ y $G$, luego de procesar los cuatro primeros ejemplos del ejercicio 3.
- **b)** ¿Es una buena opción la elegida por este alumno? ¿Por qué?
