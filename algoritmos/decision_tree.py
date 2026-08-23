"""
Módulo de Árboles de Decisión (Decision Trees)
Contiene implementaciones de:
- Funciones de impureza e información: entropía de Shannon, ganancia de información, Gain Ratio.
- Clase DecisionTreeNode: Representación de nodos del árbol (interno o terminal).
- Clase ID3DecisionTree: Algoritmo ID3 con extensiones para min_info_gain, max_depth,
  atributos continuos, manejo de valores no vistos, imputación de faltantes y poda.
"""

import math
from collections import Counter
from typing import List, Dict, Any, Tuple, Optional, Union, Set


def entropy(labels: List[Any]) -> float:
    """
    Calcula la entropía de Shannon para una lista de etiquetas.
    H(S) = - sum(p_i * log2(p_i))
    """
    if not labels:
        return 0.0
    total = len(labels)
    counts = Counter(labels)
    ent = 0.0
    for count in counts.values():
        if count > 0:
            p = count / total
            ent -= p * math.log2(p)
    return ent


def information_gain(
    examples: List[Dict[str, Any]],
    target_attr: str,
    split_attr: str,
    is_continuous: bool = False,
    threshold: Optional[float] = None
) -> Tuple[float, float, Dict[Any, List[Dict[str, Any]]]]:
    """
    Calcula la Ganancia de Información al dividir el conjunto según un atributo.
    Ganancia(S, A) = Entropía(S) - sum(|S_v|/|S| * Entropía(S_v))

    Devuelve: (ganancia, entropia_residual, subsets_por_rama)
    """
    if not examples:
        return 0.0, 0.0, {}

    total_len = len(examples)
    total_labels = [ex[target_attr] for ex in examples]
    base_entropy = entropy(total_labels)

    subsets: Dict[Any, List[Dict[str, Any]]] = {}

    if is_continuous and threshold is not None:
        subsets[f"<= {threshold}"] = []
        subsets[f"> {threshold}"] = []
        for ex in examples:
            val = ex.get(split_attr)
            if val is None:
                continue
            if float(val) <= threshold:
                subsets[f"<= {threshold}"].append(ex)
            else:
                subsets[f"> {threshold}"].append(ex)
    else:
        for ex in examples:
            val = ex.get(split_attr)
            if val not in subsets:
                subsets[val] = []
            subsets[val].append(ex)

    weighted_entropy = 0.0
    for branch_val, subset in subsets.items():
        if subset:
            sub_labels = [ex[target_attr] for ex in subset]
            weight = len(subset) / total_len
            weighted_entropy += weight * entropy(sub_labels)

    gain = base_entropy - weighted_entropy
    return gain, weighted_entropy, subsets


def split_information(subsets: Dict[Any, List[Dict[str, Any]]], total_len: int) -> float:
    """
    Calcula el SplitInformation de una partición:
    SplitInformation(S, A) = - sum(|S_v|/|S| * log2(|S_v|/|S|))
    """
    if total_len == 0:
        return 0.0
    split_info = 0.0
    for subset in subsets.values():
        if subset:
            p = len(subset) / total_len
            split_info -= p * math.log2(p)
    return split_info


def gain_ratio(
    examples: List[Dict[str, Any]],
    target_attr: str,
    split_attr: str
) -> float:
    """
    Calcula la Tasa de Ganancia (Gain Ratio) para penalizar atributos con muchos valores:
    GainRatio(S, A) = Ganancia(S, A) / SplitInformation(S, A)
    """
    gain, _, subsets = information_gain(examples, target_attr, split_attr)
    split_info = split_information(subsets, len(examples))
    if split_info == 0:
        return 0.0
    return gain / split_info


class DecisionTreeNode:
    """
    Nodo de un Árbol de Decisión.
    Puede ser un nodo de decisión interno o un nodo hoja (terminal).
    """

    def __init__(
        self,
        attribute: Optional[str] = None,
        is_leaf: bool = False,
        prediction: Optional[Any] = None,
        probabilities: Optional[Dict[Any, float]] = None,
        samples_count: int = 0,
        entropy_val: float = 0.0,
        is_continuous: bool = False,
        threshold: Optional[float] = None
    ):
        self.attribute = attribute
        self.is_leaf = is_leaf
        self.prediction = prediction
        self.probabilities = probabilities or {}
        self.samples_count = samples_count
        self.entropy = entropy_val
        self.is_continuous = is_continuous
        self.threshold = threshold
        self.branches: Dict[Any, 'DecisionTreeNode'] = {}
        self.default_child_prediction: Optional[Any] = prediction

    def add_branch(self, branch_value: Any, child_node: 'DecisionTreeNode') -> None:
        self.branches[branch_value] = child_node

    def is_terminal(self) -> bool:
        return self.is_leaf or len(self.branches) == 0

    def __repr__(self) -> str:
        if self.is_leaf:
            return f"Leaf(pred={self.prediction}, n={self.samples_count})"
        if self.is_continuous:
            return f"Node({self.attribute} <= {self.threshold}, branches={list(self.branches.keys())})"
        return f"Node({self.attribute}, branches={list(self.branches.keys())})"


