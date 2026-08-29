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
| **$\text{Ganancia}(S, A)$** | $\text{Ent}(S) - \sum_{v \in \text{Val}(A)} \frac{\|S_v\|}{\|S\|} \text{Ent}(S_v)$ | **Ganancia de Información:** Reducción esperada en la entropía al particionar por el atributo $A$. |
| **$\text{SplitInformation}(S, A)$** | $-\sum_{v \in \text{Val}(A)} \frac{\|S_v\|}{\|S\|} \log_2\left(\frac{\|S_v\|}{\|S\|}\right)$ | Entropía intrínseca de la partición del atributo $A$ (mide cuántas ramas genera). |
| **$\text{GainRatio}(S, A)$** | $\frac{\text{Ganancia}(S, A)}{\text{SplitInformation}(S, A)}$ | **Tasa de Ganancia:** Criterio alternativo que penaliza atributos con muchos valores únicos. |
| **$\text{min\_info\_gain}$** | Hiperparámetro $\ge 0$ | Umbral de parada temprana (*pre-pruning*); detiene la recursión si la ganancia no supera el umbral. |
| **Atributos Continuos** | Umbral $c = \frac{v_i + v_{i+1}}{2}$ | Discretización dinámica probando puntos de corte medios entre cambios de clase adyacentes. |
| **Sobreajuste (*Overfitting*)** | $\text{error}_{\text{train}}(h) < \text{error}_{\text{train}}(h')$ y $\text{error}_D(h) > \text{error}_D(h')$ | El modelo memoriza el ruido del conjunto de entrenamiento y pierde capacidad de generalización. |
| **Poda Reducida (*Reduced Error Pruning*)** | Post-poda con validación | Reemplaza un subárbol por una hoja si la exactitud sobre el conjunto de validación no disminuye. |
| **Algoritmo ID3** | Top-Down voraz sin backtracking | Construye el árbol eligiendo recursivamente el atributo con mayor $\text{Ganancia}(S, A)$. |

---

## 🔮 4. Aprendizaje Bayesiano y Naïve Bayes (Clase 4)

| Símbolo / Término | Definición / Notación | Significado / Contexto de la Clase |
| :--- | :--- | :--- |
| **Teorema de Bayes** | $P(h \mid D) = \frac{P(D \mid h) P(h)}{P(D)}$ | Actualiza la probabilidad de una hipótesis $h$ a la luz de los datos observados $D$. |
| **$P(h)$ (Probabilidad a Priori)** | Probabilidad inicial | Conocimiento o creencia previa sobre la verosimilitud de la hipótesis $h$ antes de ver $D$. |
| **$P(D \mid h)$ (Verosimilitud / Likelihood)** | Probabilidad de los datos | Probabilidad de observar los datos $D$ bajo el supuesto de que la hipótesis $h$ es verdadera. |
| **$P(D)$ (Probabilidad Marginal)** | $\sum_{h_i \in H} P(D \mid h_i) P(h_i)$ | Factor de normalización constante independiente de la hipótesis $h$. |
| **$P(h \mid D)$ (Probabilidad a Posteriori)** | Probabilidad actualizada | Grado de certeza sobre $h$ una vez incorporada la evidencia de los datos $D$. |
| **Hipótesis MAP ($h_{\text{MAP}}$)** | $\arg\max_{h \in H} P(D \mid h) P(h)$ | **Máximo a Posteriori:** Hipótesis más probable del espacio $H$ dados los datos $D$. |
| **Hipótesis ML ($h_{\text{ML}}$)** | $\arg\max_{h \in H} P(D \mid h)$ | **Máxima Verosimilitud:** Hipótesis que maximiza la probabilidad de los datos observados (asume priors uniformes). |
| **Clasificador Bayesiano Sencillo (Naïve Bayes / CBS)** | $c_{\text{NB}} = \arg\max_{c_j} P(c_j) \prod_{i=1}^n P(a_i \mid c_j)$ | Asume independencia condicional de los atributos dada la clase $c_j$. |
| **Suposición de Independencia Condicional** | $P(a_1, \dots, a_n \mid c) = \prod_{i=1}^n P(a_i \mid c)$ | Simplificación fundamental de Naïve Bayes que reduce exponencialmente la cantidad de parámetros a estimar. |
| **$m$-estimador de Probabilidad** | $\hat{P}(a_i \mid c) = \frac{n_c + m \cdot p}{n + m}$ | Técnica de suavizado para evitar probabilidades nulas ($0$). $m$ = peso de la muestra virtual, $p$ = prior uniforme ($1/k$). |
| **Suavizado de Laplace** | $m = k = \|\text{Val}(A)\|$, $p = \frac{1}{k}$ | Caso particular del $m$-estimador que suma $+1$ a cada conteo: $\hat{P} = \frac{n_c + 1}{n + k}$. |
| **Inferencia Logarítmica** | $\arg\max_{c} \left[ \log P(c) + \sum_{i} \log P(a_i \mid c) \right]$ | Transforma productos en sumas para evitar el desbordamiento por subflujo numérico (*underflow*). |
| **Clasificador Bayesiano Óptimo (BOC)** | $\arg\max_{v_j \in V} \sum_{h_i \in H} P(v_j \mid h_i) P(h_i \mid D)$ | Combina las predicciones de todas las hipótesis ponderadas por $P(h_i \mid D)$. Maximiza la probabilidad de acierto. |

