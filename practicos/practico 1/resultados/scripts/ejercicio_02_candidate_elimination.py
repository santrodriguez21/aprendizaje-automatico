"""
Ejercicio 2: Algoritmo Candidate-Elimination (Pedro Fútbol Playa)
=================================================================
Práctico 1: Introducción y Aprendizaje Conceptual
Curso: Aprendizaje Automático

Calcula las fronteras S y G del Espacio de Versiones y evalúa las instancias 5 a 8.
"""

from typing import List, Tuple

ATRIBUTOS = {
    'Cielo': ['Soleado', 'Lluvioso', 'Nublado'],
    'Temp': ['Templado', 'Frío'],
    'Humedad': ['Normal', 'Alta'],
    'Viento': ['Fuerte', 'Suave'],
    'TmpAgua': ['Templada', 'Fría'],
    'Tiempo': ['Sin cambios', 'Cambiante']
}

NOMBRES_ATTRS = list(ATRIBUTOS.keys())
N_ATTRS = len(NOMBRES_ATTRS)

def es_mas_general_o_igual(h1: List[str], h2: List[str]) -> bool:
    """Retorna True si h1 >=_g h2."""
    for v1, v2 in zip(h1, h2):
        if v1 != '?' and v1 != v2:
            return False
    return True

def satisface(instancia: Tuple[str, ...], h: List[str]) -> bool:
    """Evalúa si una instancia cumple una hipótesis h."""
    for v_inst, v_h in zip(instancia, h):
        if v_h != '?' and v_h != v_inst:
            return False
    return True

def candidate_elimination(datos: List[Tuple[Tuple[str, ...], int]]):
    S = [['∅'] * N_ATTRS]
    G = [['?'] * N_ATTRS]
    
    for i, (x, c) in enumerate(datos, 1):
        print(f"\n--- Paso {i}: Procesando instancia {x} (Clase: {'+' if c==1 else '-'}) ---")
        if c == 1:
            # Remover de G inconsistentes
            G = [g for g in G if satisface(x, g)]
            
            # Generalizar S
            nuevo_S = []
            for s in S:
                if not satisface(x, s):
                    if s == ['∅'] * N_ATTRS:
                        h_gen = list(x)
                        if any(es_mas_general_o_igual(g, h_gen) for g in G):
                            nuevo_S.append(h_gen)
                    else:
                        h_gen = list(s)
                        for j in range(N_ATTRS):
                            if h_gen[j] != x[j]:
                                h_gen[j] = '?'
                        if any(es_mas_general_o_igual(g, h_gen) for g in G):
                            nuevo_S.append(h_gen)
                else:
                    nuevo_S.append(s)
            S = nuevo_S
        else:
            # Remover de S inconsistentes
            S = [s for s in S if not satisface(x, s)]
            
            # Especificar G
            nuevo_G = []
            for g in G:
                if satisface(x, g):
                    for j in range(N_ATTRS):
                        if g[j] == '?':
                            for val in ATRIBUTOS[NOMBRES_ATTRS[j]]:
                                if val != x[j]:
                                    h_esp = list(g)
                                    h_esp[j] = val
                                    if any(es_mas_general_o_igual(h_esp, s) for s in S):
                                        if h_esp not in nuevo_G:
                                            nuevo_G.append(h_esp)
                else:
                    if g not in nuevo_G:
                        nuevo_G.append(g)
            G = nuevo_G
            
        print(f"  S = {S}")
        print(f"  G = {G}")
        
    return S, G

if __name__ == '__main__':
    datos_entrenamiento = [
        (('Soleado', 'Templado', 'Normal', 'Fuerte', 'Templada', 'Sin cambios'), 1),
        (('Soleado', 'Templado', 'Alta', 'Fuerte', 'Templada', 'Sin cambios'), 1),
        (('Lluvioso', 'Frío', 'Alta', 'Fuerte', 'Templada', 'Cambiante'), 0),
        (('Soleado', 'Templado', 'Alta', 'Fuerte', 'Fría', 'Cambiante'), 1),
    ]
    
    S_final, G_final = candidate_elimination(datos_entrenamiento)
    
    print("\n" + "=" * 60)
    print("FRONTERAS FINALES DEL ESPACIO DE VERSIONES:")
    print(f"S = {S_final}")
    print(f"G = {G_final}")
    print("=" * 60)
    
    instancias_test = [
        (5, ('Soleado', 'Templado', 'Normal', 'Fuerte', 'Fría', 'Cambiante')),
        (6, ('Lluvioso', 'Frío', 'Normal', 'Suave', 'Templada', 'Sin cambios')),
        (7, ('Soleado', 'Templado', 'Normal', 'Suave', 'Templada', 'Sin cambios')),
        (8, ('Soleado', 'Frío', 'Normal', 'Fuerte', 'Templada', 'Sin cambios')),
    ]
    
    print("\nCLASIFICACIÓN DE INSTANCIAS DE PRUEBA:")
    for num, inst in instancias_test:
        votos_S = [satisface(inst, s) for s in S_final]
        votos_G = [satisface(inst, g) for g in G_final]
        
        todos_S = all(votos_S)
        algun_G = any(votos_G)
        todos_G = all(votos_G)
        
        if todos_S:
            veredict = "SÍ (Unánime / Positivo con certeza)"
        elif not algun_G:
            veredict = "NO (Unánime / Negativo con certeza)"
        else:
            veredict = f"AMBIGUO / INCERTIDUMBRE (Voto S: {votos_S}, Voto G: {votos_G})"
            
        print(f"Instancia {num}: {inst} -> {veredict}")
