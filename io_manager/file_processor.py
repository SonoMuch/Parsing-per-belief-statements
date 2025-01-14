from parser import BeliefParser
from transformer_module import ASPTransformer
from model import AssignmentList

class FileProcessor:

    def __init__(self, input_file="input.txt", output_file="output.txt"): #costruttore
        self.input_file = input_file #input
        self.output_file = output_file  #output
        self.parser = BeliefParser()
        self.asp_transformer = ASPTransformer()

    def process(self):
        results = []  # serve per accumulare i risultati trasformati e messaggi di errore


        with open(self.input_file, "r", encoding="utf-8") as fin: #lettura file
            for idx, line in enumerate(fin, start=1):
                original_line = line.strip().replace(' ', '')  #elimina soazi
                if not original_line:
                    continue

                while original_line.endswith("."):

                    original_line = original_line[:-1]

                assignment_list, invalid_segments = self.parser.parse_line(original_line)

                results.append(f"Output riga {idx}:")

                if assignment_list and not assignment_list.is_empty(): #trasforma i risultati
                    transformed_lines = self.asp_transformer.transform(assignment_list)
                    if any("% Errore:" in line for line in transformed_lines): #errori
                        results.extend([line for line in transformed_lines if "% Errore:" in line])
                        continue
                    results.extend(transformed_lines)  # Add risultati.

                for invalid in invalid_segments: #messaggi di errore
                    results.append(f"% La riga '{invalid}.' non rispetta la grammatica.")
                results.append("")

        with open(self.output_file, "w", encoding="utf-8") as fout: #write
            for r in results:
                fout.write(r + "\n")
