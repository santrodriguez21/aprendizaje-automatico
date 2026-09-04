import json

cells = []

def add_markdown(source):
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": source.strip().splitlines(keepends=True)
    })

def add_code(source):
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source.strip().splitlines(keepends=True)
    })

# --- TITLE & INTRO ---
add_markdown("""# Aprendizaje Automático - Práctico 3: Notebook Interactivo de Soluciones y Verificación
**Temas:** Aprendizaje Bayesiano, Aprendizaje por Casos ($k$-NN) y Metodología de Evaluación  
**Curso:** Aprendizaje Automático - Facultad de Ingeniería (UdelaR)

Este notebook permite ejecutar, probar de forma interactiva y visualizar todos los experimentos, clasificadores y cálculos estadísticos de los ejercicios del **Práctico 3**.""")

add_code("""# Configuración inicial e importación de librerías
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from scipy import stats

# Estilo de gráficos
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['figure.figsize'] = (9, 5)
plt.rcParams['font.size'] = 11
print("Librerías importadas correctamente.")""")

# --- EJERCICIO 1 ---
add_markdown("""---
## Ejercicio 1: Hipótesis MAP, ML y Clasificador Bayesiano Óptimo

**Enunciado:** Conjunto de entrenamiento $D$ sin ruido. Espacio $H$ donde a mayor generalidad, mayor probabilidad *a priori* $P(h)$.

* **i. Find-S da una hipótesis MAP:** **FALSA**. Find-S entrega la hipótesis más específica $S \in VS_{H,D}$, la cual tiene la *menor* probabilidad a priori dentro del espacio de versiones.
* **ii. Find-S da una hipótesis ML:** **VERDADERA**. Al ser datos sin ruido, toda hipótesis consistente $h \in VS_{H,D}$ alcanza la máxima verosimilitud posible $P(D \mid h) = 1$.
* **iii. Candidate-Elimination con votación es un clasificador bayesiano óptimo:** **FALSA**. La votación no ponderada asume un prior uniforme y no pondera los votos por la probabilidad posterior real $P(h \mid D) \propto P(h)$.""")

# --- EJERCICIO 2 ---
add_markdown("""---
## Ejercicio 2: Principio MDL (Minimum Description Length)

El principio MDL selecciona la hipótesis que minimiza:
$$h_{\\text{MDL}} = \\arg\\min_{h \\in H} \\left[ L(h) + L(D \\mid h) \\right] = \\arg\\min_{h \\in H} \\left[ k(h) \\log_2(n) + e(h) \\log_2(m) \\right]$$

A continuación probamos la selección de hipótesis comparando una hipótesis consistente pero compleja vs. una simple con 1 error:""")

add_code("""def description_length(k, e, n, m):
    \"\"\"
    k: número de atributos en la hipótesis
    e: número de errores sobre el conjunto de datos
    n: total de atributos posibles
    m: total de ejemplos
    \"\"\"
    l_h = k * math.log2(n) if n > 1 else 0
    l_d = e * math.log2(m) if m > 1 else 0
    return l_h + l_d, l_h, l_d

# Parámetros del experimento
n_atributos = 50
m_ejemplos = 20

print(f"Espacio: n = {n_atributos} atributos, m = {m_ejemplos} ejemplos\\n")

# Hipótesis 1: Consistente pero memorizada/compleja (k=8 literales, 0 errores)
mdl1, lh1, ld1 = description_length(k=8, e=0, n=n_atributos, m=m_ejemplos)
print(f"Hipótesis Compleja Consistente (k=8, e=0):")
print(f"  L(h) = {lh1:.2f} bits, L(D|h) = {ld1:.2f} bits => Costo Total MDL = {mdl1:.2f} bits")

# Hipótesis 2: Simple pero con 1 error residual (k=1 literal, 1 error)
mdl2, lh2, ld2 = description_length(k=1, e=1, n=n_atributos, m=m_ejemplos)
print(f"\\nHipótesis Simple con 1 error (k=1, e=1):")
print(f"  L(h) = {lh2:.2f} bits, L(D|h) = {ld2:.2f} bits => Costo Total MDL = {mdl2:.2f} bits")

print(f"\\n=> Ganadora según MDL: {'Hipótesis Simple (h2)' if mdl2 < mdl1 else 'Hipótesis Compleja (h1)'} (Ahorro de {abs(mdl1-mdl2):.2f} bits)")""")