class ID3DecisionTree:
    """
    Implementación completa del clasificador de Árbol de Decisión basado en ID3.
    Soporta:
    - Criterios de división: 'gain' (Ganancia de Información) o 'gain_ratio' (Gain Ratio).
    - Hiperparámetro min_info_gain (umbral mínimo de ganancia para continuar dividiendo).
    - Hiperparámetro max_depth (profundidad máxima del árbol).
    - Atributos continuos (encuentra dinámicamente el mejor umbral de corte).
    - Manejo de valores no vistos en test (retorna la clase mayoritaria local).
    """

    def __init__(
        self,
        criterion: str = 'gain',
        min_info_gain: float = 0.0,
        max_depth: Optional[int] = None,
        continuous_attributes: Optional[Set[str]] = None
    ):
        self.criterion = criterion
        self.min_info_gain = min_info_gain
        self.max_depth = max_depth
        self.continuous_attributes = continuous_attributes or set()
        self.root: Optional[DecisionTreeNode] = None
        self.target_attr: Optional[str] = None
        self.classes_: List[Any] = []
        self.feature_names_: List[str] = []

    def fit(
        self,
        examples: List[Dict[str, Any]],
        target_attr: str,
        features: Optional[List[str]] = None
    ) -> 'ID3DecisionTree':
        """
        Entrena el árbol de decisión sobre una lista de diccionarios que representan ejemplos.
        """
        if not examples:
            raise ValueError("El conjunto de entrenamiento no puede estar vacío.")

        self.target_attr = target_attr
        labels = [ex[target_attr] for ex in examples]
        self.classes_ = sorted(list(set(labels)))

        if features is None:
            features = [k for k in examples[0].keys() if k != target_attr]
        self.feature_names_ = list(features)

        self.root = self._build_tree(examples, features, depth=0)
        return self

    def _build_tree(
        self,
        examples: List[Dict[str, Any]],
        available_features: List[str],
        depth: int
    ) -> DecisionTreeNode:
        labels = [ex[self.target_attr] for ex in examples]
        counts = Counter(labels)
        majority_class = counts.most_common(1)[0][0]
        node_entropy = entropy(labels)
        total_samples = len(examples)
        probs = {c: counts.get(c, 0) / total_samples for c in self.classes_}

        # Caso base 1: Todos los ejemplos tienen la misma etiqueta (nodo puro)
        if len(counts) == 1:
            return DecisionTreeNode(
                is_leaf=True,
                prediction=majority_class,
                probabilities=probs,
                samples_count=total_samples,
                entropy_val=node_entropy
            )

        # Caso base 2: No quedan atributos o se alcanzó la profundidad máxima
        if not available_features or (self.max_depth is not None and depth >= self.max_depth):
            return DecisionTreeNode(
                is_leaf=True,
                prediction=majority_class,
                probabilities=probs,
                samples_count=total_samples,
                entropy_val=node_entropy
            )

        # Buscar el mejor atributo para dividir
        best_attr = None
        best_metric_val = -1.0
        best_subsets: Dict[Any, List[Dict[str, Any]]] = {}
        best_is_continuous = False
        best_threshold: Optional[float] = None

        for attr in available_features:
            is_cont = attr in self.continuous_attributes

            if is_cont:
                # Encontrar el mejor punto de corte continuo
                gain, thresh, subsets = self._best_continuous_split(examples, attr)
                metric_val = gain
                if metric_val > best_metric_val:
                    best_metric_val = metric_val
                    best_attr = attr
                    best_subsets = subsets
                    best_is_continuous = True
                    best_threshold = thresh
            else:
                if self.criterion == 'gain_ratio':
                    metric_val = gain_ratio(examples, self.target_attr, attr)
                    gain, _, subsets = information_gain(examples, self.target_attr, attr)
                else:
                    gain, _, subsets = information_gain(examples, self.target_attr, attr)
                    metric_val = gain

                if metric_val > best_metric_val:
                    best_metric_val = metric_val
                    best_attr = attr
                    best_subsets = subsets
                    best_is_continuous = False
                    best_threshold = None

        # Caso base 3: La mejor ganancia no supera el umbral min_info_gain
        if best_attr is None or best_metric_val < self.min_info_gain or best_metric_val <= 0.0:
            return DecisionTreeNode(
                is_leaf=True,
                prediction=majority_class,
                probabilities=probs,
                samples_count=total_samples,
                entropy_val=node_entropy
            )

        # Crear nodo interno
        node = DecisionTreeNode(
            attribute=best_attr,
            is_leaf=False,
            prediction=majority_class,
            probabilities=probs,
            samples_count=total_samples,
            entropy_val=node_entropy,
            is_continuous=best_is_continuous,
            threshold=best_threshold
        )

        remaining_features = [f for f in available_features if f != best_attr or best_is_continuous]

        for branch_val, subset in best_subsets.items():
            if not subset:
                # Rama vacía: hoja con la clase mayoritaria del nodo padre
                child = DecisionTreeNode(
                    is_leaf=True,
                    prediction=majority_class,
                    probabilities=probs,
                    samples_count=0,
                    entropy_val=0.0
                )
            else:
                child = self._build_tree(subset, remaining_features, depth + 1)
            node.add_branch(branch_val, child)

        return node

    def _best_continuous_split(
        self,
        examples: List[Dict[str, Any]],
        attr: str
    ) -> Tuple[float, Optional[float], Dict[str, List[Dict[str, Any]]]]:
        """
        Encuentra el punto de corte óptimo para un atributo numérico continuo.
        """
        sorted_examples = sorted(
            [ex for ex in examples if ex.get(attr) is not None],
            key=lambda x: float(x[attr])
        )
        if len(sorted_examples) < 2:
            return 0.0, None, {}

        candidate_thresholds: List[float] = []
        for i in range(len(sorted_examples) - 1):
            if sorted_examples[i][self.target_attr] != sorted_examples[i + 1][self.target_attr]:
                v1 = float(sorted_examples[i][attr])
                v2 = float(sorted_examples[i + 1][attr])
                candidate_thresholds.append((v1 + v2) / 2.0)

        if not candidate_thresholds:
            v_min = float(sorted_examples[0][attr])
            v_max = float(sorted_examples[-1][attr])
            candidate_thresholds.append((v_min + v_max) / 2.0)

        best_gain = -1.0
        best_thresh = candidate_thresholds[0]
        best_subsets: Dict[str, List[Dict[str, Any]]] = {}

        for thresh in candidate_thresholds:
            gain, _, subsets = information_gain(
                examples, self.target_attr, attr, is_continuous=True, threshold=thresh
            )
            if gain > best_gain:
                best_gain = gain
                best_thresh = thresh
                best_subsets = subsets

        return best_gain, best_thresh, best_subsets

    def predict_one(self, instance: Dict[str, Any]) -> Any:
        """
        Predice la etiqueta para una única instancia.
        """
        if self.root is None:
            raise ValueError("El árbol debe ser entrenado antes de predecir.")

        curr = self.root
        while not curr.is_leaf:
            attr_val = instance.get(curr.attribute)

            if curr.is_continuous:
                if attr_val is None:
                    return curr.prediction
                key = f"<= {curr.threshold}" if float(attr_val) <= curr.threshold else f"> {curr.threshold}"
                if key in curr.branches:
                    curr = curr.branches[key]
                else:
                    return curr.prediction
            else:
                if attr_val in curr.branches:
                    curr = curr.branches[attr_val]
                else:
                    # Valor no visto durante el entrenamiento: se retorna la predicción mayoritaria
                    return curr.prediction

        return curr.prediction

    def predict(self, instances: List[Dict[str, Any]]) -> List[Any]:
        """
        Predice las etiquetas para una lista de instancias.
        """
        return [self.predict_one(inst) for inst in instances]

    def predict_proba_one(self, instance: Dict[str, Any]) -> Dict[Any, float]:
        """
        Predice la distribución de probabilidad de las clases para una instancia.
        """
        if self.root is None:
            raise ValueError("El árbol debe ser entrenado antes de predecir.")

        curr = self.root
        while not curr.is_leaf:
            attr_val = instance.get(curr.attribute)
            if curr.is_continuous:
                if attr_val is None:
                    return curr.probabilities
                key = f"<= {curr.threshold}" if float(attr_val) <= curr.threshold else f"> {curr.threshold}"
                if key in curr.branches:
                    curr = curr.branches[key]
                else:
                    return curr.probabilities
            else:
                if attr_val in curr.branches:
                    curr = curr.branches[attr_val]
                else:
                    return curr.probabilities

        return curr.probabilities

    def to_rules(self) -> List[str]:
        """
        Exporta las ramas del árbol de decisión a un conjunto de reglas lógicas DNF (IF ... THEN ...).
        """
        if self.root is None:
            return []

        rules = []

        def _traverse(node: DecisionTreeNode, current_conditions: List[str]):
            if node.is_leaf:
                cond_str = " AND ".join(current_conditions) if current_conditions else "TRUE"
                rules.append(f"IF {cond_str} THEN {self.target_attr} = {node.prediction}")
                return

            for branch_val, child in node.branches.items():
                if node.is_continuous:
                    cond = f"({node.attribute} {branch_val})"
                else:
                    cond = f"({node.attribute} == '{branch_val}')"
                _traverse(child, current_conditions + [cond])

        _traverse(self.root, [])
        return rules
