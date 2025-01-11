# Il modulo parser_module implementa il parsing e la trasformazione di linee di input

# Classi:
# 1. AssignmentTransformer:
#    - Trasforma l'albero sintattico generato dal parser in oggetti Python comprensibili dal sistema.
#    - Supporta fatti semplici e composti, assegnamenti probabilistici e liste di assegnamenti.

# 2. BeliefParser:
#    - Utilizza la grammatica Lark per analizzare linee di input.
#    - Trasforma il contenuto parseato in oggetti Python tramite l'AssignmentTransformer.

from lark import Lark, Transformer  # Importa Lark per la definizione della grammatica e Transformer per la trasformazione dell'albero.
from model import Fact, Assignment, AssignmentList  # Importa i modelli utilizzati per rappresentare i dati parseati.

class AssignmentTransformer(Transformer):
    # Classe che trasforma l'albero sintattico in oggetti Python.

    def FLOAT(self, v):
        # Converte un valore FLOAT in un tipo Python float.
        return float(v)

    def NAME(self, v):
        # Converte un valore NAME in una stringa.
        return str(v)

    def fact(self, items):
        # Trasforma un fatto, supportando fatti semplici e composti.
        if len(items) == 1:
            return Fact(items[0])  # Ritorna un fatto semplice con un solo nome.
        else:
            name = items[0]  # Nome del fatto.
            args = items[1]  # Argomenti del fatto.
            return Fact(name, args)  # Ritorna un fatto composto con nome e argomenti.

    def argument_list(self, items):
        # Ritorna la lista di argomenti.
        return items

    def fact_list(self, items):
        # Ritorna la lista di fatti.
        return items

    def assignment(self, items):
        # Trasforma un assegnamento in un oggetto Assignment.
        return Assignment(items[0], items[1])

    def assignment_list(self, items):
        # Trasforma una lista di assegnamenti in un oggetto AssignmentList.
        return AssignmentList(items)

class BeliefParser:
    # Classe che utilizza Lark per analizzare linee di input basate su una grammatica definita.

    def __init__(self):
        # Inizializza il parser caricando la grammatica da un file esterno e associa un trasformatore.
        with open("grammar.lark", "r", encoding="utf-8") as f:
            grammar = f.read()  # Legge il contenuto del file di grammatica.
        self.parser = Lark(grammar, parser='lalr', maybe_placeholders=False)  # Inizializza il parser con Lark.
        self.transformer = AssignmentTransformer()  # Associa il trasformatore AssignmentTransformer.

    def parse_line(self, line):
        # Analizza una singola linea di input e la trasforma in oggetti Python.
        try:
            tree = self.parser.parse(line)  # Esegue il parsing della linea usando il parser.
            return self.transformer.transform(tree)  # Trasforma l'albero sintattico in oggetti Python.
        except Exception:
            return None  # Ritorna None in caso di errore di parsing.
