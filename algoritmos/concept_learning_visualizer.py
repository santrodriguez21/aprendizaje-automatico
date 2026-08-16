"""
Módulo de visualización específico para Aprendizaje Conceptual y Espacio de Versiones.
Incluye funciones para graficar el Espacio de Versiones, retículas y trazas paso a paso
de los algoritmos Find-S y Candidate-Elimination.
"""

import sys
from typing import List, Dict, Set, Any
from .concept_learning import Hypothesis, CandidateElimination

if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def print_step_by_step_trace(ce: CandidateElimination):
    """Muestra en terminal una traza visual y formateada paso a paso."""
    print("=" * 80)
    print(" TRAZA PASO A PASO: CANDIDATE-ELIMINATION")
    print("=" * 80)

    for record in ce.history:
        step = record["step"]
        desc = record["description"]
        s_set = record["S"]
        g_set = record["G"]

        print(f"\n[+] PASO {step}: {desc}")
        if record["instance"] is not None:
            inst_str = ", ".join(f"{k}={v}" for k, v in zip(ce.attribute_names, record["instance"]))
            print(f"   [Instancia]: [{inst_str}]  Etiqueta: {record['label']}")

        print(f"   S_{step} = {s_set}")
        print(f"   G_{step} = {g_set}")
        print("-" * 80)


def print_ascii_version_space(ce: CandidateElimination):
    """Muestra una representación en texto (ASCII) del Espacio de Versiones."""
    print("\n" + "=" * 60)
    print(" RETÍCULA DEL ESPACIO DE VERSIONES (ASCII)")
    print("=" * 60)
    print(" [Límite General G]:")
    for g in ce.G:
        print(f"    ^  {g}")
    print("    |       ^")
    print("    |  (Hipótesis intermedias del VS)")
    print("    |       |")
    print(" [Límite Específico S]:")
    for s in ce.S:
        print(f"    *  {s}")
    print("=" * 60)


def plot_version_space(ce: CandidateElimination, title: str = "Espacio de Versiones (Version Space)", save_path: str = None, show_plot: bool = False):
    """
    Genera un gráfico de grafo/red mostrando los límites S y G y sus relaciones de generalización.
    Si matplotlib o networkx no están instalados, muestra la versión ASCII como respaldo.
    """
    try:
        import matplotlib.pyplot as plt
        import networkx as nx
    except ImportError:
        print("[!] Matplotlib o NetworkX no están disponibles. Mostrando diagrama ASCII:")
        print_ascii_version_space(ce)
        return

    G_graph = nx.DiGraph()

    # Nodos para G
    for g in ce.G:
        node_name = f"G: {repr(g)}"
        G_graph.add_node(node_name, layer=2, node_type="G", label=repr(g))

    # Nodos para S
    for s in ce.S:
        node_name = f"S: {repr(s)}"
        G_graph.add_node(node_name, layer=0, node_type="S", label=repr(s))

    # Conectar S con G si s <=_g g
    for s in ce.S:
        s_name = f"S: {repr(s)}"
        for g in ce.G:
            g_name = f"G: {repr(g)}"
            if g.is_more_general_or_equal(s):
                G_graph.add_edge(s_name, g_name)

    fig, ax = plt.subplots(figsize=(10, 6))

    # Layout por capas
    pos = {}
    g_nodes = [n for n, d in G_graph.nodes(data=True) if d.get("node_type") == "G"]
    s_nodes = [n for n, d in G_graph.nodes(data=True) if d.get("node_type") == "S"]

    for i, n in enumerate(g_nodes):
        pos[n] = (i + 1, 2.0)
    for i, n in enumerate(s_nodes):
        pos[n] = (len(g_nodes) / 2 + 0.5 if len(s_nodes) == 1 else i + 1, 0.0)

    # Dibujar nodos S (verde) y G (azul)
    nx.draw_networkx_nodes(G_graph, pos, nodelist=g_nodes, node_color="#3498db", node_size=3200, node_shape="s", alpha=0.9, ax=ax)
    nx.draw_networkx_nodes(G_graph, pos, nodelist=s_nodes, node_color="#2ecc71", node_size=3200, node_shape="o", alpha=0.9, ax=ax)

    # Dibujar aristas
    nx.draw_networkx_edges(G_graph, pos, edge_color="#7f8c8d", arrows=True, arrowsize=20, width=2, style="dashed", ax=ax)

    # Etiquetas
    labels = {n: d["label"] for n, d in G_graph.nodes(data=True)}
    nx.draw_networkx_labels(G_graph, pos, labels=labels, font_size=9, font_weight="bold", font_color="white", ax=ax)

    # Anotaciones
    ax.text(0.1, 2.0, "Límite General (G)\n[Más generales]", fontsize=11, fontweight="bold", color="#2980b9", va="center")
    ax.text(0.1, 0.0, "Límite Específico (S)\n[Más específicas]", fontsize=11, fontweight="bold", color="#27ae60", va="center")
    ax.text(0.1, 1.0, "Espacio de Versiones (VS)\n(Hipótesis intermedias)", fontsize=10, fontstyle="italic", color="#7f8c8d", va="center")

    ax.set_title(title, fontsize=13, fontweight="bold", pad=20)
    ax.axis("off")
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        print(f" Gráfico guardado en: {save_path}")

    if show_plot:
        try:
            plt.show()
        except Exception:
            pass
    
    plt.close(fig)
