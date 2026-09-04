# Ejercicio 8: Intervalos de Confianza y Estimación de Error Binomial

**Práctico 3: Aprendizaje Bayesiano, Aprendizaje por Casos y Metodología**  
**Curso:** Aprendizaje Automático

---

## Enunciado

Considere un clasificador binario $h$ que, cuando es evaluado en un conjunto de 100 instancias, clasifica correctamente a 83 de ellas. 

- **a)** ¿Cuál es la desviación estándar y el intervalo de confianza de 95% para la tasa real de error?
- **b)** ¿Y si clasifica correctamente 830 de 1000 instancias?

---

## Solución Detallada

### 💻 Código Ejecutable
Se incluye el script en Python para reproducir las estimaciones y los intervalos de confianza:
* 🐍 [**`scripts/ejercicio_08_intervalos_confianza.py`**](./scripts/ejercicio_08_intervalos_confianza.py)

---

### Fundamentación Estadística Previa

Sea $h$ una hipótesis y $S$ un conjunto de prueba de $n$ instancias extraídas de forma independiente e idénticamente distribuida ($\text{i.i.d.}$) según la distribución de datos $\mathcal{D}$.

1. **Error Muestral ($\text{error}_S(h)$):**
   La proporción de errores observada sobre la muestra $S$ de tamaño $n$:
   $$\text{error}_S(h) = \frac{k}{n} = 1 - \text{Accuracy}_S(h)$$
   donde $k$ es el número de instancias mal clasificadas.

2. **Modelo Binomial y Estimación:**
   El conteo de errores $k$ sigue una distribución Binomial $k \sim \text{Binomial}(n, \text{error}_{\mathcal{D}}(h))$, donde $\text{error}_{\mathcal{D}}(h)$ es la tasa real de error poblacional que deseamos estimar.

3. **Aproximación Normal (Teorema Central del Límite):**
   Para muestras donde $n \cdot \text{error}_S(h) \ge 5$ y $n \cdot (1 - \text{error}_S(h)) \ge 5$, la distribución del estimador $\text{error}_S(h)$ se aproxima mediante una distribución normal:
   $$\text{error}_S(h) \approx \mathcal{N}\left( \text{error}_{\mathcal{D}}(h), \, \sigma^2 \right)$$
   con **desviación estándar (error estándar del estimador)**:
   $$\sigma = \sqrt{\frac{\text{error}_S(h) \cdot (1 - \text{error}_S(h))}{n}}$$

4. **Intervalo de Confianza al $(1 - \alpha)\%$ (Wald Interval):**
   $$\text{IC}_{1-\alpha} = \text{error}_S(h) \pm z_{1 - \alpha/2} \cdot \sigma$$
   Para un nivel de confianza del **$95\%$** ($\alpha = 0{,}05$), el valor crítico de la distribución normal estándar es **$z_{0{,}975} \approx 1{,}96$** (exacto: $1{,}95996$).

---

### Parte a) Evaluación con $n = 100$ Instancias (83 Aciertos)

#### 1. Estimación del Error Muestral:
- Aciertos: $r = 83 \implies \text{Accuracy} = 0{,}83$.
- Errores observados: $k = 100 - 83 = 17$.
$$\text{error}_S(h) = \frac{17}{100} = \mathbf{0{,}17 \quad (17{,}0\%)}$$

#### 2. Desviación Estándar ($\sigma$):
$$\sigma = \sqrt{\frac{0{,}17 \cdot (1 - 0{,}17)}{100}} = \sqrt{\frac{0{,}17 \cdot 0{,}83}{100}} = \sqrt{\frac{0{,}1411}{100}} = \sqrt{0{,}001411} \approx \mathbf{0{,}03756 \quad (3{,}76\%)}$$

#### 3. Intervalo de Confianza al 95%:
$$\text{Margen de Error} = z_{0{,}975} \cdot \sigma = 1{,}96 \cdot 0{,}037563 \approx \mathbf{0{,}07362 \quad (7{,}36\%)}$$

$$\text{IC}_{95\%} = 0{,}17 \pm 0{,}07362 = [0{,}17 - 0{,}07362, \, 0{,}17 + 0{,}07362] = \mathbf{[0{,}0964, \, 0{,}2436]}$$

> **Resultado Parte a:**
> - **Desviación Estándar:** $\sigma \approx \mathbf{0{,}0376 \quad (3{,}76\%)}$
> - **Intervalo de Confianza (95%):** $\mathbf{[9{,}64\%, \, 24{,}36\%]}$

---

### Parte b) Evaluación con $n = 1000$ Instancias (830 Aciertos)

#### 1. Estimación del Error Muestral:
- Aciertos: $r = 830 \implies \text{Accuracy} = 0{,}83$.
- Errores observados: $k = 1000 - 830 = 170$.
$$\text{error}_S(h) = \frac{170}{1000} = \mathbf{0{,}17 \quad (17{,}0\%)}$$

#### 2. Desviación Estándar ($\sigma$):
$$\sigma = \sqrt{\frac{0{,}17 \cdot 0{,}83}{1000}} = \sqrt{\frac{0{,}1411}{1000}} = \sqrt{0{,}0001411} \approx \mathbf{0{,}011879 \quad (1{,}19\%)}$$

#### 3. Intervalo de Confianza al 95%:
$$\text{Margen de Error} = z_{0{,}975} \cdot \sigma = 1{,}96 \cdot 0{,}011879 \approx \mathbf{0{,}02328 \quad (2{,}33\%)}$$

$$\text{IC}_{95\%} = 0{,}17 \pm 0{,}02328 = [0{,}17 - 0{,}02328, \, 0{,}17 + 0{,}02328] = \mathbf{[0{,}1467, \, 0{,}1933]}$$

> **Resultado Parte b:**
> - **Desviación Estándar:** $\sigma \approx \mathbf{0{,}0119 \quad (1{,}19\%)}$
> - **Intervalo de Confianza (95%):** $\mathbf{[14{,}67\%, \, 19{,}33\%]}$

---

### Tabla Comparativa y Análisis

| Tamaño Muestra ($n$) | Aciertos ($r$) | Error Muestral ($\text{error}_S$) | Desviación Estándar ($\sigma$) | Margen Error (95%) | Intervalo de Confianza (95%) | Ancho del Intervalo |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **$n = 100$** | $83$ | $17{,}0\%$ | **$3{,}76\%$** | $\pm 7{,}36\%$ | **$[9{,}64\%, \, 24{,}36\%]$** | $14{,}72\%$ |
| **$n = 1000$** | $830$ | $17{,}0\%$ | **$1{,}19\%$** | $\pm 2{,}33\%$ | **$[14{,}67\%, \, 19{,}33\%]$** | $4{,}66\%$ |

#### Conclusión Metodológica:
- Al multiplicar por **$10$** el tamaño de la muestra de evaluación manteniendo constante la proporción de error ($17\%$), la desviación estándar y el margen de error se reducen en un factor de:
  $$\frac{\sigma_{100}}{\sigma_{1000}} = \sqrt{\frac{1000}{100}} = \sqrt{10} \approx \mathbf{3{,}162}$$
- Esto ilustra la ley estadística según la cual la precisión de la estimación escala con $\mathcal{O}(1/\sqrt{n})$, reduciendo el ancho del intervalo a menos de un tercio y proporcionando una cota mucho más estrecha y confiable para la tasa real de error $\text{error}_{\mathcal{D}}(h)$.
