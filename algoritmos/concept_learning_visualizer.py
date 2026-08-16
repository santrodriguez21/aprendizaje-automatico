"""
Módulo de visualización específico para Aprendizaje Conceptual y Espacio de Versiones.
Incluye funciones para graficar el Espacio de Versiones, retículas completas y trazas paso a paso
de los algoritmos Find-S y Candidate-Elimination.
"""

import sys
import itertools
from typing import List, Dict, Set, Any, Tuple
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


def get_all_version_space_hypotheses(ce: CandidateElimination) -> Tuple[Set[Hypothesis], Set[Hypothesis], Set[Hypothesis]]:
    """
    Calcula todas las hipótesis intermedias del Espacio de Versiones entre S y G.
    Retorna: (S, Intermedias, G)
    """
    intermediates: Set[Hypothesis] = set()

    for s in ce.S:
        if s.is_null():
            continue
        for g in ce.G:
            if not g.is_more_general_or_equal(s):
                continue
            
            # Identificar posiciones donde s tiene un valor específico y g tiene '?'
            diff_indices = [
                i for i, (s_val, g_val) in enumerate(zip(s.values, g.values))
                if g_val == Hypothesis.ANY_SYMBOL and s_val != Hypothesis.ANY_SYMBOL
            ]

            # Generar todas las combinaciones de reemplazo
            for r in range(len(diff_indices) + 1):
                for subset in itertools.combinations(diff_indices, r):
                    new_vals = list(s.values)
                    for idx in subset:
                        new_vals[idx] = Hypothesis.ANY_SYMBOL
                    h = Hypothesis(new_vals)
                    if h not in ce.S and h not in ce.G:
                        intermediates.add(h)

    return ce.S, intermediates, ce.G