# --- EJERCICIO 3 ---
add_markdown("""---
## Ejercicio 3: Inclusión Financiera - 3-NN, Naive Bayes e ID3

Dataset de medios de pago con atributos continuos (`Edad`, `Gasto`), categóricos (`Mercancía`, `Sexo`) y faltantes.""")

add_code("""# Dataset original
data_raw = [
    {"id": 1, "edad": 18, "medio": "efectivo", "gasto": 80,  "mercancia": "1ra. necesidad",     "sexo": "M"},
    {"id": 2, "edad": 35, "medio": "débito",   "gasto": 12,  "mercancia": "1ra. necesidad",     "sexo": "F"},
    {"id": 3, "edad": 55, "medio": "crédito",  "gasto": 180, "mercancia": "1ra. necesidad",     "sexo": "M"},
    {"id": 4, "edad": 73, "medio": "efectivo", "gasto": 80,  "mercancia": "cultura",            "sexo": "M"}, # Imputado 'M'
    {"id": 5, "edad": 45, "medio": "crédito",  "gasto": 540, "mercancia": "electrodomésticos", "sexo": "M"},
    {"id": 6, "edad": 27, "medio": "débito",   "gasto": 150, "mercancia": "electrodomésticos", "sexo": "F"},
]
df_e3 = pd.DataFrame(data_raw)
display(df_e3)

# Instancia a clasificar #7
test_7 = {"id": 7, "edad": 38, "gasto": 950, "mercancia": "electrodomésticos", "sexo": "M"}
print(f"\\nInstancia de Test #7: {test_7}")""")

add_code("""# 1. Clasificación con 3-NN (Normalización Min-Max + Distancia Mixta)
edad_min, edad_max = 18.0, 80.0
gasto_min, gasto_max = 0.0, 1000.0

def distancia_mixta(d1, d2):
    n_edad1, n_edad2 = (d1["edad"] - edad_min) / (edad_max - edad_min), (d2["edad"] - edad_min) / (edad_max - edad_min)
    n_gasto1, n_gasto2 = (d1["gasto"] - gasto_min) / (gasto_max - gasto_min), (d2["gasto"] - gasto_min) / (gasto_max - gasto_min)
    d_merc = 0.0 if d1["mercancia"] == d2["mercancia"] else 1.0
    d_sexo = 0.0 if d1["sexo"] == d2["sexo"] else 1.0
    return math.sqrt((n_edad1 - n_edad2)**2 + (n_gasto1 - n_gasto2)**2 + d_merc + d_sexo)

distancias = [(distancia_mixta(d, test_7), d) for d in data_raw]
distancias.sort(key=lambda x: x[0])

print("--- Distancias de #7 a los puntos de entrenamiento ---")
for dist, d in distancias:
    print(f"  Inst #{d['id']}: Dist = {dist:.4f} | Medio = {d['medio']} ({d['mercancia']}, {d['sexo']}, Edad={d['edad']}, Gasto={d['gasto']})")

top3 = distancias[:3]
votos_3nn = [d["medio"] for _, d in top3]
pred_3nn = Counter(votos_3nn).most_common(1)[0][0]
print(f"\\n3 Vecinos más cercanos: {[d['id'] for _, d in top3]} -> Votos: {votos_3nn}")
print(f"=> Predicción 3-NN: {pred_3nn}")""")

