# Ejercicio 1: Fundamentos y Definición $(T, P, E)$

**Práctico 1: Introducción y Aprendizaje Conceptual**  
**Curso:** Aprendizaje Automático

---

## Enunciado

### a)
Dé dos ejemplos en los cuales las técnicas de Aprendizaje Automático sean útiles y dos en los cuales no lo sean. Dé una breve justificación en cada caso.

### b)
Elija una aplicación que considere interesante. Descríbala informalmente, y luego especifique lo más precisamente posible la tarea, la medida de performance, y la descripción de la función objetivo.

---

## Solución Detallada

### Parte a) Ámbito de Aplicabilidad del Aprendizaje Automático

#### 1. Casos donde el Aprendizaje Automático es ÚTIL:

* **Ejemplo 1: Diagnóstico médico por imágenes (Detección de patologías en radiografías / resonancias):**
  * *Justificación:* Los seres humanos (radiólogos expertos) pueden reconocer patrones visuales sutiles basados en años de experiencia, pero es prácticamente imposible especificar un conjunto determinista de reglas lógicas o condicionales `if-else` que cubra todas las variaciones anatómicas, niveles de ruido en la captura y formas de las lesiones. El Aprendizaje Automático permite generalizar a partir de miles de imágenes anotadas (*Ground Truth*).

* **Ejemplo 2: Detección de transacciones fraudulentas en tiempo real (Fintech / Tarjetas de crédito):**
  * *Justificación:* El entorno es altamente dinámico y adversarial. Los defraudadores cambian constantemente sus estrategias y patrones de ataque. Un sistema estático de reglas fijas queda obsoleto rápidamente, mientras que un modelo de aprendizaje automático puede actualizarse continuamente con nuevos flujos de datos para capturar comportamientos anómalos.

#### 2. Casos donde el Aprendizaje Automático NO es ÚTIL:

* **Ejemplo 1: Liquidación de nóminas salariales o cálculo de impuestos según la ley:**
  * *Justificación:* El problema es completamente determinista y está regido por un conjunto explícito, finito y no ambiguo de normativas legales y tablas aritméticas. No existe incertidumbre, generalización inductiva ni aprendizaje a partir de ejemplos: una implementación de software tradicional garantiza un resultado exacto y auditable con $0\%$ de error.

* **Ejemplo 2: Ordenamiento de un arreglo numérico o cálculo de rutas más cortas en grafos estáticos:**
  * *Justificación:* Existen algoritmos clásicos deterministas óptimos (como *MergeSort*, *Quicksort* o *Dijkstra*) con garantías formales de corrección y complejidad computacional óptima ($O(n \log n)$, $O(V \log V + E)$). Un enfoque probabilístico o aproximado por ML sería innecesariamente impreciso, costoso e ineficiente.

---

### Parte b) Formalización de una Aplicación $(T, P, E)$

#### Aplicación Elegida: Sistema de Recomendación Personalizada de Contenido Multimedia (ej. Spotify / Netflix)

#### 1. Descripción Informal:
El sistema sugiere a cada usuario una lista ordenada de películas o canciones que probablemente le gusten, basándose en su historial de visualizaciones/reproducciones previas, calificaciones pasadas, preferencias de género y la similitud con usuarios de gustos afines (*Filtrado Colaborativo y Basado en Contenido*).

#### 2. Especificación Formal $(T, P, E)$:

* **Tarea ($T$):**  
  Para un usuario $u \in \mathcal{U}$ y un ítem $i \in \mathcal{I}$, predecir la calificación o nivel de agrado estimado $\hat{y}_{u,i} \in [1, 5]$ que el usuario otorgaría al ítem no visto, y generar un ranking de los $K$ ítems con mayor puntuación esperada:
  $$\text{Top-}K(u) = \arg\max_{i \in \mathcal{I} \setminus \mathcal{I}_u}^K \hat{y}_{u,i}$$

* **Medida de Desempeño ($P$):**  
  * Para la predicción de calificaciones: **Raíz del Error Cuadrático Medio (*RMSE*)** sobre un conjunto de prueba reservado $D_{\text{test}}$:
    $$\text{RMSE} = \sqrt{\frac{1}{|D_{\text{test}}|} \sum_{(u, i) \in D_{\text{test}}} (y_{u,i} - \hat{y}_{u,i})^2}$$
  * Para la calidad del ranking recomendado: **Precisión en los primeros $K$ (*Precision@K*)** y **Ganancia Acumulada Descontada Normalizada (*NDCG@K*)**:
    $$\text{Precision@}K(u) = \frac{|\text{Ítems relevantes en Top-}K|}{K}$$

* **Experiencia ($E$):**  
  Conjunto histórico de interacciones usuario-ítem:
  $$E = \{ (u, i, y_{u,i}, t) \mid u \in \mathcal{U}, i \in \mathcal{I}, y_{u,i} \in [1, 5], t \in \text{Timestamp} \} \cup \text{Metadatos de usuarios e ítems}$$

* **Función Objetivo ($V$):**  
  $$V: \mathcal{U} \times \mathcal{I} \longrightarrow \mathbb{R}$$
  que asigna a cada par $(\text{usuario}, \text{ítem})$ un valor escalar de preferencia real o probabilidad de consumo.