def plot_version_space(
    ce: CandidateElimination,
    title: str = "Espacio de Versiones (Version Space)",
    save_path: str = None,
    show_plot: bool = False,
    include_intermediates: bool = True
):
    """
    Genera un gráfico claro, legible y profesional del Espacio de Versiones mostrando
    los límites S, G y (opcionalmente) las hipótesis intermedias que forman la retícula.
    """
    try:
        import matplotlib.pyplot as plt
        from matplotlib.patches import FancyBboxPatch
    except ImportError:
        print("[!] Matplotlib no está disponible. Mostrando diagrama ASCII:")
        print_ascii_version_space(ce)
        return

    s_set, intermediate_set, g_set = get_all_version_space_hypotheses(ce)

    if not include_intermediates:
        intermediate_set = set()

    g_list = sorted(list(g_set), key=lambda h: repr(h))
    int_list = sorted(list(intermediate_set), key=lambda h: repr(h))
    s_list = sorted(list(s_set), key=lambda h: repr(h))
    all_nodes = s_list + int_list + g_list

    # Identificar el nivel de especificidad (k = cantidad de atributos fijos != '?')
    def get_level(h: Hypothesis) -> int:
        if h.is_null():
            return 999
        return sum(1 for v in h.values if v != Hypothesis.ANY_SYMBOL)

    levels = sorted(list(set(get_level(h) for h in all_nodes)))

    
    # Agrupar nodos por nivel de especificidad
    nodes_by_level: Dict[int, List[Hypothesis]] = {}
    for lvl in levels:
        nodes_by_level[lvl] = [h for h in all_nodes if get_level(h) == lvl]

    # Dimensionamiento dinámico de la figura
    max_layer_count = max((len(nodes) for nodes in nodes_by_level.values()), default=1)
    max_repr_len = max((len(repr(h)) for h in all_nodes), default=30)
    
    node_spacing = max(6.5, (max_repr_len * 0.18) + 2.5)
    total_width = max_layer_count * node_spacing
    fig_width = max(18.0, total_width + 7.0)
    fig_height = max(9.5, len(levels) * 2.5)

    fig, ax = plt.subplots(figsize=(fig_width, fig_height), dpi=200)
    fig.patch.set_facecolor("#FAFAFA")
    ax.set_facecolor("#FAFAFA")

    positions: Dict[Hypothesis, Tuple[float, float]] = {}
    start_x = 1.0

    # Asignar coordenadas Y proporcionales de arriba (más general) a abajo (más específica)
    y_min, y_max = 0.6, fig_height * 0.3
    if len(levels) > 1:
        y_step = (y_max - y_min) / (len(levels) - 1)
        level_y = {lvl: y_max - i * y_step for i, lvl in enumerate(levels)}
    else:
        level_y = {levels[0]: 1.5}

    # Posicionar nodos capa por capa de arriba hacia abajo usando baricentro
    for i, lvl in enumerate(levels):
        layer_nodes = nodes_by_level[lvl]
        
        if i == 0:
            # Capa superior (G): ordenar alfabéticamente
            layer_nodes = sorted(layer_nodes, key=lambda h: repr(h))
        else:
            # Capas intermedias e inferiores: ordenar por el baricentro de sus padres superiores
            def get_barycenter(h: Hypothesis) -> float:
                parent_xs = [positions[p][0] for p in positions if p.is_strictly_more_general(h)]
                if parent_xs:
                    return sum(parent_xs) / len(parent_xs)
                return total_width / 2.0
            
            layer_nodes = sorted(layer_nodes, key=lambda h: (get_barycenter(h), repr(h)))

        nodes_by_level[lvl] = layer_nodes
        
        # Asignar coordenadas X equidistantes
        for j, h in enumerate(layer_nodes):
            x = start_x + (j + 1) * (total_width / (len(layer_nodes) + 1))
            positions[h] = (x, level_y[lvl])

    # Dibujar aristas de generalización (de específica hacia general)
    for h_spec in all_nodes:
        for h_gen in all_nodes:
            if h_gen.is_strictly_more_general(h_spec):
                # Verificar relación directa (transitividad mínima)
                is_direct = True
                for h_mid in all_nodes:
                    if h_gen.is_strictly_more_general(h_mid) and h_mid.is_strictly_more_general(h_spec):
                        is_direct = False
                        break
                
                if is_direct and h_spec in positions and h_gen in positions:
                    x1, y1 = positions[h_spec]
                    x2, y2 = positions[h_gen]
                    ax.annotate(
                        "",
                        xy=(x2, y2 - 0.14),
                        xytext=(x1, y1 + 0.14),
                        arrowprops=dict(
                            arrowstyle="-|>",
                            color="#7F8C8D",
                            lw=1.8,
                            ls="--",
                            mutation_scale=14,
                            shrinkA=6,
                            shrinkB=6
                        )
                    )

    # Ajuste de fuente según longitud de caracteres
    font_size = 9 if max_repr_len > 35 else 10

    # Dibujar Cajas de Nodos
    def draw_node_box(h: Hypothesis, x: float, y: float, bg_color: str, border_color: str, text_color: str, tag: str):
        text_str = f"{tag}\n{repr(h)}"
        bbox_props = dict(
            boxstyle="round,pad=0.55,rounding_size=0.3",
            facecolor=bg_color,
            edgecolor=border_color,
            linewidth=2.0,
            alpha=0.95
        )
        ax.text(
            x, y,
            text_str,
            ha="center",
            va="center",
            fontsize=font_size,
            fontweight="bold",
            color=text_color,
            bbox=bbox_props,
            family="monospace"
        )

    # Nodos G (Azul)
    for g in g_list:
        x, y = positions[g]
        draw_node_box(g, x, y, "#EBF5FB", "#2980B9", "#1B4F72", "[Límite General G]")

    # Nodos Intermedios (Gris / Pizarra)
    for h in int_list:
        x, y = positions[h]
        draw_node_box(h, x, y, "#F4F6F7", "#7F8C8D", "#2C3E50", "[Hipótesis VS]")

    # Nodos S (Verde)
    for s in s_list:
        x, y = positions[s]
        draw_node_box(s, x, y, "#E8F8F5", "#27AE60", "#117A65", "[Límite Específico S]")

    # Anotaciones de Capas a la izquierda
    top_lvl = levels[0]
    bottom_lvl = levels[-1]
    
    ax.text(-1.2, level_y[top_lvl], "▲ Más General\n(Límite G)", fontsize=11, fontweight="bold", color="#2980B9", va="center", ha="right")
    
    for lvl in levels[1:-1]:
        ax.text(-1.2, level_y[lvl], f"◆ Capa Intermedia\n(k = {lvl} fijos)", fontsize=10, fontstyle="italic", color="#7F8C8D", va="center", ha="right")
        
    ax.text(-1.2, level_y[bottom_lvl], "▼ Más Específica\n(Límite S)", fontsize=11, fontweight="bold", color="#27AE60", va="center", ha="right")

    ax.set_xlim(-3.5, total_width + 3.5)
    ax.set_ylim(0.0, y_max + 0.7)
    ax.set_title(f"{title}\n(Orden Parcial General-Específico)", fontsize=14, fontweight="bold", pad=18, color="#1A252C")
    ax.axis("off")

    if save_path:
        plt.savefig(save_path, dpi=200, bbox_inches="tight", facecolor=fig.get_facecolor())
        print(f" Gráfico guardado en: {save_path}")

    if show_plot:
        try:
            plt.show()
        except Exception:
            pass

    plt.close(fig)


