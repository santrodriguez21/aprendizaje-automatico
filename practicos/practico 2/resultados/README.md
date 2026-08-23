# Resoluciones: Práctico 2 (Árboles de Decisión)

En este directorio se encuentran las soluciones detalladas, formalizaciones matemáticas, diagramas en Mermaid y scripts en Python para cada ejercicio del **Práctico 2**:

---

## 📑 Índice de Ejercicios

* 📄 [**`ejercicio_01.md`**](./ejercicio_01.md): Representación de funciones booleanas ($p \land \neg q$, $p \oplus q$, $p \lor [q \land r]$, $[p \land q] \lor [r \land s]$, $\neg [p \land q]$) mediante árboles de decisión mínimos.
* 📄 [**`ejercicio_02.md`**](./ejercicio_02.md): Cálculo formal paso a paso de la Entropía de Shannon $H(S) = 1{,}0$ y Ganancia de Información para los atributos $a_1$ ($0{,}0817$) y $a_2$ ($0{,}0000$).
* 📄 [**`ejercicio_03.md`**](./ejercicio_03.md): Inducción de árboles con el algoritmo ID3 sobre el dataset de Pedro juega al fútbol en la playa, agregado de nueva instancia, clasificación de instancias de test y comparación con el Espacio de Versiones $VS$.
* 📄 [**`ejercicio_04.md`**](./ejercicio_04.md): Extensiones de ID3 para clasificación de frutas: tratamiento de atributos continuos (`Peso` con punto de corte), valores faltantes (`Mes`) y manejo de ruido / inconsistencias.
* 📄 [**`ejercicio_05.md`**](./ejercicio_05.md): Algoritmo de post-poda de árboles basado en conjunto de validación (*Reduced Error Pruning*), evaluación de subárboles y árbol podado final.
* 📄 [**`ejercicio_06.md`**](./ejercicio_06.md): Análisis crítico de aplicar Candidate-Elimination sobre el espacio de árboles de decisión ($H_{\text{DT}}$): límites $S$ y $G$, futilidad del aprendizaje sin sesgo y explosión combinatoria ($2^{96}$).

---

### 💻 Scripts y Verificación
En la carpeta [**`scripts/`**](./scripts/) se encuentran implementaciones en Python para verificar y simular los ejercicios:
- 🐍 [**`ejercicio_02_entropia_ganancia.py`**](./scripts/ejercicio_02_entropia_ganancia.py)
- 🐍 [**`ejercicio_03_id3_pedro.py`**](./scripts/ejercicio_03_id3_pedro.py)
- 🐍 [**`ejercicio_05_poda_arbol.py`**](./scripts/ejercicio_05_poda_arbol.py)

---

### 📄 Enunciados
- 📄 [**`Letra en Markdown (letra/practico_2.md)`**](../letra/practico_2.md)
- 📑 [**`Letra original en PDF (letra/practico_2.pdf)`**](../letra/practico_2.pdf)
