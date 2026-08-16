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

    # Configuración de capas y posiciones
    fig, ax = plt.subplots(figsize=(16, 9), dpi=180)
    fig.patch.set_facecolor("#FAFAFA")
    ax.set_facecolor("#FAFAFA")

    # Posiciones X de cada capa
    g_list = sorted(list(g_set), key=lambda h: repr(h))
    int_list = sorted(list(intermediate_set), key=lambda h: repr(h))
    s_list = sorted(list(s_set), key=lambda h: repr(h))

    positions: Dict[Hypothesis, Tuple[float, float]] = {}

    total_width = 14.0
    start_x = 1.0

    # Capa G (Superior, y=2.5)
    for i, g in enumerate(g_list):
        x = start_x + (i + 1) * (total_width / (len(g_list) + 1))
        positions[g] = (x, 2.5)

    # Capa Intermedia (Medio, y=1.5)
    for i, h in enumerate(int_list):
        x = start_x + (i + 1) * (total_width / (len(int_list) + 1))
        positions[h] = (x, 1.5)

    # Capa S (Inferior, y=0.5)
    for i, s in enumerate(s_list):
        x = start_x + (i + 1) * (total_width / (len(s_list) + 1))
        positions[s] = (x, 0.5)

    # Dibujar aristas de generalización (S -> Intermedias -> G o S -> G)
    all_nodes = s_list + int_list + g_list

    for h_spec in all_nodes:
        for h_gen in all_nodes:
            if h_gen.is_strictly_more_general(h_spec):
                # Verificar si es una relación directa (sin ningún nodo intermedio en nuestro conjunto)
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
                        xy=(x2, y2 - 0.12),
                        xytext=(x1, y1 + 0.12),
                        arrowprops=dict(
                            arrowstyle="-|>",
                            color="#7F8C8D",
                            lw=1.6,
                            ls="--",
                            mutation_scale=14,
                            shrinkA=5,
                            shrinkB=5
                        )
                    )

    # Dibujar Cajas de Nodos con formato nítido y texto completo
    def draw_node_box(h: Hypothesis, x: float, y: float, bg_color: str, border_color: str, text_color: str, tag: str):
        text_str = f"{tag}\n{repr(h)}"
        bbox_props = dict(
            boxstyle="round,pad=0.5,rounding_size=0.3",
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
            fontsize=10,
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
    ax.text(-0.5, 2.5, "▲ Más General\n(Límite G)", fontsize=11, fontweight="bold", color="#2980B9", va="center", ha="right")
    if int_list:
        ax.text(-0.5, 1.5, "◆ Espacio de Versiones\n(Consistentes)", fontsize=10, fontstyle="italic", color="#7F8C8D", va="center", ha="right")
    ax.text(-0.5, 0.5, "▼ Más Específica\n(Límite S)", fontsize=11, fontweight="bold", color="#27AE60", va="center", ha="right")

    ax.set_xlim(-2.5, 17.5)
    ax.set_ylim(0.0, 3.2)
    ax.set_title(f"{title}\n(Orden Parcial General-Específico)", fontsize=14, fontweight="bold", pad=15, color="#1A252C")
    ax.axis("off")

    if save_path:
        plt.savefig(save_path, dpi=200, bbox_inches="tight", facecolor=fig.get_facecolor())
        print(f" Gráfico nítido guardado en: {save_path}")

    if show_plot:
        try:
            plt.show()
        except Exception:
            pass

    plt.close(fig)
