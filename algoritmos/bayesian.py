"""
Módulo de Aprendizaje Bayesiano (Bayesian Learning)
Contiene implementaciones de:
- NaiveBayesClassifier (Clasificador Bayesiano Sencillo - CBS):
  - Estimación de probabilidades a priori y verosimilitud condicional.
  - Suavizado por m-estimador y suavizado de Laplace.
  - Inferencia logarítmica para estabilidad numérica.
  - Explicabilidad paso a paso de predicciones.
- BayesOptimalClassifier (Clasificador Bayesiano Óptimo).
"""

import math
from collections import Counter, defaultdict
from typing import List, Dict, Any, Tuple, Optional, Union, Set


class NaiveBayesClassifier:
    """
    Clasificador Bayesiano Sencillo (Naïve Bayes / CBS).
    Asume independencia condicional entre los atributos dado el valor del concepto objetivo:
    P(a1, a2, ..., ad | c) = Prod_{i=1}^d P(ai | c)
    """

    def __init__(
        self,
        m: float = 0.0,
        use_laplace: bool = False,
        default_p: Optional[float] = None
    ):
        """
        Parámetros:
        - m: Tamaño equivalente de muestra (m-estimador). Si m=0, usa frecuencias simples (ML).
        - use_laplace: Si es True, fija m = |Val(A)| y p = 1 / |Val(A)|.
        - default_p: Probabilidad a priori por defecto para el m-estimador. Si es None, usa 1 / |Val(A)|.
        """
        self.m = m
        self.use_laplace = use_laplace
        self.default_p = default_p

        self.classes_: List[Any] = []
        self.class_counts_: Dict[Any, int] = {}
        self.total_samples_: int = 0
        self.priors_: Dict[Any, float] = {}

        # feature_values_[attr] = set de valores observados o posibles
        self.feature_values_: Dict[str, Set[Any]] = defaultdict(set)
        # conditional_counts_[attr][class_val][attr_val] = count
        self.conditional_counts_: Dict[str, Dict[Any, Dict[Any, int]]] = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
        # conditional_probs_[attr][class_val][attr_val] = prob
        self.conditional_probs_: Dict[str, Dict[Any, Dict[Any, float]]] = defaultdict(lambda: defaultdict(dict))

        self.feature_names_: List[str] = []
        self.target_attr_: Optional[str] = None

    def fit(
        self,
        examples: List[Dict[str, Any]],
        target_attr: str,
        features: Optional[List[str]] = None,
        domains: Optional[Dict[str, List[Any]]] = None
    ) -> 'NaiveBayesClassifier':
        """
        Entrena el clasificador estimando probabilidades a priori y condicionales.
        """
        if not examples:
            raise ValueError("El conjunto de entrenamiento no puede estar vacío.")

        self.target_attr_ = target_attr
        self.total_samples_ = len(examples)

        if features is None:
            features = [k for k in examples[0].keys() if k != target_attr]
        self.feature_names_ = list(features)

        # Si se pasan dominios predefinidos, registrarlos
        if domains:
            for attr, vals in domains.items():
                self.feature_values_[attr].update(vals)

        # 1. Contar frecuencias de clases
        labels = [ex[target_attr] for ex in examples]
        self.class_counts_ = dict(Counter(labels))
        self.classes_ = sorted(list(self.class_counts_.keys()))

        # Probabilidades a priori P(c)
        for c in self.classes_:
            self.priors_[c] = self.class_counts_[c] / self.total_samples_

        # 2. Contar frecuencias condicionales
        for ex in examples:
            c = ex[target_attr]
            for attr in self.feature_names_:
                val = ex.get(attr)
                if val is not None:
                    self.feature_values_[attr].add(val)
                    self.conditional_counts_[attr][c][val] += 1

        # 3. Calcular probabilidades condicionales P(ai | c) con m-estimador / Laplace
        for attr in self.feature_names_:
            num_vals = len(self.feature_values_[attr])
            p_prior = self.default_p if self.default_p is not None else (1.0 / max(num_vals, 1))
            effective_m = float(num_vals) if self.use_laplace else self.m

            for c in self.classes_:
                n_c = self.class_counts_[c]
                for val in self.feature_values_[attr]:
                    n_c_a = self.conditional_counts_[attr][c].get(val, 0)
                    if effective_m > 0:
                        prob = (n_c_a + effective_m * p_prior) / (n_c + effective_m)
                    else:
                        prob = n_c_a / n_c if n_c > 0 else 0.0
                    self.conditional_probs_[attr][c][val] = prob

        return self

    def _get_cond_prob(self, attr: str, val: Any, class_val: Any) -> float:
        """Devuelve P(attr=val | class_val), aplicando m-estimador para valores no vistos."""
        if val in self.conditional_probs_[attr][class_val]:
            return self.conditional_probs_[attr][class_val][val]

        # Si el valor no fue visto durante el entrenamiento para esa clase:
        num_vals = max(len(self.feature_values_[attr]), 1)
        p_prior = self.default_p if self.default_p is not None else (1.0 / num_vals)
        effective_m = float(num_vals) if self.use_laplace else self.m

        if effective_m > 0:
            n_c = self.class_counts_[class_val]
            return (0.0 + effective_m * p_prior) / (n_c + effective_m)
        return 1e-12  # Evitar log(0)

    def predict_one(self, instance: Dict[str, Any]) -> Any:
        """
        Predice la clase para una única instancia usando la regla MAP en escala logarítmica.
        """
        scores = self.predict_log_proba_one(instance)
        return max(scores.items(), key=lambda item: item[1])[0]

    def predict(self, instances: List[Dict[str, Any]]) -> List[Any]:
        """Predice las clases para una lista de instancias."""
        return [self.predict_one(inst) for inst in instances]

    def predict_log_proba_one(self, instance: Dict[str, Any]) -> Dict[Any, float]:
        """
        Calcula el puntaje logarítmico proporcional a log P(c) + sum log P(ai | c).
        """
        scores: Dict[Any, float] = {}
        for c in self.classes_:
            log_score = math.log(max(self.priors_[c], 1e-12))
            for attr in self.feature_names_:
                val = instance.get(attr)
                if val is not None:
                    p_cond = self._get_cond_prob(attr, val, c)
                    log_score += math.log(max(p_cond, 1e-12))
            scores[c] = log_score
        return scores

    def predict_proba_one(self, instance: Dict[str, Any]) -> Dict[Any, float]:
        """
        Calcula las probabilidades a posteriori normalizadas P(c | x) mediante Softmax / normalización exponencial.
        """
        log_scores = self.predict_log_proba_one(instance)
        max_log = max(log_scores.values())
        exp_scores = {c: math.exp(score - max_log) for c, score in log_scores.items()}
        total_exp = sum(exp_scores.values())
        return {c: score / total_exp for c, score in exp_scores.items()}

    def predict_proba(self, instances: List[Dict[str, Any]]) -> List[Dict[Any, float]]:
        """Calcula probabilidades a posteriori para una lista de instancias."""
        return [self.predict_proba_one(inst) for inst in instances]

    def explain_prediction(self, instance: Dict[str, Any]) -> Dict[str, Any]:
        """
        Devuelve una traza estructurada con todos los cálculos (a priori, verosimilitud y a posteriori).
        """
        explanation: Dict[str, Any] = {
            'instance': instance,
            'classes': {}
        }

        for c in self.classes_:
            prior = self.priors_[c]
            likelihoods: Dict[str, float] = {}
            product = prior

            for attr in self.feature_names_:
                val = instance.get(attr)
                if val is not None:
                    p_cond = self._get_cond_prob(attr, val, c)
                    likelihoods[f"P({attr}={val}|{c})"] = p_cond
                    product *= p_cond

            explanation['classes'][c] = {
                'prior': prior,
                'likelihoods': likelihoods,
                'unnormalized_product': product
            }

        posteriors = self.predict_proba_one(instance)
        best_class = max(posteriors.items(), key=lambda x: x[1])[0]
        explanation['posterior_probabilities'] = posteriors
        explanation['predicted_class'] = best_class
        return explanation


