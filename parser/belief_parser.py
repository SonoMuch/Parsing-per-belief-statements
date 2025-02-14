from lark import Lark
from model import Fact, Assignment, AssignmentList
from .assignment_transformer import AssignmentTransformer


class BeliefParser:

    def __init__(self):
        import os

        grammar_path = os.path.join(os.path.dirname(__file__), "..", "grammar.lark")
        with open(grammar_path, "r", encoding="utf-8") as f:
            grammar = f.read()
        self.parser = Lark(grammar, parser='lalr', maybe_placeholders=False, transformer=AssignmentTransformer())

    def parse_line(self, line):
        try:
            print(
                f"DEBUG: Processing line: {line}")  # Messaggio di debug per tracciare l'elaborazione delle righe di input  # Debug usato per verificare errori
            assignments = line.split(";")
            valid_assignments = []
            invalid_segments = []

            for assignment in assignments:
                assignment = assignment.strip()
                if not assignment:
                    continue
                try:
                    tree = self.parser.parse(f"{assignment}.")
                    parsed_result = tree.assignments[0] if hasattr(tree, 'assignments') else tree

                    if parsed_result and hasattr(parsed_result,
                                                 'probability') and parsed_result.probability is not None:  # Controlla se è un assegnamento con probabilità valida
                        valid_assignments.append(parsed_result)  # Aggiunta assegnamento valido
                    elif hasattr(parsed_result, 'fact'):  # Gestisce la sintassi alternativa (mass(), label(), leaf())
                        valid_assignments.append(parsed_result)  # Gestisce la sintassi alternativa
                    else:
                        invalid_segments.append(assignment)  # Non valido
                except Exception as e:
                    print(f"DEBUG: Parse Error for '{assignment}': {e}")  # Debug per errori
                    invalid_segments.append(assignment)

            if valid_assignments:
                return AssignmentList(valid_assignments), invalid_segments  # Ritorno assegnamenti
            else:
                return None, invalid_segments
        except Exception as e:
            print(f"DEBUG: Parse Error: {e}")  # Debug per errori
            return None, [line]
