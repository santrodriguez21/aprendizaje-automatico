# Aprendizaje Automático — 2026
## Tarea 1: Predicción de resultados del fútbol uruguayo

---

### Objetivos del laboratorio
- **a)** Aplicar herramientas metodológicas sobre datos reales.
- **b)** Implementar y aplicar métodos de aprendizaje supervisado para predecir resultados de partidos de fútbol.
- **c)** Analizar críticamente los resultados obtenidos.

---

## 1. Descripción del Problema

El objetivo es predecir el resultado de un partido de fútbol entre tres valores posibles:
- **`L`**: Gana el equipo local.
- **`V`**: Gana el equipo visitante.
- **`E`**: Hay empate.

Para ello se utilizará el conjunto de datos construido por [Mart Jürisoo](https://github.com/martj42/international_results) de resultados de partidos de fútbol internacional, restringido a los partidos del **fútbol uruguayo entre 1932 y 2025** (`futbol_uruguayo.csv`).

---

## 2. Preprocesamiento

Aplique herramientas adecuadas sobre el dataset provisto para:
1. **Limpieza:** Limpiar los datos, descartar o corregir anomalías.
2. **Valores faltantes:** Completar o imputar valores nulos/faltantes con criterios justificados.
3. **Transformaciones:** Realizar codificaciones, normalizaciones y discretizaciones.
4. **Duplicados:** Eliminar registros duplicados y aplicar cualquier otro procedimiento necesario.

> [!NOTE]
> - No es obligatorio utilizar todos los atributos provistos.
> - Se permite y alienta la ingeniería de atributos (*feature engineering*): crear nuevos atributos calculados (por ejemplo: rachas, goles promedio recientes, historial directo *head-to-head*, diferencia de goles, etc.) o incorporar atributos externos.
> - Construya un pipeline de procesamiento **completamente reproducible** (se recomienda la clase `Pipeline` de `scikit-learn`).

---

## 3. Modelos Supervisados a Implementar

Debe implementar clasificadores para predecir la variable objetivo `ganador` $\in \{'L', 'V', 'E'\}$:

### A. Implementaciones Propias (desde cero):
1. **Árbol de Decisión:**
   - Incorporar el hiperparámetro `min_info_gain` que detenga la recursión cuando ningún atributo supere una ganancia mínima de información especificada.
2. **Naïve Bayes:**
   - Incorporar el hiperparámetro $m$ correspondiente al tamaño equivalente de muestra ($m$-estimador para suavizado de probabilidades).
3. **Clasificador Base (*Baseline*):**
   - Un clasificador heurístico que siempre prediga como ganador al equipo que tenga una mayor proporción de partidos ganados en general durante los últimos 10 años.

### B. Modelos de Referencia (`scikit-learn`):
- **Random Forest Classifier** (`sklearn.ensemble.RandomForestClassifier`)
- **Naïve Bayes** (`sklearn.naive_bayes.GaussianNB` o variantes categóricas)

---

## 4. Experimentación y Validación

### Partición Temporal de Datos:
- **Conjunto de Entrenamiento (*Train*):** Partidos jugados hasta el año **2023 inclusive** (1932 – 2023).
- **Conjunto de Evaluación / Test (*Test*):** Partidos jugados en los años **2024 y 2025**.

```
[=================== ENTRENAMIENTO (1932 - 2023) ===================] [== EVALUACIÓN (2024 - 2025) ==]
```

### Ajuste de Hiperparámetros (Validación Cruzada):
- Al tratarse de **series temporales / datos con orden cronológico**, se debe prestar especial atención a la estrategia de partición para evitar *data leakage* (investigar e implementar métodos adecuados como *Time Series Split* o validación por ventanas expansivas / rodantes).
- Comparar el desempeño al variar los hiperparámetros (`min_info_gain`, $m$, etc.) y presentar **gráficas de evolución del error/rendimiento**.

### Evaluación Final y Métricas:
Reentrenar los modelos con sus mejores hiperparámetros sobre todo el conjunto de entrenamiento (hasta 2023) y evaluarlos sobre el conjunto de test (2024–2025):
- **Métricas Globales:** *Accuracy* y **Macro-$F_1$** (métrica principal).
- **Métricas por Clase:** Precisión, *Recall* y $F_1$-score para cada resultado (`L`, `V`, `E`).
- **Matriz de Confusión:** Matriz $3 \times 3$ para cada modelo evaluado.
- **Análisis Cualitativo:** Describir en qué escenarios funciona mejor cada modelo y en cuáles tiende a equivocarse (ej. predicción de empates, partidos clásicos, equipos recién ascendidos).

---

## 5. Entregables

1. **Código Fuente:** Implementaciones de los clasificadores y pipelines.
2. **Jupyter Notebook:** Archivo autocontenido que lea el dataset, ejecute el preprocesamiento, entrene los modelos, realice la validación cruzada y presente las predicciones y gráficos.
3. **Informe en formato IEEE:** Artículo en plantilla [IEEE Conference Format](https://www.ieee.org/conferences/publishing/templates) de **hasta 5 páginas** describiendo la metodología, pruebas realizadas, discusión de resultados y conclusiones.

> [!IMPORTANT]
> - **Autocontenido:** La solución debe ser reproducible de punta a punta. No se aceptarán archivos intermedios o procesamientos parciales externos.
> - **Entorno:** Python 3.12 y scikit-learn 1.9 (fijar semillas aleatorias para garantizar reproducibilidad).
> - **Fecha límite de entrega:** **Lunes 21 de septiembre de 2026 a las 23:59**.

---

## 6. Pautas sobre el Uso de Inteligencia Artificial

Siguiendo la *Guía para el uso ético y crítico de IA* de la Facultad de Ingeniería:
- **Categoría 3 (Uso extensivo):** Se permite el uso de IA como herramienta profesional asistida.
- **Compromiso:** Declarar explícitamente el uso de herramientas de IA, comprender a fondo el código generado, juzgar críticamente sus resultados y mantener buenas prácticas de programación y documentación clara.

---

## 7. Política de Días Extra

- Cada grupo dispone de un total de **4 días extra** acumulables para administrar libremente entre los dos laboratorios del semestre.
- Deben solicitarse al equipo docente **antes** del vencimiento de la fecha límite formal de entrega.
