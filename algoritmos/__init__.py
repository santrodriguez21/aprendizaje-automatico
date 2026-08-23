"""
Módulo de algoritmos de Aprendizaje Automático.
Provee implementaciones didácticas y visualizadores para:
1. Concept Learning (Find-S, Candidate-Elimination, Espacio de Versiones).
2. Decision Trees (ID3, Entropía, Ganancia de Información, Gain Ratio, reglas DNF).
3. Bayesian Learning (Naïve Bayes / CBS con m-estimador y Laplace, Clasificador Bayesiano Óptimo).
"""

from .concept_learning import Hypothesis, FindS, CandidateElimination
from .concept_learning_visualizer import (
    plot_version_space,
    print_step_by_step_trace,
    print_ascii_version_space,
)

from .decision_tree import (
    ID3DecisionTree,
    DecisionTreeNode,
    entropy,
    information_gain,
    gain_ratio,
    split_information,
)
from .decision_tree_visualizer import (
    print_tree_ascii,
    plot_decision_tree,
    print_entropy_gain_table,
)

from .bayesian import (
    NaiveBayesClassifier,
    BayesOptimalClassifier,
)
from .bayesian_visualizer import (
    print_bayesian_trace,
    plot_prior_and_posterior,
)

__all__ = [
    # Concept Learning
    "Hypothesis",
    "FindS",
    "CandidateElimination",
    "plot_version_space",
    "print_step_by_step_trace",
    "print_ascii_version_space",
    # Decision Trees
    "ID3DecisionTree",
    "DecisionTreeNode",
    "entropy",
    "information_gain",
    "gain_ratio",
    "split_information",
    "print_tree_ascii",
    "plot_decision_tree",
    "print_entropy_gain_table",
    # Bayesian Learning
    "NaiveBayesClassifier",
    "BayesOptimalClassifier",
    "print_bayesian_trace",
    "plot_prior_and_posterior",
]