class BayesOptimalClassifier:
    """
    Clasificador Bayesiano Óptimo (Bayes Optimal Classifier).
    Combina las predicciones de todas las hipótesis del espacio H,
    ponderadas por su probabilidad a posteriori P(h | D):
    P(y | x) = sum_{h in H} P(y | h, x) * P(h | D)
    """

    def __init__(self, hypotheses: List[Any], hypothesis_posteriors: List[float]):
        if len(hypotheses) != len(hypothesis_posteriors):
            raise ValueError("La cantidad de hipótesis debe coincidir con la cantidad de probabilidades.")
        total_prob = sum(hypothesis_posteriors)
        self.hypotheses = hypotheses
        self.posteriors = [p / total_prob for p in hypothesis_posteriors]

    def predict_proba_one(self, instance: Any) -> Dict[Any, float]:
        class_probs: Dict[Any, float] = defaultdict(float)
        for h, p_h in zip(self.hypotheses, self.posteriors):
            pred = h.predict_one(instance) if hasattr(h, 'predict_one') else h(instance)
            class_probs[pred] += p_h
        return dict(class_probs)

    def predict_one(self, instance: Any) -> Any:
        probs = self.predict_proba_one(instance)
        return max(probs.items(), key=lambda x: x[1])[0]

    def predict(self, instances: List[Any]) -> List[Any]:
        return [self.predict_one(inst) for inst in instances]
