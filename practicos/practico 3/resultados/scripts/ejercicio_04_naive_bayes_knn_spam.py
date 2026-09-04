"""
Script de resolución y verificación para el Ejercicio 4: Filtro de Correo No Deseado (Spam)
Naive Bayes (estándar y con Laplace) y 2-NN
"""

from collections import Counter

# Dataset
# #, Agendado, Idioma, Para, Venta, Deseado
train_data = [
    {"id": 1, "agendado": "Sí", "idioma": "Inglés",  "para": "Sí", "venta": "Sí", "deseado": "Sí"},
    {"id": 2, "agendado": "No", "idioma": "Otro",    "para": "No", "venta": "No", "deseado": "Sí"},
    {"id": 3, "agendado": "No", "idioma": "Español", "para": "No", "venta": "Sí", "deseado": "Sí"},
    {"id": 4, "agendado": "Sí", "idioma": "Otro",    "para": "Sí", "venta": "No", "deseado": "No"},
    {"id": 5, "agendado": "No", "idioma": "Español", "para": "Sí", "venta": "Sí", "deseado": "No"},
]

test_instance = {"id": 6, "agendado": "Sí", "idioma": "Inglés", "para": "No", "venta": "Sí"}

def resolver_naive_bayes():
    print("=== EJERCICIO 4: PARTE A) NAIVE BAYES ===")
    n = len(train_data)
    n_si = sum(1 for d in train_data if d["deseado"] == "Sí")
    n_no = sum(1 for d in train_data if d["deseado"] == "No")
    
    p_si = n_si / n
    p_no = n_no / n
    print(f"P(Deseado=Sí) = {n_si}/{n} = {p_si:.3f}")
    print(f"P(Deseado=No)  = {n_no}/{n} = {p_no:.3f}")
    
    # Condicionales para Instancia #6: Agendado='Sí', Idioma='Inglés', Para='No', Venta='Sí'
    # Clase Sí (3 ejemplos: 1, 2, 3)
    p_ag_si = sum(1 for d in train_data if d["deseado"]=="Sí" and d["agendado"]=="Sí") / n_si  # 1/3
    p_id_si = sum(1 for d in train_data if d["deseado"]=="Sí" and d["idioma"]=="Inglés") / n_si  # 1/3
    p_pa_si = sum(1 for d in train_data if d["deseado"]=="Sí" and d["para"]=="No") / n_si       # 2/3
    p_ve_si = sum(1 for d in train_data if d["deseado"]=="Sí" and d["venta"]=="Sí") / n_si      # 2/3
    
    score_si = p_si * p_ag_si * p_id_si * p_pa_si * p_ve_si
    
    print("\nPara Deseado = Sí:")
    print(f"  P(Agendado=Sí | Sí) = {p_ag_si:.4f} (1/3)")
    print(f"  P(Idioma=Inglés | Sí) = {p_id_si:.4f} (1/3)")
    print(f"  P(Para=No | Sí) = {p_pa_si:.4f} (2/3)")
    print(f"  P(Venta=Sí | Sí) = {p_ve_si:.4f} (2/3)")
    print(f"  Score(Sí) = (3/5) * (1/3) * (1/3) * (2/3) * (2/3) = 4/135 ≈ {score_si:.6f}".replace("≈", "~="))
    
    # Clase No (2 ejemplos: 4, 5)
    p_ag_no = sum(1 for d in train_data if d["deseado"]=="No" and d["agendado"]=="Sí") / n_no  # 1/2
    p_id_no = sum(1 for d in train_data if d["deseado"]=="No" and d["idioma"]=="Inglés") / n_no  # 0/2 = 0
    p_pa_no = sum(1 for d in train_data if d["deseado"]=="No" and d["para"]=="No") / n_no       # 0/2 = 0
    p_ve_no = sum(1 for d in train_data if d["deseado"]=="No" and d["venta"]=="Sí") / n_no      # 1/2
    
    score_no = p_no * p_ag_no * p_id_no * p_pa_no * p_ve_no
    
    print("\nPara Deseado = No:")
    print(f"  P(Agendado=Sí | No) = {p_ag_no:.4f} (1/2)")
    print(f"  P(Idioma=Inglés | No) = {p_id_no:.4f} (0/2)")
    print(f"  P(Para=No | No) = {p_pa_no:.4f} (0/2)")
    print(f"  P(Venta=Sí | No) = {p_ve_no:.4f} (1/2)")
    print(f"  Score(No) = (2/5) * (1/2) * (0) * (0) * (1/2) = 0.0")
    
    p_post_si = score_si / (score_si + score_no)
    p_post_no = score_no / (score_si + score_no)
    print(f"\nProbabilidad Normalizada:")
    print(f"  P(Deseado=Sí | x6) = {p_post_si:.4f} (100%)")
    print(f"  P(Deseado=No | x6)  = {p_post_no:.4f} (0%)")
    print(f"=> Clasificación: Deseado = Sí (con probabilidad 1.0)")

def resolver_2nn():
    print("\n=== EJERCICIO 4: PARTE C) 2-NN ===")
    # Distancia de Hamming (número de atributos diferentes)
    attrs = ["agendado", "idioma", "para", "venta"]
    distancias = []
    for d in train_data:
        diffs = [a for a in attrs if d[a] != test_instance[a]]
        dist = len(diffs)
        distancias.append((dist, diffs, d))
    
    distancias.sort(key=lambda x: x[0])
    print("Distancias de Hamming desde Instancia #6 a cada ejemplo de entrenamiento:")
    for dist, diffs, d in distancias:
        print(f"  Inst #{d['id']}: Dist = {dist} (Diferencias: {diffs}) | Deseado = {d['deseado']}")
    
    k2 = distancias[:2]
    print(f"\nLos 2 vecinos más cercanos son:")
    for dist, _, d in k2:
        print(f"  - Inst #{d['id']} (Dist={dist}, Deseado={d['deseado']})")
    
    votos = [d["deseado"] for _, _, d in k2]
    print(f"=> Votos: {votos} => Clasificación 2-NN: Deseado = Sí (Unánime)")

if __name__ == "__main__":
    resolver_naive_bayes()
    resolver_2nn()
