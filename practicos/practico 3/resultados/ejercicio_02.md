# Ejercicio 2: Principio de Mínima Longitud de Descripción (MDL)

**Práctico 3: Aprendizaje Bayesiano, Aprendizaje por Casos y Metodología**  
**Curso:** Aprendizaje Automático

---

## Enunciado

Se desea aplicar el principio MDL (*Minimum Description Length*) a un espacio de conjunciones de hasta $n$ atributos booleanos; por ejemplo: $\text{Soleado} \land \text{SinCambios}$. Se tiene un conjunto de $m$ ejemplos.

Cada hipótesis se transmite listando sus atributos; cada atributo se codifica utilizando $\log_2(n)$ bits. Dada una hipótesis $h$, la codificación de un ejemplo tiene largo cero si $h$ lo clasifica correctamente, y largo $\log_2(m)$ en caso contrario (para indicar cuál ejemplo es errado).

- **a)** Dé la expresión a minimizar según el principio MDL.
- **b)** ¿Es posible construir un conjunto de entrenamiento que tenga una hipótesis consistente pero haga que MDL elija otra menos consistente? Justifique.
- **c)** Plantee distribuciones para $P(h)$ y $P(D \mid h)$ bajo las cuales el algoritmo MDL da como resultado una hipótesis MAP.

---

## Solución Detallada

### 💻 Código Ejecutable
Se incluye el script interactivo que simula y verifica numéricamente la selección de hipótesis por MDL:
* 🐍 [**`scripts/ejercicio_02_mdl.py`**](./scripts/ejercicio_02_mdl.py)

---

### Parte a) Expresión a Minimizar según MDL

El principio **MDL** (*Minimum Description Length*) formula que la mejor hipótesis $h$ es aquella que minimiza la suma del costo de codificación de la propia hipótesis más el costo de codificación de las excepciones o errores cometidos por la hipótesis sobre el conjunto de datos $D$:

$$h_{\text{MDL}} = \arg\min_{h \in H} \left[ L_{C_1}(h) + L_{C_2}(D \mid h) \right]$$

A partir de las especificaciones del problema:

1. **Costo de codificación de la hipótesis $L_{C_1}(h)$:**
   - La hipótesis se transmite listando sus atributos.
   - Si la conjunción contiene $k(h)$ atributos (donde $0 \le k(h) \le n$), y cada atributo cuesta $\log_2(n)$ bits:
     $$L_{C_1}(h) = k(h) \cdot \log_2(n)$$

2. **Costo de codificación de los datos dados la hipótesis $L_{C_2}(D \mid h)$:**
   - Los ejemplos clasificados correctamente tienen costo $0$ bits.
   - Cada ejemplo mal clasificado por $h$ requiere $\log_2(m)$ bits para identificar cuál de los $m$ ejemplos de $D$ cometió el error.
   - Si $h$ comete $e(h)$ errores de clasificación sobre $D$:
     $$L_{C_2}(D \mid h) = e(h) \cdot \log_2(m)$$

#### Expresión Final:
$$\mathbf{h_{\text{MDL}} = \arg\min_{h \in H} \left[ k(h) \log_2(n) + e(h) \log_2(m) \right]}$$

---

### Parte b) Selección de Hipótesis Menos Consistente sobre una Consistente

> **Respuesta:** **SÍ, es perfectamente posible.**

#### Justificación y Demostración:

El principio MDL formaliza matemáticamente el principio de parsimonia o **Navaja de Ockham**, penalizando hipótesis complejas (*sobreajustadas*) en favor de hipótesis más simples que cometan un pequeño número de errores tolerables.

Consideremos un escenario concreto:
- Supongamos $n = 100$ atributos disponibles ($\log_2(n) = \log_2(100) \approx 6{,}64$ bits).
- Disponemos de un conjunto de $m = 10$ ejemplos ($\log_2(m) = \log_2(10) \approx 3{,}32$ bits).

Analicemos dos hipótesis candidatas:
1. **Hipótesis $h_1$ (Consistente pero muy compleja):**
   - Requiere una conjunción de $k_1 = 8$ atributos para memorizar y ser consistente con los 10 ejemplos sin cometer errores ($e_1 = 0$).
   - $\text{MDL}(h_1) = 8 \cdot \log_2(100) + 0 \cdot \log_2(10) \approx 8 \cdot 6{,}64 = \mathbf{53{,}12 \text{ bits}}$.

2. **Hipótesis $h_2$ (Simple pero no perfectamente consistente):**
   - Utiliza solo $k_2 = 1$ atributo, pero comete $e_2 = 1$ único error.
   - $\text{MDL}(h_2) = 1 \cdot \log_2(100) + 1 \cdot \log_2(10) \approx 6{,}64 + 3{,}32 = \mathbf{9{,}96 \text{ bits}}$.

#### Conclusión:
Dado que $\text{MDL}(h_2) < \text{MDL}(h_1)$ ($9{,}96 < 53{,}12$), el algoritmo MDL elegirá inequívocamente la hipótesis $h_2$ (inconsistente) sobre la hipótesis $h_1$ (100% consistente), previniendo el sobreajuste (*overfitting*).

---

### Parte c) Distribuciones de Probabilidad para Equivalencia MAP - MDL

La hipótesis MAP se define como:
$$h_{\text{MAP}} = \arg\max_{h \in H} P(h \mid D) = \arg\max_{h \in H} \left[ P(D \mid h) P(h) \right] = \arg\min_{h \in H} \left[ -\log_2 P(h) - \log_2 P(D \mid h) \right]$$

Según la **Teoría de la Información de Shannon**, la longitud óptima de codificación en bits de un evento $x$ con probabilidad $P(x)$ es $L(x) = -\log_2 P(x)$. Por tanto:

1. **Distribución a priori $P(h)$:**
   $$-\log_2 P(h) = L_{C_1}(h) = k(h) \log_2(n) \implies \mathbf{P(h) = 2^{-k(h)\log_2(n)} = n^{-k(h)} = \left(\frac{1}{n}\right)^{k(h)}}$$
   *(Normalizada convenientemente sobre el espacio $H$). Esta distribución penaliza exponencialmente la cantidad de literales de la hipótesis (asigna menor probabilidad a priori a hipótesis más largas y complejas).*

2. **Distribución de verosimilitud $P(D \mid h)$:**
   $$-\log_2 P(D \mid h) = L_{C_2}(D \mid h) = e(h) \log_2(m) \implies \mathbf{P(D \mid h) = 2^{-e(h)\log_2(m)} = m^{-e(h)} = \left(\frac{1}{m}\right)^{e(h)}}$$
   *(Esta verosimilitud decae exponencialmente con el número de errores $e(h)$ cometidos sobre los datos de entrenamiento).*

Con estas distribuciones asignadas:
$$\arg\min_{h \in H} \left[ -\log_2 P(h) - \log_2 P(D \mid h) \right] \equiv \arg\min_{h \in H} \left[ k(h)\log_2(n) + e(h)\log_2(m) \right] \equiv h_{\text{MDL}}$$

Por ende, bajo estas distribuciones, el principio MDL conduce exactamente a una hipótesis MAP.
