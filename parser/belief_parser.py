
from lark import Lark  # Importa Lark per gestire la sintassi della grammatica.
from model import Fact, Assignment, AssignmentList  # Importa le classi necessarie per rappresentare i dati parseati.
from .assignment_transformer import AssignmentTransformer  # Importa il trasformatore per convertire gli alberi sintattici.

class BeliefParser:

    def __init__(self):

        with open("grammar.lark", "r", encoding="utf-8") as f: #carica grammatica
            grammar = f.read()
        self.parser = Lark(grammar, parser='lalr', maybe_placeholders=False, transformer=AssignmentTransformer())


    def parse_line(self, line):
        try:
            print(f"DEBUG: Processing line: {line}")  #Debug usati per verificare errori
            assignments = line.split(";")
            valid_assignments = []  # Lista per assegnamenti validi.
            invalid_segments = []  # Lista per segmenti non validi.

            for assignment in assignments:
                assignment = assignment.strip()
                if not assignment:
                    continue
                try:
                    tree = self.parser.parse(f"{assignment}.")
                    if tree.assignments[0].probability is not None:
                        valid_assignments.append(tree.assignments[0])  #aggiunta assegnamento valido
                    else:
                        invalid_segments.append(assignment)  #non valido
                except Exception as e:
                    print(f"DEBUG: Parse Error for '{assignment}': {e}")  #usato per controllo errori
                    invalid_segments.append(assignment)

            if valid_assignments:
                return AssignmentList(valid_assignments), invalid_segments  #ritorno assegnamenti
            else:
                return None, invalid_segments
        except Exception as e:
            print(f"DEBUG: Parse Error: {e}")  #usato per controllo errori
            return None, [line]
