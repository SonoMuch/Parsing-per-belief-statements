from model import Fact
import math

def facts_name(facts): #trasforma assegnamenti in fatti
    for f in facts:
        if not isinstance(f, Fact):
            raise TypeError(f"Expected Fact, got {type(f)}: {f}")
        print("DEBUG: Fact in facts_name =", f)  # check errori
    return "_".join(f.to_normalized_str() for f in facts)

class ASPTransformer:


    def __init__(self):
        self.remaining_probability = 1.0

    def transform_to_facts(self, assignments):
        self.remaining_probability = 1.0
        facts = []

        for assignment in assignments:
            if self.remaining_probability <= 0:  # Probabilità residua <= 0
                facts.append("% Errore: la probabilità residua è zero o negativa.")
                return facts

            probability = assignment.probability / self.remaining_probability
            fact_name = facts_name(assignment.facts)


            print(
                f"DEBUG: assignment.probability={assignment.probability}, probability={probability}, fact_name={fact_name}") # Debug per verificare gli errori

            if probability > 1:  # Probabilità calcolata > 1
                facts.append(
                    f"% Errore: la probabilità calcolata non è valida perché >1."
                )
                self.remaining_probability = 0
                return facts

            if 0 < probability < 1 and not math.isclose(probability, 1, abs_tol=1e-9): #Evitare = 1 dovuti ad approssimazione
                facts.append(f"{probability:.9f}::{fact_name}f.")

            if assignment.probability < self.remaining_probability:
                self.remaining_probability -= assignment.probability
            elif assignment.probability == self.remaining_probability:
                self.remaining_probability = 0

        return facts

    def transform_to_rules(self, assignments):
        rules = []  # Lista per regole generate
        fact_names = [facts_name(a.facts) for a in assignments if a.probability > 0]

        # check n assegnamenti (rimozione di ridondanze)
        if len(fact_names) <= 2:
            for i, assignment in enumerate(assignments):
                if assignment.probability == 0:
                    continue
                current_fact = fact_names[i]
                if i == 0:
                    rules.append(f"{current_fact}:- {current_fact}f.")
                else:
                    preconditions = [f"not {fact_names[j]}f" for j in range(i)]
                    rule = f"{current_fact}:- {', '.join(preconditions)}, {current_fact}f."
                    rules.append(rule)
            return rules


        for i, assignment in enumerate(assignments[:-1]):  # Tutti tranne l'ultimo
            if assignment.probability == 0:
                continue
            current_fact = fact_names[i]
            preconditions = [f"not {fn}f" for fn in fact_names[:i]]
            rule = f"{current_fact}:- {', '.join(preconditions)}, {current_fact}f." if preconditions else f"{current_fact}:- {current_fact}f."
            rules.append(rule)


            if len(assignment.facts) == 2:
                combined_facts = ";".join(fact.to_normalized_str() for fact in assignment.facts)
                rules.append(f"{combined_facts} :- {current_fact}.")

        # Gestione dell'ultimo assegnamento
        last_fact = fact_names[-1]
        preconditions = [f"not {fn}f" for fn in fact_names[:-1]]
        combined_rule = f"{last_fact}:- {', '.join(preconditions)}." if preconditions else f"{last_fact}:- {last_fact}f."
        rules.append(combined_rule)


        combined_facts = ";".join(last_fact.split("_"))  # Combina i nomi dei fatti con il punto e virgola
        rules.append(f"{combined_facts}:- {last_fact}.")

        return rules

    def transform(self, assignment_list):
        assignments = assignment_list.assignments
        facts = self.transform_to_facts(assignments)
        rules = self.transform_to_rules(assignments)
        return facts + rules
