"""
Script de resolución y verificación para el Ejercicio 5: Pedro compra paltas
Métricas de evaluación, Matriz de Confusión, KNN y Naive Bayes
"""

import pandas as pd
import numpy as np

# Datos de entrenamiento
# #, Precio, Ciudad, Mes, Humor, Calidad, Peso, Compra
train_data = [
    {"id": 1, "precio": 100, "ciudad": "Salto",   "mes": "Febrero", "humor": "Bueno", "calidad": "Buena", "peso": 0.300, "compra": "Sí"},
    {"id": 2, "precio": 140, "ciudad": "Florida", "mes": "Marzo",   "humor": "Malo",  "calidad": "Media", "peso": 0.200, "compra": "No"},
    {"id": 3, "precio": 80,  "ciudad": "Salto",   "mes": "Marzo",   "humor": "Malo",  "calidad": "Buena", "peso": 0.500, "compra": "Sí"},
    {"id": 4, "precio": 160, "ciudad": "Durazno", "mes": "Agosto",  "humor": "Bueno", "calidad": "Buena", "peso": 0.700, "compra": "Sí"}, # Imputado 'Buena'
    {"id": 5, "precio": 200, "ciudad": "Salto",   "mes": "Octubre", "humor": "Bueno", "calidad": "Buena", "peso": 0.100, "compra": "No"},
]

def resolver_parte_b():
    print("=== EJERCICIO 5: PARTE B) EVALUACIÓN DEL CLASIFICADOR (PESO > 0.600) ===")
    
    # Clasificador predice 'Sí' si Peso > 0.600 else 'No'
    tp, fp, fn, tn = 0, 0, 0, 0
    
    print("Evaluación instancia por instancia:")
    for d in train_data:
        pred = "Sí" if d["peso"] > 0.600 else "No"
        real = d["compra"]
        if real == "Sí" and pred == "Sí":
            tp += 1
            tipo = "TP"
        elif real == "No" and pred == "Sí":
            fp += 1
            tipo = "FP"
        elif real == "Sí" and pred == "No":
            fn += 1
            tipo = "FN"
        else:
            tn += 1
            tipo = "TN"
        print(f"  Inst #{d['id']}: Peso={d['peso']}kg -> Pred={pred}, Real={real} [{tipo}]")
    
    print(f"\nMatriz de Confusión:")
    print(f"                Predicho Sí | Predicho No | Total Real")
    print(f"  Real Sí (Pos)     TP = {tp}    |   FN = {fn}    |    {tp+fn}")
    print(f"  Real No (Neg)     FP = {fp}    |   TN = {tn}    |    {fp+tn}")
    print(f"  Total Pred        {tp+fp}           {fn+tn}          {tp+fp+fn+tn}")
    
    acc = (tp + tn) / (tp + fp + fn + tn)
    
    # En clasificación binaria:
    # Micro-accuracy = Macro-accuracy = Global Accuracy
    acc_micro = acc
    acc_macro = acc
    
    prec_pos = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    rec_pos = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1_pos = 2 * prec_pos * rec_pos / (prec_pos + rec_pos) if (prec_pos + rec_pos) > 0 else 0.0
    
    print(f"\nMétricas:")
    print(f"  Acierto Micro (Micro Accuracy): {acc_micro:.4f} ({acc_micro*100:.1f}%)")
    print(f"  Acierto Macro (Macro Accuracy): {acc_macro:.4f} ({acc_macro*100:.1f}%)")
    print(f"  Precisión Clase Positiva ('Sí'): {prec_pos:.4f} ({prec_pos*100:.1f}%)")
    print(f"  Recall Clase Positiva ('Sí'):    {rec_pos:.4f} ({rec_pos*100:.2f}%)")
    print(f"  F1 Clase Positiva ('Sí'):        {f1_pos:.4f}")

