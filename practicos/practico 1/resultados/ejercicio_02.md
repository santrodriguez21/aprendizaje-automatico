# Ejercicio 2: Aprendizaje Conceptual - Pedro Juega al Fútbol en la Playa

**Práctico 1: Introducción y Aprendizaje Conceptual**  
**Curso:** Aprendizaje Automático

---

## Enunciado

Se desea aprender bajo qué condiciones a Pedro le gusta ir a jugar al fútbol a la playa:

| # | Cielo | Temp | Humedad | Viento | Tmp. Agua | Tiempo | Juega |
| :-: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | Soleado | Templado | Normal | Fuerte | Templada | Sin cambios | Sí |
| 2 | Soleado | Templado | Alta | Fuerte | Templada | Sin cambios | Sí |
| 3 | Lluvioso | Frío | Alta | Fuerte | Templada | Cambiante | No |
| 4 | Soleado | Templado | Alta | Fuerte | Fría | Cambiante | Sí |

Con los siguientes posibles valores para cada atributo:
* **Cielo:** Soleado, Lluvioso, Nublado ($3$ valores)
* **Temperatura:** Templado, Frío ($2$ valores)
* **Humedad:** Normal, Alta ($2$ valores)
* **Viento:** Fuerte, Suave ($2$ valores)
* **Tmp.Agua:** Templada, Fría ($2$ valores)
* **Tiempo:** Sin cambios, Cambiante ($2$ valores)

### Preguntas:
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

## Solución Detallada

### 💻 Código Ejecutable en Python
Se incluye una implementación automática del algoritmo **Candidate-Elimination** que reproduce la traza y evalúa las instancias de test en:
* 🐍 [**`scripts/ejercicio_02_candidate_elimination.py`**](./scripts/ejercicio_02_candidate_elimination.py)

---

### Parte i) Tamaño del Espacio de Instancias ($|X|$) e Hipótesis ($|H|$)


#### 1. Espacio de Instancias ($|X|$):
$$|X| = |\text{Cielo}| \times |\text{Temp}| \times |\text{Humedad}| \times |\text{Viento}| \times |\text{TmpAgua}| \times |\text{Tiempo}|$$
$$|X| = 3 \times 2 \times 2 \times 2 \times 2 \times 2 = \mathbf{96 \text{ instancias posibles}}$$

#### 2. Hipótesis Sintácticamente Distintas ($|H_{\text{sintáctico}}|$):
Cada hipótesis conjuntiva $h = \langle a_1, a_2, a_3, a_4, a_5, a_6 \rangle$ admite para cada atributo sus valores discretos válidos más dos comodines:
* Un valor literal específico (ej. `Soleado`).
* El comodín `?` (acepta cualquier valor).
* El símbolo nulo $\emptyset$ (no acepta ningún valor).

Por lo tanto, la cantidad de opciones por atributo es $(\text{cantidad de valores} + 2)$:
$$|H_{\text{sintáctico}}| = (3+2) \times (2+2) \times (2+2) \times (2+2) \times (2+2) \times (2+2) = 5 \times 4^5 = 5 \times 1024 = \mathbf{5120}$$

#### 3. Hipótesis Semánticamente Distintas ($|H_{\text{semántico}}|$):
Cualquier hipótesis que contenga al menos un símbolo $\emptyset$ clasifica todas las instancias como negativas ($h(x) = 0, \forall x$). Por lo tanto, todas esas hipótesis son semánticamente equivalentes a una única hipótesis nula $h_\emptyset$:
$$|H_{\text{semántico}}| = 1 + (3+1) \times (2+1)^5 = 1 + 4 \times 3^5 = 1 + 4 \times 243 = 1 + 972 = \mathbf{973}$$

---

### Parte ii) Cálculo del Espacio de Versiones ($VS_{H,D}$)

Utilizamos el algoritmo **Candidate-Elimination**:

#### Paso 0: Inicialización
* **Límite más específico:**
  $$S_0 = \{ \langle \emptyset, \emptyset, \emptyset, \emptyset, \emptyset, \emptyset \rangle \}$$
