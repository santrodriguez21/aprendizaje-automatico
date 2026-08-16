# Ejercicio 4: Implementación y Experimentación de Find-S

**Práctico 1: Introducción y Aprendizaje Conceptual**  
**Curso:** Aprendizaje Automático

---

## Enunciado

### a)
Implemente el algoritmo FIND-S para el problema de cuándo Pedro salva un examen.

### b)
Verifique su algoritmo contra el ejemplo visto en el teórico.

### c)
Implemente un programa que genere instancias aleatorias, y luego las clasifique de acuerdo al concepto: 
$$\langle ?, \text{Media}, ?, ?, ? \rangle$$
¿Cuántos ejemplos únicos (sin repetidos) tiene que generar en promedio para aprender el concepto? ¿Cuántos ejemplos únicos positivos?

---

## Solución y Desarrollo

### 💻 Código Ejecutable en Python
El código completo y documentado para la implementación, verificación y simulación estadística de Monte Carlo se encuentra en el script:
* 🐍 [**`scripts/ejercicio_04_find_s.py`**](./scripts/ejercicio_04_find_s.py)

Para ejecutarlo desde la terminal:
```bash
python "practicos/practico 1/resultados/scripts/ejercicio_04_find_s.py"
```

---

### Parte a) Lógica del Algoritmo Find-S

Find-S inicializa su hipótesis con la más específica posible ($\langle \emptyset, \emptyset, \emptyset, \emptyset, \emptyset \rangle$). Para cada ejemplo de entrenamiento:
* Si el ejemplo es **positivo**, compara cada atributo con la hipótesis actual: si difieren, generaliza reemplazándolo por `?`.
* Si el ejemplo es **negativo**, se ignora completamente.

---

### Parte b) Verificación Paso a Paso con el Teórico

Con el dataset del teórico:
* $x_1 = [\text{Alta}, \text{Alta}, \text{Nocturno}, \text{Media}, \text{Bueno}]$ ($+$)
* $x_2 = [\text{Baja}, \text{Media}, \text{Matutino}, \text{Alta}, \text{Malo}]$ ($-$)
* $x_3 = [\text{Media}, \text{Alta}, \text{Nocturno}, \text{Media}, \text{Malo}]$ ($+$)
* $x_4 = [\text{Media}, \text{Alta}, \text{Matutino}, \text{Alta}, \text{Bueno}]$ ($-$)

#### Traza:
1. $h_0 = \langle \emptyset, \emptyset, \emptyset, \emptyset, \emptyset \rangle$
2. Llega $x_1$ ($+$):
   $$h_1 = \langle \text{Alta}, \text{Alta}, \text{Nocturno}, \text{Media}, \text{Bueno} \rangle$$
3. Llega $x_2$ ($-$):
   $$h_2 = h_1$$
   *(Find-S ignora los ejemplos negativos).*
4. Llega $x_3$ ($+$):
   * Dedicación (`Alta` vs `Media` $\to `?`$)
   * HumorDoc (`Bueno` vs `Malo` $\to `?`$)
   $$h_3 = \langle ?, \text{Alta}, \text{Nocturno}, \text{Media}, ? \rangle$$
5. Llega $x_4$ ($-$):
   $$h_{\text{final}} = \langle ?, \text{Alta}, \text{Nocturno}, \text{Media}, ? \rangle$$

*(El script verifica automáticamente que la salida coincide de forma idéntica con el resultado teórico).*

---

### Parte c) Análisis de la Simulación Monte Carlo

El concepto objetivo a aprender es $c = \langle ?, \text{Media}, ?, ?, ? \rangle$ (es decir, la instancia es positiva si y solo si la dificultad es `Media`).

#### Características del Espacio de Búsqueda:
* **Total de instancias en el universo:** $|X| = 3 \times 3 \times 2 \times 3 \times 2 = 108$.
* **Total de instancias positivas para $c$ en $X$:**
  $$|X_+| = 3 \times 1 \times 2 \times 3 \times 2 = 36 \implies P(\text{Positivo}) = \frac{36}{108} = \frac{1}{3}$$
* Para que Find-S generalice a `?` en todos los atributos libres (Dedicación, Horario, Humedad, HumorDoc), el algoritmo debe observar al menos dos valores distintos en cada uno de los 4 atributos libres dentro de ejemplos positivos.

#### Resultados Promedio Obtenidos ($10.000$ repeticiones):
* **Ejemplos únicos totales necesarios en promedio:** $\mathbf{11.20 \pm 5.76}$ ejemplos.
* **Ejemplos únicos positivos necesarios en promedio:** $\mathbf{3.80 \pm 1.30}$ ejemplos.

> [!NOTE]
> Dado que la probabilidad de extraer un ejemplo positivo uniforme al azar es $p = \frac{1}{3}$, en promedio se requieren $3 \times 3.8 \approx 11.4$ muestras para observar los $3.8$ ejemplos positivos necesarios que generalicen todos los atributos libres a `?`.