def resolver_parte_e():
    print("\n=== EJERCICIO 5: PARTE E) NAIVE BAYES ===")
    # Instancia 6: Precio 110, Salto, Marzo, Malo, Buena, Peso 0.250
    # Discretización razonable:
    # Precio: <=120 (Bajo/Medio) vs >120 (Alto)
    # Peso: <=0.350 (Liviano) vs >0.350 (Pesado)
    print("Discretización:")
    print("  Precio: <=120 vs >120")
    print("  Peso:   <=0.350 vs >0.350")
    
    # Dataset discretizado:
    # 1: P<=120, Salto, Feb, Bueno, Buena, W<=0.350 -> Sí
    # 2: P>120,  Flor,  Mar, Malo,  Media, W<=0.350 -> No
    # 3: P<=120, Salto, Mar, Malo,  Buena, W>0.350  -> Sí
    # 4: P>120,  Dur,   Ago, Bueno, Buena, W>0.350  -> Sí
    # 5: P>120,  Salto, Oct, Bueno, Buena, W<=0.350 -> No
    
    # Instancia 6 discretizada:
    # Precio_disc: '<=120', Ciudad: 'Salto', Mes: 'Marzo', Humor: 'Malo', Calidad: 'Buena', Peso_disc: '<=0.350'
    
    n = 5
    n_si, n_no = 3, 2
    p_si, p_no = 3/5, 2/5
    
    # Para Sí:
    # P(P<=120 | Sí) = 2/3 (inst 1, 3)
    # P(Salto | Sí)  = 2/3 (inst 1, 3)
    # P(Marzo | Sí)  = 1/3 (inst 3)
    # P(Malo | Sí)   = 1/3 (inst 3)
    # P(Buena | Sí)  = 3/3 = 1 (inst 1, 3, 4)
    # P(W<=0.350 | Sí)= 1/3 (inst 1)
    score_si = (3/5) * (2/3) * (2/3) * (1/3) * (1/3) * (1.0) * (1/3)
    
    # Para No:
    # P(P<=120 | No) = 0/2 = 0 (inst 2 y 5 tienen >120)
    # P(Salto | No)  = 1/2 (inst 5)
    # P(Marzo | No)  = 1/2 (inst 2)
    # P(Malo | No)   = 1/2 (inst 2)
    # P(Buena | No)  = 1/2 (inst 5)
    # P(W<=0.350 | No)= 2/2 = 1.0 (inst 2, 5)
    score_no = (2/5) * (0/2) * (1/2) * (1/2) * (1/2) * (1/2) * (1.0)
    
    print(f"Score estándar Sí = {score_si:.6f}")
    print(f"Score estándar No = {score_no:.6f}")
    print(f"=> Predicción estándar Naive Bayes: ¿Compra? = Sí (Probabilidad = 1.0)")
    
    # Con Laplace
    # Cardinalidades: Precio:2, Ciudad:3, Mes:5, Humor:2, Calidad:3, Peso:2
    p_lap_si = (3/5) * ((2+1)/(3+2)) * ((2+1)/(3+3)) * ((1+1)/(3+5)) * ((1+1)/(3+2)) * ((3+1)/(3+3)) * ((1+1)/(3+2))
    p_lap_no = (2/5) * ((0+1)/(2+2)) * ((1+1)/(2+3)) * ((1+1)/(2+5)) * ((1+1)/(2+2)) * ((1+1)/(2+3)) * ((2+1)/(2+2))
    print(f"Score con Laplace Sí = {p_lap_si:.6f}")
    print(f"Score con Laplace No = {p_lap_no:.6f}")
    p_norm_si = p_lap_si / (p_lap_si + p_lap_no)
    p_norm_no = p_lap_no / (p_lap_si + p_lap_no)
    print(f"Probabilidad Laplace: P(Sí|x6) = {p_norm_si:.4f}, P(No|x6) = {p_norm_no:.4f}")
    print(f"=> Predicción Laplace: ¿Compra? = Sí")

if __name__ == "__main__":
    resolver_parte_b()
    resolver_parte_e()
