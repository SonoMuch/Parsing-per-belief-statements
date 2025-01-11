# Il modulo AssignmentTransformer definisce una classe per trasformare l'albero sintattico generato dal parser in oggetti Python comprensibili dal sistema.

# Classi:
# - AssignmentTransformer: Implementa trasformazioni per:
#   - Convertire token FLOAT, NAME e INT in tipi Python.
#   - Gestire fatti semplici e composti.
#   - Trasformare assegnamenti probabilistici e liste di assegnamenti.

from lark import Transformer  # Importa Transformer da Lark per creare trasformazioni personalizzate.
from model import Fact, Assignment, AssignmentList  # Importa le classi utilizzate nelle trasformazioni.

class AssignmentTransformer(Transformer):
    # Trasforma l'albero sintattico generato dal parser in oggetti Python.

    def FLOAT(self, v):
        # Trasforma un valore FLOAT e verifica che sia nell'intervallo [0, 1].
        try:
            probability = float(v)  # Converte il valore in float.
            if 0 <= probability <= 1:
                return probability  # Ritorna il valore se valido.
            else:
                raise ValueError(f"Invalid probability range: {probability}")  # Genera un'eccezione per valori fuori intervallo.
        except ValueError:
            print(f"DEBUG: Invalid FLOAT value: {v}")  # Stampa un messaggio di debug per valori non validi.
            return None  # Ritorna None per indicare un valore non valido.

    def NAME(self, v):
        # Trasforma un token NAME in una stringa.
        return str(v)

    def INT(self, v):
        # Trasforma un token INT in una stringa.
        return str(v)

    def atom(self, items):
        # Ritorna il primo elemento della lista di item.
        return items[0]

    def fact(self, items):
        # Trasforma un fatto:
        # - Senza argomenti: Fact(name)
        # - Con argomenti: Fact(name, args)
        if len(items) == 1:
            return Fact(items[0])  # Crea un fatto semplice con solo il nome.
        else:
            name = items[0]  # Il primo elemento è il nome del fatto.
            args = [self.fact([arg]) if isinstance(arg, str) else arg for arg in items[1]]  # Crea i fatti per gli argomenti.
            return Fact(name, args)  # Crea un fatto composto con nome e argomenti.

    def argument_list(self, items):
        # Ritorna la lista di argomenti così com'è.
        return items

    def fact_list(self, items):
        # Ritorna una lista di fatti, trasformando ogni elemento se necessario.
        return [self.fact([item]) if isinstance(item, str) else item for item in items]

    def assignment(self, items):
        # Trasforma un assegnamento: {facts}:probabilità
        return Assignment(items[0], items[1])  # Crea un oggetto Assignment con fatti e probabilità.

    def assignment_list(self, items):
        # Raccoglie una lista di assegnamenti.
        return AssignmentList(items)  # Crea un oggetto AssignmentList con la lista di assegnamenti.