---

## 🧠 5. Sesgo Inductivo y Principios de Búsqueda (Clases 2, 3 y 4)

| Símbolo / Término | Definición / Notación | Significado / Contexto de la Clase |
| :--- | :--- | :--- |
| **$B$ (Sesgo Inductivo)** | $(B \land D \land x_i) \vdash L(D, x_i)$ | Conjunto mínimo de suposiciones que junto a $D$ permite deducir la clasificación de $x_i$. |
| **Sesgo Preferencial** | Preferencia de búsqueda | El espacio $H$ es completo (contiene todas las funciones), pero el algoritmo prefiere unas sobre otras (ej. ID3 prefiere árboles más cortos; FIND-S prefiere la más específica). |
| **Sesgo Restrictivo** | Restricción del lenguaje | El espacio $H$ es incompleto a priori (ej. Candidate-Elimination solo permite conjunciones; Regresión Lineal solo hiperplanos). |
| **Navaja de Ockham** | Principio de parsimonia | *"Cuando se ofrecen varias explicaciones, es preferible la más simple que se ajuste a los datos."* (William de Ockham, S.XIV). |

---

## 📊 6. Métricas de Evaluación y Validación Estadística (Clases 1 a 5)

| Símbolo / Término | Definición / Notación | Significado / Contexto de la Clase |
| :--- | :--- | :--- |
| **Matriz de Confusión** | $\begin{pmatrix} \text{VP} & \text{FN} \\ \text{FP} & \text{VN} \end{pmatrix}$ | Tabla cruzada entre valores reales y predicciones del modelo (binaria o $K \times K$ multiclase). |
| **Acierto / Exactitud (*Accuracy*)** | $\frac{\text{VP} + \text{VN}}{\text{Total}}$ | Proporción de predicciones correctas sobre el total. Engañosa y poco informativa con clases desbalanceadas. |
| **Precisión ($P$)** | $\frac{\text{VP}}{\text{VP} + \text{FP}}$ | Fracción de instancias predichas como positivas que realmente lo son. |
| **Exhaustividad / Sensibilidad (*Recall* / $R$)** | $\frac{\text{VP}}{\text{VP} + \text{FN}}$ | Fracción de instancias reales positivas que el modelo logró recuperar/detectar. |
| **Medida $F_\beta$** | $\frac{(1 + \beta^2) P \cdot R}{\beta^2 P + R}$ | Media armónica ponderada; $\beta$ modula la importancia relativa del Recall respecto a la Precisión. |
| **Medida $F_1$ (*F1-Score*)** | $2 \cdot \frac{P \cdot R}{P + R} = \frac{2\text{VP}}{2\text{VP} + \text{FP} + \text{FN}}$ | Caso balanceado ($\beta=1$); media armónica entre Precisión y Recall. |
| **Macro-Average** | $\frac{1}{K} \sum_{k=1}^K M_k$ | Promedio aritmético simple de la métrica sobre las $K$ clases (trata a todas las clases por igual, ideal para evaluar clases minoritarias). |
| **Micro-Average** | $\frac{\sum \text{VP}_k}{\sum (\text{VP}_k + \text{FP}_k)}$ | Agregación global de aciertos y errores sumando todas las instancias. En multiclase exclusivo coincide con el *Accuracy*. |
| **Curva Precision-Recall (PR)** | Curva $P$ vs $R$ | Evolución de la Precisión en función del Recall al variar el umbral continuo de decisión $\theta \in [0, 1]$. |
| **Área bajo la curva PR / AP** | *Average Precision* | Cuantifica la solidez global del clasificador a lo largo de todos los umbrales posibles (área bajo la curva PR). |
| **Índice de Jaccard (IoU)** | $IJ(A, B) = \frac{\|A \cap B\|}{\|A \cup B\|}$ | Métrica por instancia para problemas **multietiqueta** (*Multi-label*); mide la proporción de solapamiento entre etiquetas reales y predichas. |
| **Error en la Muestra ($error_S(h)$)** | $\frac{1}{n} \sum \delta(y, h(x))$ | Frecuencia observada de errores de la hipótesis $h$ sobre la muestra $S$ de tamaño $n$. Es un estimador insesgado de $error_D(h)$. |
| **Error Real / Poblacional ($error_D(h)$)** | $P_{x \sim \mathcal{D}}(y \ne h(x))$ | Probabilidad de que $h$ clasifique erróneamente una nueva instancia aleatoria de la distribución $\mathcal{D}$. |
| **Intervalo de Confianza al 95%** | $error_S(h) \pm 1.96 \sqrt{\frac{error_S(1-error_S)}{n}}$ | Rango de valores donde reside el error real con $95\%$ de certeza (aproximación normal de la binomial según Mitchell Cap. 5). |
| **Línea Base (*Baseline*)** | Modelo de referencia mínimo | Rendimiento mínimo que cualquier modelo útil debe superar (ej. clasificador mayoritario *Zero-Rule* o asignación aleatoria). |
| **Línea de Tope (*Ceiling / Bayes Error*)** | Límite superior alcanzable | Cota superior teórica del rendimiento (desempeño humano experto o error irreducible de Bayes por solapamiento probabilístico). |
| **Validación Cruzada $k$-fold** | Partición en $k$ bloques disjuntos | Divide el dataset en $k$ partes; entrena en $k-1$ y valida en la restante rotativamente, reportando media y varianza ($\mu \pm \text{sem}$). |
| **Muestreo Estratificado** | Mantiene proporciones de clase | Fuerza que cada partición (*fold*, *train*, *test*) preserve exactamente la distribución porcentual original de cada clase. |