add_code("""# 2. Clasificación con Naive Bayes (Dataset Discretizado)
def disc_edad(e):
    return "<30" if e < 30 else ("30-60" if e <= 60 else ">60")

def disc_gasto(g):
    return "<100" if g < 100 else ("100-500" if g <= 500 else ">500")

data_disc = [
    {**d, "edad_d": disc_edad(d["edad"]), "gasto_d": disc_gasto(d["gasto"])} for d in data_raw
]
test_7_d = {"edad_d": disc_edad(test_7["edad"]), "gasto_d": disc_gasto(test_7["gasto"]), "mercancia": test_7["mercancia"], "sexo": test_7["sexo"]}

clases = ["efectivo", "débito", "crédito"]
priors = {c: sum(1 for d in data_disc if d["medio"] == c) / len(data_disc) for c in clases}

scores = {}
print("--- Scores Naive Bayes para #7 (Edad='30-60', Gasto='>500', Merc='electrodomésticos', Sexo='M') ---")
for c in clases:
    n_c = sum(1 for d in data_disc if d["medio"] == c)
    p_c = priors[c]
    p_edad = sum(1 for d in data_disc if d["medio"] == c and d["edad_d"] == test_7_d["edad_d"]) / n_c
    p_gasto = sum(1 for d in data_disc if d["medio"] == c and d["gasto_d"] == test_7_d["gasto_d"]) / n_c
    p_merc = sum(1 for d in data_disc if d["medio"] == c and d["mercancia"] == test_7_d["mercancia"]) / n_c
    p_sexo = sum(1 for d in data_disc if d["medio"] == c and d["sexo"] == test_7_d["sexo"]) / n_c
    
    score = p_c * p_edad * p_gasto * p_merc * p_sexo
    scores[c] = score
    print(f"  Clase '{c}': Score = {score:.5f} (P(c)={p_c:.2f}, P(edad)={p_edad:.2f}, P(gasto)={p_gasto:.2f}, P(merc)={p_merc:.2f}, P(sexo)={p_sexo:.2f})")

pred_nb = max(scores, key=scores.get)
print(f"\\n=> Predicción Naive Bayes: {pred_nb} (Score Normalizado = 100%)")""")

# --- EJERCICIO 4 ---
add_markdown("""---
## Ejercicio 4: Filtro de Correo No Deseado (Spam) - Naive Bayes y 2-NN""")

add_code("""# Dataset Spam
spam_train = [
    {"id": 1, "agendado": "Sí", "idioma": "Inglés",  "para": "Sí", "venta": "Sí", "deseado": "Sí"},
    {"id": 2, "agendado": "No", "idioma": "Otro",    "para": "No", "venta": "No", "deseado": "Sí"},
    {"id": 3, "agendado": "No", "idioma": "Español", "para": "No", "venta": "Sí", "deseado": "Sí"},
    {"id": 4, "agendado": "Sí", "idioma": "Otro",    "para": "Sí", "venta": "No", "deseado": "No"},
    {"id": 5, "agendado": "No", "idioma": "Español", "para": "Sí", "venta": "Sí", "deseado": "No"},
]
correo_6 = {"id": 6, "agendado": "Sí", "idioma": "Inglés", "para": "No", "venta": "Sí"}

# 2-NN con Distancia de Hamming
attrs = ["agendado", "idioma", "para", "venta"]
dist_spam = []
for d in spam_train:
    d_h = sum(1 for a in attrs if d[a] != correo_6[a])
    dist_spam.append((d_h, d))

dist_spam.sort(key=lambda x: x[0])
print("--- Distancias de Hamming del Correo #6 a los ejemplos de entrenamiento ---")
for d_h, d in dist_spam:
    print(f"  Inst #{d['id']}: Distancia = {d_h} | Deseado = {d['deseado']}")

top2 = dist_spam[:2]
print(f"\\n2 Vecinos más cercanos: Instancias {[d['id'] for _, d in top2]}")
print(f"=> Predicción 2-NN: Deseado = Sí (Unánime)")""")

# --- EJERCICIO 5 ---
add_markdown("""---
## Ejercicio 5: Pedro Compra Paltas - Métricas y Matriz de Confusión""")

