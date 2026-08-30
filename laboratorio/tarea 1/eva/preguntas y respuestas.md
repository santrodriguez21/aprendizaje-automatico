Aviso 1:

Estimad@s, en la página de gitlab del curso (https://gitlab.fing.edu.uy/aprendaut2/aa-26) quedaron unos Jupyter Notebooks con unos breves tutoriales sobre algunas de las herramientas que pueden utilizar para la tarea. También hay un ejemplo de informe como para que tengan una referencia (y solamente para eso, no es un "fill in the blanks").

Pregunta 1:

Respecto al uso del encoder, el fit del encoder debería de hacerse solo sobre el conjunto de entrenamiento cierto ? (es decir, no considerar las instancias con fecha 2024/2025 ya que ese es el conjunto de evaluación)

Respuesta 1:

Sí. El fit siempre es sobre train, la evaluación siempre asume que las instancias sobre las que evaluás no fueron vistas en el entrenamiento. Revisen el teórico de metodología.

Pregunta 2:

Se pueden usar las funciones disponibles de scikit-learn para hacer validación cruzada, ya que vi que tienen eso implementado. Por lo tanto, adaptando el clasificador que construimos se puede hacer llamadas a esas funciones, o esperan que nosotros hagamos mismo una implementación para eso ?

Respuesta 2:

Sí, de hecho sugerimos que lo hagan.

Pregunta 3:

Respecto a validación cruzada para determinar el valor del hiperparametro, primero se deberían tener definidos todos los atributos que vayamos a usar no? Porque esto va a ser dependiente del dominio que tengamos de los atributos para posteriormente ver el valor del hiperparametro

Respuesta 3:

Sí y no. Parte del ajuste podría ser elegir qué atributos usar (vean la parte de feature selection), pero deberían tener un conjunto de atributos definido sobre los que probar.

Pregunta 4:

Tengo una duda sobre el clasificador base. El mismo predice al ganador de un partido según cual tenga una mayor proporción de partidos ganados en general en los
últimos diez años. Mi duda es: Una vez este clasificador predice un partido, ¿El resultado real de ese partido se usa para recalcular dicha proporción dejando fuera los resultados que ya no entren en la ventana de los 10 años para el siguiente partido? ¿o, por el contrario, la proporción se congela para cada equipo para todos los partidos del subconjunto de partidos de evaluación? La misma duda tengo sobre cualquier atributo calculado que deseemos agregar.

Respuesta 4:

Piensen en la evaluación como el modelo funcionando en "el mundo real". Si ustedes van a predecir el resultado de cada partido del próximo fin de semana, ahí tienen la información histórica completa (aunque no, por supuesto, el futuro). Por lo tanto, todos los partidos jugados en los últimos diez años, aún aquellos que aparecen en el conjunto de evaluación, pueden utilizarse para el clasificador. Es decir, que el resultado real sí puede utilizarse para predecir otros partidos (un concepto parecido a este se utiliza al entrenar redes neuronales, y se llama "teacher forcing").

En la clase de metodología: veremos que el conjunto de evaluación, a diferencia del de entrenamiento, utiliza los ejemplos uno a uno, para poder obtener estadísticas de acierto o error, a diferencia del de train, donde queremos características generales del conjunto que nos permita construir un modelo.

Pregunta 5

La letra indica que “la solución tiene que ser autocontenida: no se aceptarán archivos de procesamiento parciales como parte de la entrega”. Queríamos consultar si esto refiere exclusivamente a evitar datasets o artefactos intermedios precalculados (es decir, que todo el flujo de carga, preprocesamiento y entrenamiento debe ejecutarse de punta a punta desde el dataset original), o si también restringe la modularización del código. En particular, ¿es válido estructurar funciones auxiliares o clases en módulos .py separados e importarlos en el Jupyter Notebook, o se espera que todo el código resida estrictamente dentro del propio notebook?

Respuesta 5:

Lo que quiere decir es que lo que entreguen debería poder evaluarse sin necesidad de ejecutar código y que, de ser necesario hacerlo, todo lo necesario está en la entrega (y no aparecen cosas como "descargar el archivo tal del sitio www.pepito.org" o cosas así). No solamente debe poder ejecutarse de punta a punta, sino que debe estar ejecutado en la entrega.

Pregunta 6:

Respecto al clasificador base, queríamos confirmar si entendimos bien cómo encararlo: ¿la idea es que sea simplemente una regla fija que calcule las proporciones de victorias de los últimos 10 años y elija al que tenga mayor porcentaje (sin usar ningún modelo de aprendizaje), o se espera algún otro enfoque? 

Respuesta 6:

Sí, es eso. Podría considerarse un método de aprendizaje muy sencillo (generalmente el término "modelo" lo usamos como sinónimo de "hipótesis").