---

## 🛠️ 7. Metodología, Preprocesamiento e Ingeniería de Atributos (Clase 5)

| Símbolo / Término | Definición / Notación | Significado / Contexto de la Clase |
| :--- | :--- | :--- |
| **Fuga de Información (*Data Leakage*)** | Contaminación de datos | Utilizar información del conjunto de prueba/validación para calcular transformaciones o estadísticos durante el preprocesamiento o entrenamiento. |
| **Regla contra Data Leakage** | `fit` solo en Train | Cualquier cálculo de medias, medianas, escalas o vocabularios **debe realizarse exclusivamente sobre el conjunto de entrenamiento**. |
| **Imputación de Faltantes** | Media, mediana, moda o centinela | Estrategias para sustituir valores nulos (`NaN`): media/mediana para continuos, moda para categóricos o códigos de advertencia (`UNK`). |
| **Codificación Ordinal / Label Encoding** | $c_j \to \{0, \dots, k-1\}$ | Asigna enteros consecutivos a categorías. Solo válido para variables ordinales con jerarquía real, riesgoso en variables nominales puras. |
| **One-Hot Encoding (OHE)** | $k$ columnas binarias ($0/1$) | Genera un atributo dummy por cada categoría. Evita inducir orden métrico artificial en atributos nominales. |
| **Bolsa de Palabras (BoW)** | Vector de dimensión $\|V\|$ | Representación de texto en base a frecuencia de términos (binario, conteo absoluto o frecuencia relativa normalizada). |
| **TF-IDF** | $\text{tf}(w,d) \cdot \log\left(\frac{N}{n_w}\right)$ | Ponderación que combina la frecuencia local en el documento con la rareza global en el corpus. Destaca palabras clave distintivas. |
| **N-gramas (*Bag-of-Ngrams*)** | Secuencias de $n$ palabras | Captura contexto y orden léxico local contiguo (ej. bi-gramas `"no funciona"`, tri-gramas `"árbol de decisión"`). |
| **Word Embeddings** | Vectores densos $\mathbb{R}^d$ ($d \approx 50\text{--}300$) | Representaciones continuas de baja dimensionalidad aprendidas por contexto semántico; resuelven la alta dispersión de BoW. |
| **Escalado Min-Max** | $x_s = \frac{x - x_{\min}}{x_{\max} - x_{\min}}$ | Transforma atributos numéricos al intervalo acotado $[0, 1]$. Sensible a valores atípicos (*outliers*). |
| **Estandarización Z-Score** | $x_{\text{norm}} = \frac{x - \mu}{\sigma}$ | Centra la variable en $\mu = 0$ con dispersión $\sigma = 1$. Crucial para k-NN, SVM, Descenso por Gradiente y PCA. |
| **Random Oversampling / Undersampling** | Remuestreo de clases | Duplicación aleatoria con reemplazo de la clase minoritaria (oversampling) o descarte aleatorio de la mayoritaria (undersampling). |
| **Algoritmo SMOTE** | $x_i + \lambda (x_{zi} - x_i)$ | *Synthetic Minority Over-sampling Technique:* Genera instancias sintéticas plausibles por interpolación lineal entre vecinos $k$-NN. |
| **Algoritmo NearMiss** | Selección de prototipos | Submuestreo de la clase mayoritaria conservando solo aquellos ejemplos más cercanos a la frontera con la clase minoritaria. |
| **Métodos de Filtrado (*Filter*)** | Univariados sin modelo | Selección de atributos previa al modelado mediante pruebas estadísticas independientes ($\chi^2$, Umbral de Varianza, Información Mutua). |
| **Métodos Envolventes (*Wrappers*)** | Búsqueda guiada por modelo | Evalúan subconjuntos sucesivos de atributos entrenando iterativamente un algoritmo de aprendizaje (ej. *Recursive Feature Elimination* - RFE). |
| **Métodos Embebidos (*Embedded*)** | Selección intrínseca | La selección de atributos ocurre de manera natural dentro del algoritmo durante el ajuste (ej. divisiones en árboles de decisión, penalización L1 Lasso). |
| **GridSearchCV / RandomizedSearchCV** | Optimización de hiperparámetros | Búsqueda exhaustiva sobre una grilla discreta (*Grid*) o muestreo aleatorio probabilístico sobre distribuciones (*Randomized*). |
| **Pipeline y ColumnTransformer** | Ensamblado modular en Scikit-Learn | Encapsula transformaciones heterogéneas por tipo de columna y el estimador final, garantizando reproducibilidad y ausencia de *data leakage*. |