add_code("""# Clasificador por umbral: ¿Compra? = Sí si Peso > 0.600 Kg
paltas = [
    {"id": 1, "precio": 100, "peso": 0.300, "compra": "Sí"},
    {"id": 2, "precio": 140, "peso": 0.200, "compra": "No"},
    {"id": 3, "precio": 80,  "peso": 0.500, "compra": "Sí"},
    {"id": 4, "precio": 160, "peso": 0.700, "compra": "Sí"},
    {"id": 5, "precio": 200, "peso": 0.100, "compra": "No"},
]

tp, fp, fn, tn = 0, 0, 0, 0
for p in paltas:
    pred = "Sí" if p["peso"] > 0.600 else "No"
    real = p["compra"]
    if real == "Sí" and pred == "Sí": tp += 1
    elif real == "No" and pred == "Sí": fp += 1
    elif real == "Sí" and pred == "No": fn += 1
    else: tn += 1

cm_paltas = pd.DataFrame([[tp, fn], [fp, tn]], 
                         index=["Real Sí", "Real No"], 
                         columns=["Predicho Sí", "Predicho No"])
display(cm_paltas)

acc = (tp + tn) / len(paltas)
prec = tp / (tp + fp)
rec = tp / (tp + fn)
f1 = 2 * (prec * rec) / (prec + rec)

print(f"Accuracy Global: {acc*100:.1f}%")
print(f"Precisión (Clase Sí): {prec*100:.1f}%")
print(f"Recall (Clase Sí):    {rec*100:.2f}%")
print(f"Medida F1 (Clase Sí): {f1:.4f}")""")

# --- EJERCICIO 6 ---
add_markdown("""---
## Ejercicio 6: Dataset Estudiantes - 3-Fold Cross Validation con Clasificador Trivial""")

add_code("""# Simulación 3-Fold CV
folds = [
    {"fold": 1, "test_si": 3, "test_no": 2},
    {"fold": 2, "test_si": 3, "test_no": 2},
    {"fold": 3, "test_si": 4, "test_no": 0},
]

metricas_cv = []
for f in folds:
    tp = f["test_si"]
    fp = f["test_no"]
    fn = 0
    prec = tp / (tp + fp)
    rec = 1.0
    f1 = 2 * (prec * rec) / (prec + rec)
    metricas_cv.append({"Fold": f["fold"], "Precisión": prec, "Recall": rec, "F1-Score": f1})

df_cv = pd.DataFrame(metricas_cv)
display(df_cv)

print("--- Promedios y Desviaciones Estándar (ddof=1) ---")
print(f"Precisión: {df_cv['Precisión'].mean():.4f} +/- {df_cv['Precisión'].std():.4f}")
print(f"Recall:    {df_cv['Recall'].mean():.4f} +/- {df_cv['Recall'].std():.4f}")
print(f"F1-Score:  {df_cv['F1-Score'].mean():.4f} +/- {df_cv['F1-Score'].std():.4f}")""")

# --- EJERCICIO 7 ---
add_markdown("""---
## Ejercicio 7: Matriz de Confusión Multiclase ($3 \\times 3$) y Desbalance de Clases""")

add_code("""# Matriz de confusión
cm_7 = np.array([
    [910,   5,   5],  # Real A (920)
    [  5,  20,  20],  # Real B (45)
    [  6,   4,  15]   # Real C (25)
])
classes = ["A", "B", "C"]
N_total = cm_7.sum()

df_cm7 = pd.DataFrame(cm_7, index=[f"Real {c}" for c in classes], columns=[f"Predicho {c}" for c in classes])
display(df_cm7)

res_7 = []
for i, c in enumerate(classes):
    tp = cm_7[i, i]
    fp = cm_7[:, i].sum() - tp
    fn = cm_7[i, :].sum() - tp
    tn = N_total - (tp + fp + fn)
    acc = (tp + tn) / N_total
    prec = tp / (tp + fp)
    rec = tp / (tp + fn)
    f1 = 2 * (prec * rec) / (prec + rec)
    res_7.append({"Clase": c, "Soporte": cm_7[i, :].sum(), "Accuracy": acc, "Precisión": prec, "Recall": rec, "F1-Score": f1})

df_metrics7 = pd.DataFrame(res_7)
display(df_metrics7.style.format({"Accuracy": "{:.2%}", "Precisión": "{:.2%}", "Recall": "{:.2%}", "F1-Score": "{:.4f}"}))

# Promedios
macro_p = df_metrics7["Precisión"].mean()
macro_r = df_metrics7["Recall"].mean()
macro_f1 = df_metrics7["F1-Score"].mean()
micro_acc = np.trace(cm_7) / N_total

print(f"Global Accuracy / Micro-Average: {micro_acc*100:.2f}%")
print(f"Macro-Precision: {macro_p*100:.2f}%")
print(f"Macro-Recall:    {macro_r*100:.2f}%")
print(f"Macro-F1:        {macro_f1:.4f}")

# Gráfico comparativo por clase
fig, ax = plt.subplots(figsize=(8, 4))
x = np.arange(len(classes))
width = 0.25
ax.bar(x - width, df_metrics7["Precisión"], width, label='Precisión', color='#2b5c8f')
ax.bar(x, df_metrics7["Recall"], width, label='Recall', color='#e26d5c')
ax.bar(x + width, df_metrics7["F1-Score"], width, label='F1-Score', color='#38b000')
ax.set_xticks(x)
ax.set_xticklabels([f"Clase {c} (N={cm_7[i,:].sum()})" for i, c in enumerate(classes)])
ax.set_ylabel("Métrica")
ax.set_ylim(0, 1.1)
ax.set_title("Comparación de Rendimiento por Clase (Impacto del Desbalance)")
ax.legend()
plt.tight_layout()
plt.show()""")

