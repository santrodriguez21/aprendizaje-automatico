"""
Módulo de Aprendizaje Conceptual (Concept Learning)
Contiene implementaciones de:
- Clase Hypothesis: Representación y operadores de hipótesis.
- FindS: Algoritmo para encontrar la hipótesis más específica.
- CandidateElimination: Algoritmo para calcular el Espacio de Versiones (límites S y G).
"""

from typing import List, Dict, Any, Tuple, Optional, Set
import copy


class Hypothesis:
    """
    Representa una hipótesis expresada como conjunción de restricciones sobre atributos.
    Símbolos especiales:
    - '?' : Acepta cualquier valor para ese atributo (general).
    - 'Ø' : No acepta ningún valor (específica / nula).
    """

    NULL_SYMBOL = 'Ø'
    ANY_SYMBOL = '?'

    def __init__(self, values: List[str]):
        self.values = list(values)

    def is_null(self) -> bool:
        """Una hipótesis es nula si al menos un atributo contiene 'Ø'."""
        return any(v == self.NULL_SYMBOL for v in self.values)

    def matches(self, instance: List[str]) -> bool:
        """
        Evalúa si una instancia x satisface la hipótesis h (h(x) == 1).
        """
        if self.is_null():
            return False
        for h_val, x_val in zip(self.values, instance):
            if h_val != self.ANY_SYMBOL and h_val != x_val:
                return False
        return True

    def is_more_general_or_equal(self, other: 'Hypothesis') -> bool:
        """
        Devuelve True si self >=_g other (self es más general o igual que other).
        """
        # Si other es semánticamente nula, cualquier hipótesis es más general o igual
        if other.is_null():
            return True
        # Si self es nula pero other no, self no es más general
        if self.is_null():
            return False

        for s_val, o_val in zip(self.values, other.values):
            if s_val == self.ANY_SYMBOL:
                continue
            if s_val != o_val:
                return False
        return True

    def is_more_specific_or_equal(self, other: 'Hypothesis') -> bool:
        """Devuelve True si self <=_g other."""
        return other.is_more_general_or_equal(self)

    def is_strictly_more_general(self, other: 'Hypothesis') -> bool:
        """Devuelve True si self >_g other."""
        return self.is_more_general_or_equal(other) and self != other

    def is_strictly_more_specific(self, other: 'Hypothesis') -> bool:
        """Devuelve True si self <_g other."""
        return self.is_more_specific_or_equal(other) and self != other

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Hypothesis):
            return False
        # Si ambas son nulas, son semánticamente iguales
        if self.is_null() and other.is_null():
            return True
        return self.values == other.values

    def __hash__(self) -> int:
        if self.is_null():
            return hash(("NULL", len(self.values)))
        return hash(tuple(self.values))

    def __lt__(self, other: 'Hypothesis') -> bool:
        if not isinstance(other, Hypothesis):
            return NotImplemented
        return self.values < other.values

    def __repr__(self) -> str:
        return f"<{', '.join(self.values)}>"



class FindS:
    """
    Implementación didáctica del algoritmo Find-S.
    Registra el historial paso a paso para fines de visualización.
    """

    def __init__(self, num_attributes: int, attribute_names: Optional[List[str]] = None):
        self.num_attributes = num_attributes
        self.attribute_names = attribute_names or [f"Attr_{i}" for i in range(num_attributes)]
        self.hypothesis = Hypothesis([Hypothesis.NULL_SYMBOL] * num_attributes)
        self.history: List[Dict[str, Any]] = []

    def fit(self, X: List[List[str]], y: List[int or str]) -> 'FindS':
        """
        Entrena el algoritmo con las instancias X y etiquetas y (1/'SÍ' para positivo, 0/'NO' para negativo).
        """
        self.hypothesis = Hypothesis([Hypothesis.NULL_SYMBOL] * self.num_attributes)
        self.history = [{
            "step": 0,
            "instance": None,
            "label": None,
            "action": "Inicialización con hipótesis más específica",
            "hypothesis": copy.deepcopy(self.hypothesis)
        }]

        for idx, (instance, label) in enumerate(zip(X, y), start=1):
            is_positive = label in (1, "1", "SI", "SÍ", "yes", "Yes", True)

            if is_positive:
                if self.hypothesis.is_null():
                    # Primera instancia positiva: toma los valores literales
                    self.hypothesis = Hypothesis(list(instance))
                    action = "Primera instancia positiva: adopta valores del ejemplo"
                else:
                    # Generalizar donde no coincida
                    new_values = []
                    for h_val, x_val in zip(self.hypothesis.values, instance):
                        if h_val == x_val:
                            new_values.append(h_val)
                        else:
                            new_values.append(Hypothesis.ANY_SYMBOL)
                    self.hypothesis = Hypothesis(new_values)
                    action = "Instancia positiva: generalización mínima ('?' en diferencias)"
            else:
                action = "Instancia negativa: ignorada por Find-S"

            self.history.append({
                "step": idx,
                "instance": instance,
                "label": "Positivo" if is_positive else "Negativo",
                "action": action,
                "hypothesis": copy.deepcopy(self.hypothesis)
            })

        return self

    def predict(self, instance: List[str]) -> int:
        """Predice 1 (positivo) o 0 (negativo)."""
        return 1 if self.hypothesis.matches(instance) else 0


