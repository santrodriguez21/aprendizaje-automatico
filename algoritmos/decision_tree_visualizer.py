"""
Módulo de Visualización de Árboles de Decisión
Proporciona utilidades para:
- Visualización jerárquica en texto (ASCII / Unicode).
- Visualización gráfica de árboles de decisión mediante Matplotlib.
- Tabla explicativa de cálculos de entropía y ganancia de información.
"""

from typing import List, Dict, Any, Optional, Tuple
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from collections import Counter

from .decision_tree import ID3DecisionTree, DecisionTreeNode, information_gain, entropy


def print_tree_ascii(tree: ID3DecisionTree, node: Optional[DecisionTreeNode] = None, prefix: str = "", is_last: bool = True) -> None:
    """
    Imprime el árbol de decisión en formato jerárquico ASCII / Unicode en la consola.
    """
    if node is None:
        if tree.root is None:
            print("Árbol vacío.")
            return
        node = tree.root
        print(f"🌲 Árbol de Decisión (Objetivo: '{tree.target_attr}')")

    connector = "└── " if is_last else "├── "
    next_prefix = prefix + ("    " if is_last else "│   ")

    if node.is_leaf:
        prob_str = ", ".join([f"{k}: {v:.2f}" for k, v in node.probabilities.items() if v > 0])
        print(f"{prefix}{connector}🍃 [Clase: {node.prediction}] (n={node.samples_count}, Entropía={node.entropy:.3f}, P={{{prob_str}}})")
        return

    node_label = f"[{node.attribute}]" if not node.is_continuous else f"[{node.attribute} (<= {node.threshold})]"
    print(f"{prefix}{connector}🔍 {node_label} (n={node.samples_count}, Entropía={node.entropy:.3f})")

    branch_items = list(node.branches.items())
    for i, (branch_val, child) in enumerate(branch_items):
        is_last_branch = (i == len(branch_items) - 1)
        branch_connector = "└── " if is_last_branch else "├── "
        child_next_prefix = next_prefix + ("    " if is_last_branch else "│   ")

        print(f"{next_prefix}{branch_connector}── ( {branch_val} ) ──>")
        print_tree_ascii(tree, child, child_next_prefix, is_last=True)