* **Límite más general:**
  $$G_0 = \{ \langle ?, ?, ?, ?, ?, ? \rangle \}$$

---

#### Paso 1: Ejemplo 1 ($d_1$, Positivo)
$$d_1 = [\text{Soleado}, \text{Templado}, \text{Normal}, \text{Fuerte}, \text{Templada}, \text{Sin cambios}], \quad c(d_1) = \text{SÍ}$$

* En $G$: $G_0$ clasifica $d_1$ como positivo $\implies G_1 = G_0 = \{ \langle ?, ?, ?, ?, ?, ? \rangle \}$.
* En $S$: Se generaliza mínimamente $S_0$ para cubrir $d_1$:
  $$S_1 = \{ \langle \text{Soleado}, \text{Templado}, \text{Normal}, \text{Fuerte}, \text{Templada}, \text{Sin cambios} \rangle \}$$

---

#### Paso 2: Ejemplo 2 ($d_2$, Positivo)
$$d_2 = [\text{Soleado}, \text{Templado}, \text{Alta}, \text{Fuerte}, \text{Templada}, \text{Sin cambios}], \quad c(d_2) = \text{SÍ}$$

* En $G$: $G_1$ clasifica $d_2$ como positivo $\implies G_2 = G_1$.
* En $S$: Se comparan los atributos entre $S_1$ y $d_2$:
  * Cielo: `Soleado` = `Soleado` $\to$ `Soleado`
  * Temp: `Templado` = `Templado` $\to$ `Templado`
  * Humedad: `Normal` $\ne$ `Alta` $\to `?`$
  * Viento: `Fuerte` = `Fuerte` $\to$ `Fuerte`
  * Tmp. Agua: `Templada` = `Templada` $\to$ `Templada`
  * Tiempo: `Sin cambios` = `Sin cambios` $\to$ `Sin cambios`
  $$S_2 = \{ \langle \text{Soleado}, \text{Templado}, ?, \text{Fuerte}, \text{Templada}, \text{Sin cambios} \rangle \}$$

---

#### Paso 3: Ejemplo 3 ($d_3$, Negativo)
$$d_3 = [\text{Lluvioso}, \text{Frío}, \text{Alta}, \text{Fuerte}, \text{Templada}, \text{Cambiante}], \quad c(d_3) = \text{NO}$$

* En $S$: $S_2$ clasifica $d_3$ como negativo (falla en Cielo, Temp, Tiempo) $\implies S_3 = S_2$.
* En $G$: $G_2 = \{ \langle ?, ?, ?, ?, ?, ? \rangle \}$ clasifica $d_3$ como positivo (error).  
  Se generan todas las especificaciones mínimas de $G$ que descarten $d_3$ y sean más generales que $S_2$:
  * Diferencia en Cielo (`Lluvioso` vs `Soleado`) $\implies \langle \text{Soleado}, ?, ?, ?, ?, ? \rangle$
  * Diferencia en Temp (`Frío` vs `Templado`) $\implies \langle ?, \text{Templado}, ?, ?, ?, ? \rangle$
  * Diferencia en Humedad $\to S_2$ tiene `?`, no se puede restringir.
  * Diferencia en Viento $\to d_3$ tiene `Fuerte` igual que $S_2$, no discrimina.
  * Diferencia en Tmp. Agua $\to d_3$ tiene `Templada` igual que $S_2$, no discrimina.
  * Diferencia en Tiempo (`Cambiante` vs `Sin cambios`) $\implies \langle ?, ?, ?, ?, ?, \text{Sin cambios} \rangle$
  $$G_3 = \{ \langle \text{Soleado}, ?, ?, ?, ?, ? \rangle, \langle ?, \text{Templado}, ?, ?, ?, ? \rangle, \langle ?, ?, ?, ?, ?, \text{Sin cambios} \rangle \}$$

---

#### Paso 4: Ejemplo 4 ($d_4$, Positivo)
$$d_4 = [\text{Soleado}, \text{Templado}, \text{Alta}, \text{Fuerte}, \text{Fría}, \text{Cambiante}], \quad c(d_4) = \text{SÍ}$$