class CandidateElimination:
    """
    Implementación didáctica del algoritmo Candidate-Elimination.
    Mantiene los límites S (específico) y G (general) del Espacio de Versiones.
    """

    def __init__(self, attribute_domains: Dict[str, List[str]]):
        """
        attribute_domains: Diccionario con {nombre_atributo: [valores_posibles]}
        Ejemplo: {'Dedicacion': ['Alta', 'Media', 'Baja'], ...}
        """
        self.attribute_domains = attribute_domains
        self.attribute_names = list(attribute_domains.keys())
        self.num_attributes = len(self.attribute_names)
        self.domain_values = [attribute_domains[name] for name in self.attribute_names]

        self.S: Set[Hypothesis] = set()
        self.G: Set[Hypothesis] = set()
        self.history: List[Dict[str, Any]] = []

    def _min_generalizations(self, s: Hypothesis, x: List[str]) -> Set[Hypothesis]:
        """Calcula las generalizaciones mínimas de s consistentes con x positivo."""
        if s.is_null():
            return {Hypothesis(list(x))}
        
        new_values = []
        for s_val, x_val in zip(s.values, x):
            if s_val == x_val:
                new_values.append(s_val)
            else:
                new_values.append(Hypothesis.ANY_SYMBOL)
        return {Hypothesis(new_values)}

    def _min_specializations(self, g: Hypothesis, x: List[str]) -> Set[Hypothesis]:
        """Calcula las especificaciones mínimas de g consistentes con x negativo (g(x) == 0)."""
        specializations = set()
        for i, (g_val, x_val, domain) in enumerate(zip(g.values, x, self.domain_values)):
            if g_val == Hypothesis.ANY_SYMBOL:
                for val in domain:
                    if val != x_val:
                        spec_values = list(g.values)
                        spec_values[i] = val
                        specializations.add(Hypothesis(spec_values))
        return specializations

    def fit(self, X: List[List[str]], y: List[Any]) -> 'CandidateElimination':
        """
        Ejecuta el algoritmo Candidate-Elimination sobre las instancias X y etiquetas y.
        """
        # Inicialización
        self.S = {Hypothesis([Hypothesis.NULL_SYMBOL] * self.num_attributes)}
        self.G = {Hypothesis([Hypothesis.ANY_SYMBOL] * self.num_attributes)}

        self.history = [{
            "step": 0,
            "instance": None,
            "label": None,
            "description": "Inicialización: S={ <Ø,...,Ø> }, G={ <?,...,?> }",
            "S": copy.deepcopy(self.S),
            "G": copy.deepcopy(self.G)
        }]

        for idx, (instance, label) in enumerate(zip(X, y), start=1):
            is_positive = label in (1, "1", "SI", "SÍ", "yes", "Yes", True)

            if is_positive:
                # 1. Remover de G hipótesis que no hagan match con x
                self.G = {g for g in self.G if g.matches(instance)}

                # 2. Generalizar hipótesis de S inconsistentes que no hacen match con x
                new_S = set()
                for s in self.S:
                    if not s.matches(instance):
                        gen_hypotheses = self._min_generalizations(s, instance)
                        # Conservar solo aquellas que tengan al menos una g en G más general
                        for h in gen_hypotheses:
                            if any(g.is_more_general_or_equal(h) for g in self.G):
                                new_S.add(h)
                    else:
                        new_S.add(s)

                # 3. Remover de S hipótesis más generales que otra en S
                self.S = {
                    s1 for s1 in new_S
                    if not any(s1.is_strictly_more_general(s2) for s2 in new_S)
                }

                desc = f"Ejemplo Positivo #{idx}: S se generaliza, G poda inconsistentes"

            else:
                # Instancia negativa
                # 1. Remover de S hipótesis que hagan match con x (inconsistentes)
                self.S = {s for s in self.S if not s.matches(instance)}

                # 2. Especificar hipótesis de G inconsistentes (que hacen match con x negativo)
                new_G = set()
                for g in self.G:
                    if g.matches(instance):
                        spec_hypotheses = self._min_specializations(g, instance)
                        # Conservar solo aquellas que tengan al menos una s en S más específica
                        for h in spec_hypotheses:
                            if any(h.is_more_general_or_equal(s) for s in self.S):
                                new_G.add(h)
                    else:
                        new_G.add(g)

                # 3. Remover de G hipótesis más específicas que otra en G
                self.G = {
                    g1 for g1 in new_G
                    if not any(g1.is_strictly_more_specific(g2) for g2 in new_G)
                }

                desc = f"Ejemplo Negativo #{idx}: G se especifica, S poda inconsistentes"

            self.history.append({
                "step": idx,
                "instance": instance,
                "label": "Positivo (+)" if is_positive else "Negativo (-)",
                "description": desc,
                "S": copy.deepcopy(self.S),
                "G": copy.deepcopy(self.G)
            })

        return self

    def classify(self, instance: List[str]) -> Dict[str, Any]:
        """
        Clasifica una nueva instancia según el Espacio de Versiones.
        Retorna veredicto unánime ('Positivo', 'Negativo') o 'Ambigua / Incierta'.
        """
        s_matches = [s.matches(instance) for s in self.S]
        g_matches = [g.matches(instance) for g in self.G]

        # Si todas las de S dicen positivo => 100% positivo
        if all(s_matches) and len(self.S) > 0:
            return {
                "decision": "Positivo (+)",
                "confidence": "Unánime (Todas las hipótesis de S y del VS la aceptan)",
                "s_matches": s_matches,
                "g_matches": g_matches
            }
        # Si ninguna de G dice positivo => 100% negativo
        if not any(g_matches):
            return {
                "decision": "Negativo (-)",
                "confidence": "Unánime (Ninguna hipótesis de G ni del VS la acepta)",
                "s_matches": s_matches,
                "g_matches": g_matches
            }

        return {
            "decision": "Ambigua / Incierta",
            "confidence": f"Desacuerdo en el Espacio de Versiones (S aceptadas: {sum(s_matches)}/{len(self.S)}, G aceptadas: {sum(g_matches)}/{len(self.G)})",
            "s_matches": s_matches,
            "g_matches": g_matches
        }
