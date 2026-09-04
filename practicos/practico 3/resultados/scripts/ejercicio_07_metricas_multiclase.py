"""
Script de resolución y verificación para el Ejercicio 7: Métricas de Evaluación Multiclase
Cálculo de Accuracy, Precisión, Recall, F1 por clase y Promedios Micro / Macro
"""

import numpy as np
import pandas as pd

# Matriz de confusión dada en la letra:
# Filas: Reales (A, B, C)
# Columnas: Predichos (A, B, C)
conf_matrix = np.array([
    [910,   5,   5],  # Real A (Total = 920)
    [  5,  20,  20],  # Real B (Total = 45)
    [  6,   4,  15]   # Real C (Total = 25)
])

classes = ["A", "B", "C"]
n_total = conf_matrix.sum()

def calcular_metricas():
    print("=== EJERCICIO 7: MATRIZ DE CONFUSIÓN Y MÉTRICAS MULTICLASE ===")
    print("Matriz de Confusión:")
    df_cm = pd.DataFrame(conf_matrix, index=[f"Real {c}" for c in classes], columns=[f"Pred {c}" for c in classes])
    print(df_cm)
    print(f"Total de instancias evaluadas: N = {n_total}\n")
    
    # Cálculos por clase (One-vs-Rest)
    metrics_per_class = {}
    
    for i, c in enumerate(classes):
        tp = conf_matrix[i, i]
        fp = conf_matrix[:, i].sum() - tp
        fn = conf_matrix[i, :].sum() - tp
        tn = n_total - (tp + fp + fn)
        
        acc = (tp + tn) / n_total
        prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = (2 * prec * rec) / (prec + rec) if (prec + rec) > 0 else 0.0
        
        metrics_per_class[c] = {
            "TP": tp, "FP": fp, "FN": fn, "TN": tn,
            "Accuracy": acc, "Precision": prec, "Recall": rec, "F1": f1,
            "Soporte": conf_matrix[i, :].sum()
        }
        
        print(f"--- CLASE {c} (One-vs-Rest) ---")
        print(f"  TP = {tp}, FP = {fp}, FN = {fn}, TN = {tn} | Total Real = {conf_matrix[i, :].sum()}")
        print(f"  Accuracy  = ({tp} + {tn}) / {n_total} = {acc:.4f} ({acc*100:.2f}%)")
        print(f"  Precisión = {tp} / ({tp} + {fp}) = {prec:.4f} ({prec*100:.2f}%)")
        print(f"  Recall    = {tp} / ({tp} + {fn}) = {rec:.4f} ({rec*100:.2f}%)")
        print(f"  F1-Score  = 2 * ({prec:.4f} * {rec:.4f}) / ({prec:.4f} + {rec:.4f}) = {f1:.4f}\n")
    
    # Macro Average: Promedio aritmético simple de las métricas de cada clase
    macro_prec = np.mean([m["Precision"] for m in metrics_per_class.values()])
    macro_rec = np.mean([m["Recall"] for m in metrics_per_class.values()])
    macro_f1 = np.mean([m["F1"] for m in metrics_per_class.values()])
    
    # Micro Average: Agregación global de todos los TP, FP, FN
    total_tp = sum(m["TP"] for m in metrics_per_class.values())
    total_fp = sum(m["FP"] for m in metrics_per_class.values())
    total_fn = sum(m["FN"] for m in metrics_per_class.values())
    
    micro_prec = total_tp / (total_tp + total_fp)
    micro_rec = total_tp / (total_tp + total_fn)
    micro_f1 = (2 * micro_prec * micro_rec) / (micro_prec + micro_rec)
    
    # Global Accuracy
    global_acc = total_tp / n_total
    
    print("=== PROMEDIOS GLOBALES ===")
    print(f"Global Accuracy (Tasa de acierto global): {total_tp}/{n_total} = {global_acc:.4f} ({global_acc*100:.2f}%)")
    print(f"\nMacro Average:")
    print(f"  Macro-Precision: ({metrics_per_class['A']['Precision']:.4f} + {metrics_per_class['B']['Precision']:.4f} + {metrics_per_class['C']['Precision']:.4f}) / 3 = {macro_prec:.4f} ({macro_prec*100:.2f}%)")
    print(f"  Macro-Recall:    ({metrics_per_class['A']['Recall']:.4f} + {metrics_per_class['B']['Recall']:.4f} + {metrics_per_class['C']['Recall']:.4f}) / 3 = {macro_rec:.4f} ({macro_rec*100:.2f}%)")
    print(f"  Macro-F1:        ({metrics_per_class['A']['F1']:.4f} + {metrics_per_class['B']['F1']:.4f} + {metrics_per_class['C']['F1']:.4f}) / 3 = {macro_f1:.4f}")
    
    print(f"\nMicro Average:")
    print(f"  Micro-Precision: {total_tp} / ({total_tp} + {total_fp}) = {micro_prec:.4f} ({micro_prec*100:.2f}%)")
    print(f"  Micro-Recall:    {total_tp} / ({total_tp} + {total_fn}) = {micro_rec:.4f} ({micro_rec*100:.2f}%)")
    print(f"  Micro-F1:        {micro_f1:.4f}")

if __name__ == "__main__":
    calcular_metricas()
