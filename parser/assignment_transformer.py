from lark import Transformer
from model import Fact, Assignment, AssignmentList

class AssignmentTransformer(Transformer):
    def FLOAT(self, v):
        try:
            probability = float(v)  # Converte in float.
            if 0 <= probability <= 1:
                return probability
            else:
                raise ValueError(f"Invalid probability range: {probability}")
        except ValueError:
            print(f"DEBUG: Invalid FLOAT value: {v}")  # Debug per errori
            return None

    def NAME(self, v):  # Conversione in stringa
        return str(v)

    def INT(self, v):
        return str(v)

    def atom(self, items):  # Elemento base
        return items[0]

    def fact(self, items):
        if len(items) == 1:
            return Fact(items[0])
        else:
            name = items[0]
            args = [self.fact([arg]) if isinstance(arg, str) else arg for arg in items[1]]  # Crea fatti con argomenti
            return Fact(name, args)

    def argument_list(self, items):  # Lista di argomenti
        return items

    def fact_list(self, items):  # Lista di fatti
        return [self.fact([item]) if isinstance(item, str) else item for item in items]

    def assignment(self, items):  # Trasforma assegnamento
        return Assignment(items[0], items[1])

    def assignment_list(self, items):  # Raccolta lista di assegnamenti
        return AssignmentList(items)

    def mass_statement(self, items):
        return Assignment([items[0]], items[1])  # Ora crea un oggetto Assignment

    def label_statement(self, items):
        return {"type": "label", "fact": items[0], "labels": items[1]}

    def leaf_statement(self, items):
        return {"type": "leaf", "fact": items[0]}