# --- EJERCICIO 8 ---
add_markdown("""---
## Ejercicio 8: Intervalos de Confianza al 95% para la Tasa Real de Error

Comparación del error estándar e intervalo de confianza al variar la muestra de $N=100$ a $N=1000$ (83% acierto):""")

add_code("""def calcular_ic(n, r, z=1.96):
    k = n - r
    p = k / n
    sigma = math.sqrt(p * (1 - p) / n)
    margen = z * sigma
    return p, sigma, (p - margen, p + margen), margen

p_100, s_100, ic_100, m_100 = calcular_ic(100, 83)
p_1000, s_1000, ic_1000, m_1000 = calcular_ic(1000, 830)

print(f"Muestra N=100  (83 aciertos)  -> error_S = {p_100:.2%}, sigma = {s_100:.4f} ({s_100*100:.2f}%) | IC 95%: [{ic_100[0]:.2%}, {ic_100[1]:.2%}] (Ancho: {2*m_100:.2%})")
print(f"Muestra N=1000 (830 aciertos) -> error_S = {p_1000:.2%}, sigma = {s_1000:.4f} ({s_1000*100:.2f}%) | IC 95%: [{ic_1000[0]:.2%}, {ic_1000[1]:.2%}] (Ancho: {2*m_1000:.2%})")
print(f"\\nReducción del margen de error: {s_100/s_1000:.3f}x (Exactamente sqrt(10) = {math.sqrt(10):.3f})")

# Visualización de distribuciones e intervalos
fig, ax = plt.subplots(figsize=(10, 4.5))
x_vals = np.linspace(0.05, 0.30, 1000)
y_100 = stats.norm.pdf(x_vals, p_100, s_100)
y_1000 = stats.norm.pdf(x_vals, p_1000, s_1000)

ax.plot(x_vals * 100, y_100, label=f'N=100 (sigma={s_100*100:.2f}%)', color='#e26d5c', lw=2)
ax.plot(x_vals * 100, y_1000, label=f'N=1000 (sigma={s_1000*100:.2f}%)', color='#2b5c8f', lw=2)

ax.axvspan(ic_100[0]*100, ic_100[1]*100, color='#e26d5c', alpha=0.15, label='IC 95% (N=100)')
ax.axvspan(ic_1000[0]*100, ic_1000[1]*100, color='#2b5c8f', alpha=0.25, label='IC 95% (N=1000)')

ax.set_xlabel("Tasa de Error (%)")
ax.set_ylabel("Densidad de Probabilidad")
ax.set_title("Distribución del Estimador del Error e Intervalos de Confianza al 95%")
ax.legend()
plt.tight_layout()
plt.show()""")

notebook_dict = {
    "cells": cells,
    "metadata": {
        "language_info": {
            "name": "python",
            "version": "3.13"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 2
}

output_path = r"c:\Users\santr\aprendizaje-automatico\aprendizaje-automatico\practicos\practico 3\resultados\practico_3_laboratorio.ipynb"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(notebook_dict, f, indent=2, ensure_ascii=False)

print(f"Notebook creado exitosamente en: {output_path}")
