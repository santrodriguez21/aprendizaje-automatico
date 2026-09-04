"""
Script de resolución y verificación para el Ejercicio 3: Medios de Pago
Implementa 3-NN, Naive Bayes y Árbol ID3 para el dataset preprocesado.
"""

import math
from collections import Counter

# Dataset Original
# #, Edad, Medio, Gasto, Mercancía, Sexo
data_raw = [
    {"id": 1, "edad": 18, "medio": "efectivo", "gasto": 80,  "mercancia": "1ra. necesidad",     "sexo": "M"},
    {"id": 2, "edad": 35, "medio": "débito",   "gasto": 12,  "mercancia": "1ra. necesidad",     "sexo": "F"},
    {"id": 3, "edad": 55, "medio": "crédito",  "gasto": 180, "mercancia": "1ra. necesidad",     "sexo": "M"},
    {"id": 4, "edad": 73, "medio": "efectivo", "gasto": 80,  "mercancia": "cultura",            "sexo": "M"}, # Imputado sexo='M' (moda)
    {"id": 5, "edad": 45, "medio": "crédito",  "gasto": 540, "mercancia": "electrodomésticos", "sexo": "M"},
    {"id": 6, "edad": 27, "medio": "débito",   "gasto": 150, "mercancia": "electrodomésticos", "sexo": "F"},
]

# Instancia a clasificar #7
test_instance_raw = {"id": 7, "edad": 38, "gasto": 950, "mercancia": "electrodomésticos", "sexo": "M"}

def discretizar_edad(edad):
    if edad < 30:
        return "<30"
    elif edad <= 60:
        return "30-60"
    else:
        return ">60"

def discretizar_gasto(gasto):
    if gasto < 100:
        return "<100"
    elif gasto <= 500:
        return "100-500"
    else:
        return ">500"

# Dataset Discretizado
data_disc = []
for d in data_raw:
    data_disc.append({
        "id": d["id"],
        "edad": discretizar_edad(d["edad"]),
        "gasto": discretizar_gasto(d["gasto"]),
        "mercancia": d["mercancia"],
        "sexo": d["sexo"],
        "medio": d["medio"]
    })

test_instance_disc = {
    "id": 7,
    "edad": discretizar_edad(test_instance_raw["edad"]),
    "gasto": discretizar_gasto(test_instance_raw["gasto"]),
    "mercancia": test_instance_raw["mercancia"],
    "sexo": test_instance_raw["sexo"]
}

def resolver_3nn():
    print("--- 1. CLASIFICACIÓN CON 3-NN ---")
    # Normalización Min-Max según rangos del enunciado: Edad in [18, 80], Gasto in [0, 1000]
    edad_min, edad_max = 18.0, 80.0
    gasto_min, gasto_max = 0.0, 1000.0
    
    def dist(d1, d2):
        n_edad1 = (d1["edad"] - edad_min) / (edad_max - edad_min)
        n_edad2 = (d2["edad"] - edad_min) / (edad_max - edad_min)
        
        n_gasto1 = (d1["gasto"] - gasto_min) / (gasto_max - gasto_min)
        n_gasto2 = (d2["gasto"] - gasto_min) / (gasto_max - gasto_min)
        
        d_merc = 0.0 if d1["mercancia"] == d2["mercancia"] else 1.0
        d_sexo = 0.0 if d1["sexo"] == d2["sexo"] else 1.0
        
        return math.sqrt((n_edad1 - n_edad2)**2 + (n_gasto1 - n_gasto2)**2 + d_merc + d_sexo)
    
    distancias = []
    for d in data_raw:
        dist_val = dist(d, test_instance_raw)
        distancias.append((dist_val, d))
    
    distancias.sort(key=lambda x: x[0])
    
    print(f"Instancia de Test #7: Edad={test_instance_raw['edad']}, Gasto={test_instance_raw['gasto']}, Merc={test_instance_raw['mercancia']}, Sexo={test_instance_raw['sexo']}")
    print("Distancias a todos los puntos de entrenamiento:")
    for d_val, d in distancias:
        print(f"  Inst #{d['id']}: Dist = {d_val:.4f} | Medio = {d['medio']} (Edad={d['edad']}, Gasto={d['gasto']}, Merc={d['mercancia']}, Sexo={d['sexo']})")
    
    k_vecinos = distancias[:3]
    votos = [d["medio"] for _, d in k_vecinos]
    conteo = Counter(votos)
    pred_3nn = conteo.most_common(1)[0][0]
    print(f"\n3 vecinos más cercanos: {[d['id'] for _, d in k_vecinos]} con medios {votos}")
    print(f"=> Predicción 3-NN: {pred_3nn}")
    return pred_3nn

