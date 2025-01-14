from model import Fact

def facts_name(facts): #traforma gli assegnamenti probabilistici in fatti e regole ASP
    for f in facts:  # Verifica che ogni elemento della lista sia un oggetto Fact
        if not isinstance(f, Fact):
            raise TypeError(f"Expected Fact, got {type(f)}: {f}")  # Solleva un'eccezione per tipi non validi
        print("DEBUG: Fact in facts_name =", f)  # Debug per verificare eventuali errori nei fatti
    return "_".join(f.to_normalized_str() for f in facts)  # Restituisce i fatti concatenati in formato normalizzato

class ASPTransformer: # Classe per trasformare assegnamenti probabilistici in fatti e regole ASP


    def __init__(self):
        self.remaining_probability = 1.0

    def transform_to_facts(self, assignments): #genera fatti probabilistici
        self.remaining_probability = 1.0
        facts = []  # Lista per fatti generati

        for assignment in assignments:
            if self.remaining_probability <= 0: #P <0
                facts.append("% Errore: la probabilità residua è zero o negativa.")
                return facts

            probability = assignment.probability / self.remaining_probability
            fact_name = facts_name(assignment.facts)

            if probability > 1:  #P>1
                facts.append(
                    f"% Errore: la probabilità calcolata non è valida perché >1."
                )
                self.remaining_probability = 0
                return facts

            if assignment.probability > 0:
                facts.append(f"{probability:.9f}::{fact_name}f.")

            self.remaining_probability -= assignment.probability

        return facts

    def transform_to_rules(self, assignments): # Genera regole ASP per i fatti derivati e le condizioni associate

        rules = []  # Lista per regole generate
        fact_names = [facts_name(a.facts) for a in assignments if a.probability > 0]

        for i, assignment in enumerate(assignments[:-1]): #tutti tranne l'ultimo
            if assignment.probability == 0:
                continue
            current_fact = fact_names[i]
            preconditions = [f"not {fn}f" for fn in fact_names[:i]]
            rule = f"{current_fact}:- {', '.join(preconditions)}, {current_fact}f." if preconditions else f"{current_fact}:- {current_fact}f."
            rules.append(rule)

        last_fact = fact_names[-1]  #ultimo fatto
        preconditions = [f"not {fn}f" for fn in fact_names[:-1]]
        combined_rule = f"{last_fact}:- {', '.join(preconditions)}." if preconditions else f"{last_fact}:- {last_fact}f."
        rules.append(combined_rule)

        combined_facts = ";".join(last_fact.split("_"))  #combina regole e fatti
        rules.append(f"{combined_facts}:- {last_fact}.")

        return rules

    def transform(self, assignment_list): #Combina per un unico output
        assignments = assignment_list.assignments
        facts = self.transform_to_facts(assignments)
        rules = self.transform_to_rules(assignments)
        return facts + rules
