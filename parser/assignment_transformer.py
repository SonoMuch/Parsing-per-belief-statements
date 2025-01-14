from lark import Transformer  # Importa Transformer da Lark per creare trasformazioni personalizzate.
from model import Fact, Assignment, AssignmentList  # Importa le classi utilizzate nelle trasformazioni.

#trasforma alberi in oggetti
class AssignmentTransformer(Transformer):


    def FLOAT(self, v):

        try:
            probability = float(v)  # Converte in float.
            if 0 <= probability <= 1:
                return probability
            else:
                raise ValueError(f"Invalid probability range: {probability}")
        except ValueError:
            print(f"DEBUG: Invalid FLOAT value: {v}") #Utilizzato per verificare errori
            return None

    def NAME(self, v):
        return str(v)

    def INT(self, v):
        return str(v)

    def atom(self, items):
        return items[0]

    def fact(self, items):
        if len(items) == 1:
            return Fact(items[0])
        else:
            name = items[0]
            args = [self.fact([arg]) if isinstance(arg, str) else arg for arg in items[1]]  # Crea i fatti per gli argomenti
            return Fact(name, args)

    def argument_list(self, items): #lista di argomenti
        return items

    def fact_list(self, items): #lista di fatti
        return [self.fact([item]) if isinstance(item, str) else item for item in items]

    def assignment(self, items): #trasforma assegnamento
        return Assignment(items[0], items[1])  #crea oggetto assignment

    def assignment_list(self, items): #raccolta lista di assegnamenti
        return AssignmentList(items)