def plot_decision_tree(
    tree: ID3DecisionTree,
    figsize: tuple = (12, 8),
    save_path: Optional[str] = None,
    title: Optional[str] = None
) -> None:
    """
    Dibuja un diagrama gráfico estructurado del árbol de decisión con Matplotlib.
    """
    if tree.root is None:
        raise ValueError("El árbol no ha sido entrenado.")

    fig, ax = plt.subplots(figsize=figsize)
    ax.axis('off')

    # Asignar coordenadas a los nodos calculando posiciones x, y
    levels: Dict[int, List[DecisionTreeNode]] = {}
    positions: Dict[DecisionTreeNode, Tuple[float, float]] = {}

    def _get_tree_depth_and_leaves(node: DecisionTreeNode) -> Tuple[int, int]:
        if node.is_leaf or not node.branches:
            return 1, 1
        d_max = 0
        l_sum = 0
        for child in node.branches.values():
            d, l = _get_tree_depth_and_leaves(child)
            d_max = max(d_max, d)
            l_sum += l
        return d_max + 1, l_sum

    max_d, total_leaves = _get_tree_depth_and_leaves(tree.root)

    leaf_counter = [0]

    def _assign_positions(node: DecisionTreeNode, depth: int) -> float:
        if node.is_leaf or not node.branches:
            x = (leaf_counter[0] + 0.5) / max(total_leaves, 1)
            leaf_counter[0] += 1
            y = 1.0 - (depth / max(max_d, 1)) * 0.85
            positions[node] = (x, y)
            return x

        child_xs = []
        for child in node.branches.values():
            child_x = _assign_positions(child, depth + 1)
            child_xs.append(child_x)

        x = sum(child_xs) / len(child_xs)
        y = 1.0 - (depth / max(max_d, 1)) * 0.85
        positions[node] = (x, y)
        return x

    _assign_positions(tree.root, 0)

    # Dibujar conexiones y nodos
    def _draw_edges_and_nodes(node: DecisionTreeNode):
        x, y = positions[node]

        for branch_val, child in node.branches.items():
            cx, cy = positions[child]
            # Línea conectora
            ax.annotate(
                "",
                xy=(cx, cy + 0.03),
                xytext=(x, y - 0.03),
                arrowprops=dict(arrowstyle="->", color="#4A5568", lw=1.5)
            )
            # Etiqueta de la rama
            mid_x = (x + cx) / 2.0
            mid_y = (y + cy) / 2.0
            ax.text(
                mid_x, mid_y,
                str(branch_val),
                fontsize=9,
                color="#1A202C",
                ha='center',
                va='center',
                bbox=dict(boxstyle="round,pad=0.2", facecolor="#EDF2F7", edgecolor="#CBD5E0", alpha=0.9)
            )
            _draw_edges_and_nodes(child)

        # Dibujar caja del nodo
        if node.is_leaf:
            color = "#C6F6D5" if str(node.prediction).lower() in ['si', 'sí', 'buena', 'apto', 'true', '1', 'l'] else "#FED7D7"
            edge_col = "#38A169" if color == "#C6F6D5" else "#E53E3E"
            text_content = f"🍃 {tree.target_attr}: {node.prediction}\nn={node.samples_count} | H={node.entropy:.2f}"
            bbox_props = dict(boxstyle="round,pad=0.5", facecolor=color, edgecolor=edge_col, lw=2)
        else:
            attr_text = f"🔍 {node.attribute}" if not node.is_continuous else f"🔍 {node.attribute} <= {node.threshold:.2f}"
            text_content = f"{attr_text}\nn={node.samples_count}\nH={node.entropy:.2f}"
            bbox_props = dict(boxstyle="round,pad=0.5", facecolor="#EBF8FF", edgecolor="#3182CE", lw=2)

        ax.text(
            x, y,
            text_content,
            ha='center',
            va='center',
            fontsize=9,
            fontweight='bold',
            color="#2D3748",
            bbox=bbox_props
        )

    _draw_edges_and_nodes(tree.root)

    plot_title = title or f"Árbol de Decisión ID3 — Objetivo: '{tree.target_attr}'"
    plt.title(plot_title, fontsize=14, fontweight='bold', pad=20, color="#1A202C")
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✅ Gráfico guardado en: {save_path}")

    plt.show()


def print_entropy_gain_table(
    examples: List[Dict[str, Any]],
    target_attr: str,
    features: List[str]
) -> None:
    """
    Imprime una tabla didáctica con la entropía base y el cálculo de Ganancia de Información
    para cada atributo candidato en el conjunto de ejemplos actual.
    """
    labels = [ex[target_attr] for ex in examples]
    base_ent = entropy(labels)
    total_len = len(examples)

    print(f"\n📊 Análisis de Información (Total instancias: {total_len}, Entropía base H(S) = {base_ent:.4f}):")
    print("-" * 75)
    print(f"{'Atributo':<20} | {'Entropía Residual':<20} | {'Ganancia (Gain)':<18} | {'¿Mejor?':<8}")
    print("-" * 75)

    best_gain = -1.0
    best_attr = None
    results = []

    for attr in features:
        gain, res_ent, _ = information_gain(examples, target_attr, attr)
        results.append((attr, res_ent, gain))
        if gain > best_gain:
            best_gain = gain
            best_attr = attr

    for attr, res_ent, gain in results:
        is_best = "⭐ SÍ" if attr == best_attr else "No"
        print(f"{attr:<20} | {res_ent:<20.4f} | {gain:<18.4f} | {is_best:<8}")
    print("-" * 75)
    print(f"🎯 Atributo seleccionado para división: '{best_attr}' (Ganancia: {best_gain:.4f})\n")
