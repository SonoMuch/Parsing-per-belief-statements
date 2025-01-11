# Il modulo BeliefParser è progettato per analizzare il contenuto di un file in base a una grammatica definita.
# Permette di elaborare righe che contengono assegnamenti probabilistici separati da ';', validandoli e trasformandoli in oggetti Python comprensibili dal sistema.

# Classi:
# - BeliefParser: Gestisce il parsing e la validazione degli assegnamenti.

from lark import Lark  # Importa Lark per gestire la sintassi della grammatica.
from model import Fact, Assignment, AssignmentList  # Importa le classi necessarie per rappresentare i dati parseati.
from .assignment_transformer import AssignmentTransformer  # Importa il trasformatore per convertire gli alberi sintattici.

class BeliefParser:
    # Parser per analizzare il contenuto di un file in base alla grammatica definita.

    def __init__(self):
        # Inizializza il parser caricando la grammatica dal file 'grammar.lark'.
        with open("grammar.lark", "r", encoding="utf-8") as f:
            grammar = f.read()  # Legge il contenuto del file di grammatica.
        self.parser = Lark(grammar, parser='lalr', maybe_placeholders=False, transformer=AssignmentTransformer())
        # Inizializza il parser Lark con la grammatica letta, utilizzando il parser LALR e il trasformatore AssignmentTransformer.

    def parse_line(self, line):
        # Processa una riga contenente più assegnamenti separati da ';'.
        # Scarta assegnamenti con probabilità non valide.

        try:
            print(f"DEBUG: Processing line: {line}")  # Stampa di debug per monitorare la riga in elaborazione.
            assignments = line.split(";")  # Divide la riga in assegnamenti separati da ';'.
            valid_assignments = []  # Lista per memorizzare gli assegnamenti validi.
            invalid_segments = []  # Lista per memorizzare i segmenti non validi.

            for assignment in assignments:  # Itera su ogni assegnamento.
                assignment = assignment.strip()  # Rimuove spazi vuoti attorno all'assegnamento.
                if not assignment:  # Salta assegnamenti vuoti.
                    continue
                try:
                    tree = self.parser.parse(f"{assignment}.")  # Analizza l'assegnamento aggiungendo un punto finale.
                    # Controlla se la probabilità è valida.
                    if tree.assignments[0].probability is not None:
                        valid_assignments.append(tree.assignments[0])  # Aggiunge l'assegnamento valido alla lista.
                    else:
                        invalid_segments.append(assignment)  # Aggiunge il segmento non valido alla lista.
                except Exception as e:
                    print(f"DEBUG: Parse Error for '{assignment}': {e}")  # Stampa di debug per errori di parsing.
                    invalid_segments.append(assignment)  # Aggiunge il segmento non valido alla lista.

            if valid_assignments:
                return AssignmentList(valid_assignments), invalid_segments  # Ritorna gli assegnamenti validi e quelli non validi.
            else:
                return None, invalid_segments  # Ritorna None e i segmenti non validi se non ci sono assegnamenti validi.
        except Exception as e:
            print(f"DEBUG: Parse Error: {e}")  # Stampa di debug per errori generali di parsing.
            return None, [line]  # Ritorna None e l'intera riga come non valida.