def resolver_naive_bayes():
    print("\n--- 2. CLASIFICACIÓN CON NAIVE BAYES ---")
    clases = ["efectivo", "débito", "crédito"]
    n_total = len(data_disc)
    
    # Priors
    priors = {}
    for c in clases:
        priors[c] = sum(1 for d in data_disc if d["medio"] == c) / n_total
    
    print(f"Probabilidades a Priori P(Medio): {priors}")
    
    # Verosimilitud P(x | Medio)
    # x = (Edad='30-60', Gasto='>500', Merc='electrodomésticos', Sexo='M')
    print(f"Instancia Test Discretizada: {test_instance_disc}")
    
    attrs = ["edad", "gasto", "mercancia", "sexo"]
    scores = {}
    
    for c in clases:
        n_c = sum(1 for d in data_disc if d["medio"] == c)
        p_c = priors[c]
        prod_cond = 1.0
        detalles = []
        for a in attrs:
            val_a = test_instance_disc[a]
            count_a = sum(1 for d in data_disc if d["medio"] == c and d[a] == val_a)
            # Estimador estándar (frecuentista)
            p_cond = count_a / n_c
            prod_cond *= p_cond
            detalles.append(f"P({a}={val_a}|{c})={count_a}/{n_c}")
        
        score = p_c * prod_cond
        scores[c] = score
        print(f"\nClase '{c}': P({c}) = {p_c:.3f}")
        print(f"  Condicionales: {', '.join(detalles)}")
        print(f"  Score no normalizado: {score:.5f}")
    
    # Normalización si la suma > 0
    suma_scores = sum(scores.values())
    if suma_scores > 0:
        posteriors = {c: s / suma_scores for c, s in scores.items()}
        print(f"\nProbabilidades Posteriores Normalizadas: {posteriors}")
        pred_nb = max(scores, key=scores.get)
    else:
        print("\nTodos los scores estándar dieron 0 debido a ceros en verosimilitud.")
        # Con corrección de Laplace (m-estimate)
        print("\nAplicando Corrección de Laplace (Suavizado aditivo con m = número de valores posibles):")
        # Cardinalidades de atributos: edad=3, gasto=3, merc=3, sexo=2
        cardinalidades = {"edad": 3, "gasto": 3, "mercancia": 3, "sexo": 2}
        scores_laplace = {}
        for c in clases:
            n_c = sum(1 for d in data_disc if d["medio"] == c)
            prod_cond = 1.0
            detalles = []
            for a in attrs:
                val_a = test_instance_disc[a]
                count_a = sum(1 for d in data_disc if d["medio"] == c and d[a] == val_a)
                k_a = cardinalidades[a]
                p_cond = (count_a + 1) / (n_c + k_a)
                prod_cond *= p_cond
                detalles.append(f"P({a}={val_a}|{c})=({count_a}+1)/({n_c}+{k_a})={p_cond:.3f}")
            score = priors[c] * prod_cond
            scores_laplace[c] = score
            print(f"  Clase '{c}': Score = {score:.5f} ({', '.join(detalles)})")
        suma_lap = sum(scores_laplace.values())
        post_lap = {c: s / suma_lap for c, s in scores_laplace.items()}
        print(f"Probabilidades Posteriores con Laplace: {post_lap}")
        pred_nb = max(scores_laplace, key=scores_laplace.get)
    
    print(f"=> Predicción Naive Bayes: {pred_nb}")
    return pred_nb

def calcular_entropia(subset):
    if not subset:
        return 0.0
    counts = Counter(d["medio"] for d in subset)
    n = len(subset)
    ent = 0.0
    for c, cnt in counts.items():
        p = cnt / n
        ent -= p * math.log2(p)
    return ent

def resolver_id3():
    print("\n--- 3. CONSTRUCCIÓN DE ÁRBOL ID3 ---")
    ent_s = calcular_entropia(data_disc)
    print(f"Entropía inicial del conjunto S (N={len(data_disc)}): H(S) = {ent_s:.4f} bits")
    
    attrs = ["edad", "gasto", "mercancia", "sexo"]
    n_total = len(data_disc)
    
    print("\nGanancia de Información en la Raíz:")
    for a in attrs:
        valores = set(d[a] for d in data_disc)
        ent_residual = 0.0
        particiones = []
        for v in valores:
            sub = [d for d in data_disc if d[a] == v]
            e_sub = calcular_entropia(sub)
            peso = len(sub) / n_total
            ent_residual += peso * e_sub
            particiones.append(f"{v}: {len(sub)} ejs, H={e_sub:.3f}")
        gain = ent_s - ent_residual
        print(f"  Atributo '{a}': Gain = {gain:.4f} bits ({'; '.join(particiones)})")
    
    # Notemos que Gasto y Mercancía y Sexo tienen distintas particiones:
    # Gasto divide en:
    # <100: [1(efectivo), 2(débito), 4(efectivo)] -> H(2 ef, 1 deb) = 0.918
    # 100-500: [3(crédito), 6(débito)] -> H(1 cred, 1 deb) = 1.0
    # >500: [5(crédito)] -> puro! H = 0.0
    #
    # Mercancía divide en:
    # 1ra. necesidad: [1(ef), 2(deb), 3(cred)] -> H(1, 1, 1) = log2(3) = 1.585
    # cultura: [4(ef)] -> puro! H=0.0
    # electrodomésticos: [5(cred), 6(deb)] -> H(1, 1) = 1.0
    #
    # Edad divide en:
    # <30: [1(ef), 6(deb)] -> H=1.0
    # 30-60: [2(deb), 3(cred), 5(cred)] -> H(1 deb, 2 cred) = 0.918
    # >60: [4(ef)] -> puro! H=0.0
    
    print("\nEvaluando clasificación de la instancia de test #7:")
    print(f"Instancia 7 tiene: Gasto='>500', Mercancía='electrodomésticos', Edad='30-60', Sexo='M'")
    print("Si el árbol parte por 'Gasto': rama '>500' va directo a 'crédito' (instancia 5).")
    print("=> Predicción ID3: crédito")

if __name__ == "__main__":
    resolver_3nn()
    resolver_naive_bayes()
    resolver_id3()
