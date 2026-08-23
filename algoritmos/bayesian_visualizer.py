"""
Módulo de Visualización para Aprendizaje Bayesiano
Proporciona utilidades para:
- Desglose textual detallado y trazas explicativas paso a paso.
- Gráficos de barras comparativos de probabilidades a priori vs a posteriori.
- Visualización de tablas de verosimilitud condicional.
"""

from typing import Dict, Any, Optional
import matplotlib.pyplot as plt
from .bayesian import NaiveBayesClassifier


def print_bayesian_trace(nb: NaiveBayesClassifier, instance: Dict[str, Any]) -> None:
    """
    Imprime una traza pedagógica en la consola con el desglose de todos los cálculos
    de Naïve Bayes para una instancia de consulta.
    """
    exp = nb.explain_prediction(instance)

    print(f"\n🔮 Inferencia Naïve Bayes (CBS) para la instancia:")
    print(f"   x = {instance}\n")
    print("=" * 80)

    for c, data in exp['classes'].items():
        prior = data['prior']
        unnorm = data['unnormalized_product']
        print(f"📌 Clase: '{c}'")
        print(f"   • Probabilidad a Priori P({c}) = {prior:.4f}")
        print("   • Verosimilitudes condicionales P(a_i | c):")
        for cond_name, p_val in data['likelihoods'].items():
            print(f"     - {cond_name:<30} = {p_val:.4f}")
        print(f"   • Producto no normalizado P({c}) ∏ P(a_i | {c}) = {unnorm:.6e}")
        print("-" * 80)

    print(f"\n🎯 Distribución a Posteriori Normalizada P(c | x):")
    for c, post_prob in exp['posterior_probabilities'].items():
        bar = "█" * int(post_prob * 30)
        print(f"   • P({c:<10} | x) = {post_prob:>6.2%}  {bar}")

    pred = exp['predicted_class']
    print(f"\n🏆 Predicción Final (MAP): '{pred}' (Confianza: {exp['posterior_probabilities'][pred]:.2%})\n")


def plot_prior_and_posterior(
    nb: NaiveBayesClassifier,
    instance: Dict[str, Any],
    figsize: tuple = (10, 5),
    save_path: Optional[str] = None,
    title: Optional[str] = None
) -> None:
    """
    Genera un gráfico comparativo de barras entre las probabilidades a priori P(c)
    y las probabilidades a posteriori P(c | x).
    """
    exp = nb.explain_prediction(instance)
    classes = list(exp['classes'].keys())
    priors = [exp['classes'][c]['prior'] for c in classes]
    posteriors = [exp['posterior_probabilities'][c] for c in classes]

    x_indices = range(len(classes))
    bar_width = 0.35

    fig, ax = plt.subplots(figsize=figsize)
    bars_prior = ax.bar([i - bar_width / 2 for i in x_indices], priors, bar_width, label='A Priori P(c)', color='#63B3ED', alpha=0.9)
    bars_post = ax.bar([i + bar_width / 2 for i in x_indices], posteriors, bar_width, label='A Posteriori P(c | x)', color='#48BB78', alpha=0.9)

    ax.set_xlabel('Clases', fontsize=12, fontweight='bold', labelpad=10)
    ax.set_ylabel('Probabilidad', fontsize=12, fontweight='bold', labelpad=10)
    ax.set_title(title or f"Comparativa A Priori vs A Posteriori (Predicción: {exp['predicted_class']})", fontsize=13, fontweight='bold', pad=15)
    ax.set_xticks(list(x_indices))
    ax.set_xticklabels([str(c) for c in classes], fontsize=11)
    ax.set_ylim(0, 1.05)
    ax.legend(fontsize=11)
    ax.grid(axis='y', linestyle='--', alpha=0.4)

    # Etiquetas numéricas sobre las barras
    for bar in bars_prior:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, yval + 0.02, f"{yval:.2f}", ha='center', va='bottom', fontsize=9)

    for bar in bars_post:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, yval + 0.02, f"{yval:.2f}", ha='center', va='bottom', fontsize=9, fontweight='bold')

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✅ Gráfico guardado en: {save_path}")
    plt.show()
