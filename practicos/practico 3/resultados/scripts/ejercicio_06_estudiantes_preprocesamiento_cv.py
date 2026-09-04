"""
Script de resolución y verificación para el Ejercicio 6: Dataset Estudiantes
Preprocesamiento, Estandarización, One-Hot Encoding y 3-Fold Cross Validation con clasificador trivial
"""

import numpy as np
import pandas as pd

# Dataset
raw_data = [
    {"id": 1,  "nombre": "Luisa",     "turno": "Vespertino", "edad": 16, "nota": 10, "sexo": "Fem",  "estatura": 1.79, "aprueba": "Sí"},
    {"id": 2,  "nombre": "Ana",       "turno": "Vespertino", "edad": 15, "nota": 3,  "sexo": "Masc", "estatura": 1.65, "aprueba": "Sí"},
    {"id": 3,  "nombre": "Juanjo",    "turno": "Matutino",   "edad": 14, "nota": 4,  "sexo": "Masc", "estatura": None, "aprueba": "No"},
    {"id": 4,  "nombre": "Pedro",     "turno": "Vespertino", "edad": 16, "nota": 9,  "sexo": "Masc", "estatura": None, "aprueba": "Sí"},
    {"id": 5,  "nombre": "Ramiro",    "turno": "Vespertino", "edad": 15, "nota": 3,  "sexo": None,   "estatura": 1.65, "aprueba": "Sí"},
    {"id": 6,  "nombre": "Daniel",    "turno": "Matutino",   "edad": 15, "nota": 8,  "sexo": "Masc", "estatura": None, "aprueba": "No"},
    {"id": 7,  "nombre": "Eduardo",   "turno": None,         "edad": 14, "nota": 10, "sexo": "Masc", "estatura": None, "aprueba": "Sí"},
    {"id": 8,  "nombre": "Aiala",     "turno": None,         "edad": 15, "nota": 9,  "sexo": "Fem",  "estatura": None, "aprueba": "Sí"},
    {"id": 9,  "nombre": "Dina",      "turno": "Matutino",   "edad": 15, "nota": 7,  "sexo": "Fem",  "estatura": None, "aprueba": "No"},
    {"id": 10, "nombre": "Mathias",   "turno": "Vespertino", "edad": 14, "nota": 11, "sexo": "Masc", "estatura": 1.79, "aprueba": "Sí"},
    {"id": 11, "nombre": "Diego",     "turno": "Matutino",   "edad": 15, "nota": 5,  "sexo": "Masc", "estatura": None, "aprueba": "Sí"},
    {"id": 12, "nombre": "Santiago",  "turno": "Vespertino", "edad": 15, "nota": 6,  "sexo": "Masc", "estatura": 1.67, "aprueba": "Sí"},
    {"id": 13, "nombre": "Luis",      "turno": "Matutino",   "edad": 15, "nota": 6,  "sexo": "Masc", "estatura": 1.72, "aprueba": "No"},
    {"id": 14, "nombre": "Alejandra", "turno": "Vespertino", "edad": 16, "nota": 6,  "sexo": "Fem",  "estatura": 1.73, "aprueba": "Sí"},
]

df = pd.DataFrame(raw_data)

def simular_3fold_cv():
    print("=== EJERCICIO 6: PARTE F) 3-FOLD CROSS VALIDATION CON CLASIFICADOR MAYORITARIO ===")
    
    # Dataset total: 10 'Sí', 4 'No' (Total = 14)
    # Partición estratificada en 3 folds:
    # Folds con aprox 5, 5, 4 instancias
    # Fold 1 (5): 3 Sí, 2 No
    # Fold 2 (5): 3 Sí, 2 No
    # Fold 3 (4): 4 Sí, 0 No
    
    # Alternativamente, asignación manual balanceada:
    # Fold 1: [1(Sí), 4(Sí), 7(Sí), 3(No), 6(No)] -> 3 Sí, 2 No (Total 5)
    # Fold 2: [2(Sí), 5(Sí), 8(Sí), 9(No), 13(No)] -> 3 Sí, 2 No (Total 5)
    # Fold 3: [10(Sí), 11(Sí), 12(Sí), 14(Sí)] -> 4 Sí, 0 No (Total 4)
    
    folds = [
        {"fold": 1, "test_si": 3, "test_no": 2},
        {"fold": 2, "test_si": 3, "test_no": 2},
        {"fold": 3, "test_si": 4, "test_no": 0},
    ]
    
    # En todos los casos de entrenamiento:
    # Fold 1 test -> Train tiene 7 Sí, 2 No => Mayoritaria = 'Sí'
    # Fold 2 test -> Train tiene 7 Sí, 2 No => Mayoritaria = 'Sí'
    # Fold 3 test -> Train tiene 6 Sí, 4 No => Mayoritaria = 'Sí'
    # Por lo tanto, el clasificador siempre predice 'Sí' para todas las instancias de test en cada fold.
    
    metricas = []
    
    for f in folds:
        k = f["fold"]
        pos_reales = f["test_si"]
        neg_reales = f["test_no"]
        total_test = pos_reales + neg_reales
        
        # Como siempre predice 'Sí':
        tp = pos_reales
        fp = neg_reales
        fn = 0
        tn = 0
        
        prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = (2 * prec * rec) / (prec + rec) if (prec + rec) > 0 else 0.0
        
        metricas.append({"fold": k, "tp": tp, "fp": fp, "fn": fn, "tn": tn, "prec": prec, "rec": rec, "f1": f1})
        print(f"Fold {k}: Test = {pos_reales} Sí, {neg_reales} No | TP={tp}, FP={fp}, FN={fn}, TN={tn}")
        print(f"  Precisión = {prec:.4f}, Recall = {rec:.4f}, F1 = {f1:.4f}")
    
    prec_list = [m["prec"] for m in metricas]
    rec_list = [m["rec"] for m in metricas]
    f1_list = [m["f1"] for m in metricas]
    
    # Usamos desviación estándar muestral (ddof=1)
    mean_prec = np.mean(prec_list)
    std_prec = np.std(prec_list, ddof=1)
    
    mean_rec = np.mean(rec_list)
    std_rec = np.std(rec_list, ddof=1)
    
    mean_f1 = np.mean(f1_list)
    std_f1 = np.std(f1_list, ddof=1)
    
    print("\n--- RESULTADOS GLOBALES 3-FOLD CV ---")
    print(f"Precision: {mean_prec:.4f} +/- {std_prec:.4f}")
    print(f"Recall:    {mean_rec:.4f} +/- {std_rec:.4f}")
    print(f"Medida F1: {mean_f1:.4f} +/- {std_f1:.4f}")

if __name__ == "__main__":
    simular_3fold_cv()