* En $G$: Evaluamos cada hipótesis de $G_3$ con $d_4$:
  * $\langle \text{Soleado}, ?, ?, ?, ?, ? \rangle$ acepta $d_4$ (correcto) $\implies$ Se conserva.
  * $\langle ?, \text{Templado}, ?, ?, ?, ? \rangle$ acepta $d_4$ (correcto) $\implies$ Se conserva.
  * $\langle ?, ?, ?, ?, ?, \text{Sin cambios} \rangle$ **rechaza** $d_4$ porque Tiempo es `Cambiante` (error) $\implies$ **Se elimina**.
  $$G_4 = \{ \langle \text{Soleado}, ?, ?, ?, ?, ? \rangle, \langle ?, \text{Templado}, ?, ?, ?, ? \rangle \}$$
* En $S$: Se generaliza $S_3$ para cubrir $d_4$:
  * Tmp. Agua: `Templada` vs `Fría` $\to `?`$
  * Tiempo: `Sin cambios` vs `Cambiante` $\to `?`$
  $$S_4 = \{ \langle \text{Soleado}, \text{Templado}, ?, \text{Fuerte}, ?, ? \rangle \}$$

---

#### Resultado Final del Espacio de Versiones:
$$\mathbf{S = \{ \langle \text{Soleado}, \text{Templado}, ?, \text{Fuerte}, ?, ? \rangle \}}$$
$$\mathbf{G = \{ \langle \text{Soleado}, ?, ?, ?, ?, ? \rangle, \langle ?, \text{Templado}, ?, ?, ?, ? \rangle \}}$$

---

### Parte iii) Clasificación de Nuevas Instancias

Para clasificar una instancia nueva $x$, se evalúa contra todas las hipótesis de $S$ y de $G$:

1. **Instancia 5:** $\langle \text{Soleado}, \text{Templado}, \text{Normal}, \text{Fuerte}, \text{Fría}, \text{Cambiante} \rangle$
   * Evaluación en $S$: Cumple `Soleado`, `Templado`, `Fuerte` $\implies \mathbf{S\text{í}}$
   * Evaluación en $G$: Cumple `Soleado` y cumple `Templado` $\implies \mathbf{S\text{í}}$
   * **Resultado:** **SÍ (Con certeza / Unánime)**.

2. **Instancia 6:** $\langle \text{Lluvioso}, \text{Frío}, \text{Normal}, \text{Suave}, \text{Templada}, \text{Sin cambios} \rangle$
   * Evaluación en $S$: No cumple $\implies \mathbf{No}$
   * Evaluación en $G$: No cumple `Soleado` ni cumple `Templado` $\implies \mathbf{No}$
   * **Resultado:** **NO (Con certeza / Unánime)**.

3. **Instancia 7:** $\langle \text{Soleado}, \text{Templado}, \text{Normal}, \text{Suave}, \text{Templada}, \text{Sin cambios} \rangle$
   * Evaluación en $S$: Falla en Viento (`Suave` $\ne$ `Fuerte`) $\implies \mathbf{No}$
   * Evaluación en $G$: Cumple `Soleado` y `Templado` $\implies \mathbf{S\text{í}}$
   * **Resultado:** **AMBIGUO / INCERTIDUMBRE** (El espacio de versiones no es unánime; algunas hipótesis intermedias la aceptan y otras la rechazan).

4. **Instancia 8:** $\langle \text{Soleado}, \text{Frío}, \text{Normal}, \text{Fuerte}, \text{Templada}, \text{Sin cambios} \rangle$
   * Evaluación en $S$: Falla en Temp (`Frío` $\ne$ `Templado`) $\implies \mathbf{No}$
   * Evaluación en $G$: Cumple $\langle \text{Soleado}, ?, ?, ?, ?, ? \rangle$ (Sí), pero falla $\langle ?, \text{Templado}, ?, ?, ?, ? \rangle$ (No) $\implies \text{Voto dividido}$
   * **Resultado:** **AMBIGUO / INCERTIDUMBRE**.
