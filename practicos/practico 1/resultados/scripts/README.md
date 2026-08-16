# Scripts Ejecutables - Práctico 1

Implementaciones en Python de algoritmos y simulaciones correspondientes al **Práctico 1 (Aprendizaje Conceptual)**:

---

## 📂 Contenido del Directorio

* 🐍 [**`ejercicio_04_find_s.py`**](./ejercicio_04_find_s.py):
  * Implementación del algoritmo **Find-S**.
  * Verificación con los datos teóricos de Pedro.
  * Simulación Monte Carlo ($10.000$ iteraciones) para estimar el número promedio de ejemplos únicos necesarios para aprender $\langle ?, \text{Media}, ?, ?, ? \rangle$.
  * *Uso:* `python ejercicio_04_find_s.py`

* 🐍 [**`ejercicio_02_candidate_elimination.py`**](./ejercicio_02_candidate_elimination.py):
  * Implementación del algoritmo **Candidate-Elimination**.
  * Traza paso a paso de las fronteras $S$ y $G$ con el dataset de fútbol playa de Pedro.
  * Clasificación automática de las instancias de test #5 a #8.
  * *Uso:* `python ejercicio_02_candidate_elimination.py`

---

### 🚀 Cómo Ejecutar

Desde la terminal en el directorio raíz o en `scripts/`:

```bash
# Activar entorno virtual si está disponible
.\venv\Scripts\Activate.ps1

# Ejecutar el script del Ejercicio 4
python "practicos/practico 1/resultados/scripts/ejercicio_04_find_s.py"

# Ejecutar el script del Ejercicio 2
python "practicos/practico 1/resultados/scripts/ejercicio_02_candidate_elimination.py"
```
