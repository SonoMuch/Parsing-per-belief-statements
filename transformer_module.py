# Il modulo transformer_module fornisce strumenti per trasformare assegnamenti probabilistici in fatti e regole ASP.

# Classi e Funzioni:
# - facts_name: Normalizza una lista di fatti in una stringa lineare unica.
# - ASPTransformer: Gestisce la trasformazione di assegnamenti in:
#   - Fatti probabilistici con probabilità condizionali.
#   - Regole ASP per rappresentare la logica associata ai fatti.

# - transform_to_facts: Genera fatti probabilistici, calcolando le probabilità condizionali e gestendo errori.
# - transform_to_rules: Crea regole ASP per fatti derivati e condizioni associate.
# - transform: Combina fatti probabilistici e regole ASP in un unico output comprensivo.

from model import Fact  # Importa la classe Fact per gestire e rappresentare i fatti.

def facts_name(facts):
    # Normalizza una lista di fatti in una stringa lineare unica separata da underscore.
    for f in facts:  # Verifica che ogni elemento della lista sia un oggetto Fact.
        if not isinstance(f, Fact):
            raise TypeError(f"Expected Fact, got {type(f)}: {f}")  # Solleva un'eccezione per tipi non validi.
        print("DEBUG: Fact in facts_name =", f)  # Debug per verificare eventuali errori nei fatti.
    return "_".join(f.to_normalized_str() for f in facts)  # Restituisce i fatti concatenati in formato normalizzato.

class ASPTransformer:
    # Classe per trasformare assegnamenti probabilistici in fatti e regole ASP.

    def __init__(self):
        # Inizializza il trasformatore ASP con una probabilità residua iniziale di 1.0.
        self.remaining_probability = 1.0

    def transform_to_facts(self, assignments):
        # Genera fatti probabilistici calcolando le probabilità condizionali.
        self.remaining_probability = 1.0  # Reimposta la probabilità residua a 1.0.
        facts = []  # Lista per memorizzare i fatti generati.

        for assignment in assignments:  # Itera su ogni assegnamento.
            if self.remaining_probability <= 0:  # Controlla se la probabilità residua è esaurita.
                facts.append("% Errore: la probabilità residua è zero o negativa.")
                return facts

            probability = assignment.probability / self.remaining_probability  # Calcola la probabilità condizionale.
            fact_name = facts_name(assignment.facts)  # Ottiene il nome del fatto normalizzato.

            if probability > 1:  # Controlla se la probabilità calcolata supera 1.
                facts.append(
                    f"% Errore: la probabilità calcolata non è valida perché >1."
                )
                self.remaining_probability = 0
                return facts

            if assignment.probability > 0:  # Aggiunge il fatto solo se la probabilità è maggiore di zero.
                facts.append(f"{probability:.9f}::{fact_name}f.")

            self.remaining_probability -= assignment.probability  # Aggiorna la probabilità residua.

        return facts

    def transform_to_rules(self, assignments):
        # Genera regole ASP per i fatti derivati e le condizioni associate.
        rules = []  # Lista per memorizzare le regole generate.
        fact_names = [facts_name(a.facts) for a in assignments if a.probability > 0]  # Ottiene i nomi dei fatti validi.

        for i, assignment in enumerate(assignments[:-1]):  # Itera su tutti gli assegnamenti tranne l'ultimo.
            if assignment.probability == 0:
                continue  # Salta gli assegnamenti con probabilità zero.
            current_fact = fact_names[i]  # Nome del fatto corrente.
            preconditions = [f"not {fn}f" for fn in fact_names[:i]]  # Precondizioni basate sui fatti precedenti.
            rule = f"{current_fact}:- {', '.join(preconditions)}, {current_fact}f." if preconditions else f"{current_fact}:- {current_fact}f."
            rules.append(rule)  # Aggiunge la regola generata.

        last_fact = fact_names[-1]  # Nome dell'ultimo fatto.
        preconditions = [f"not {fn}f" for fn in fact_names[:-1]]  # Precondizioni per l'ultimo fatto.
        combined_rule = f"{last_fact}:- {', '.join(preconditions)}." if preconditions else f"{last_fact}:- {last_fact}f."
        rules.append(combined_rule)  # Aggiunge la regola combinata per l'ultimo fatto.

        combined_facts = ";".join(last_fact.split("_"))  # Combina i nomi dei fatti separandoli con il punto e virgola.
        rules.append(f"{combined_facts}:- {last_fact}.")  # Aggiunge la regola per i fatti combinati.

        return rules

    def transform(self, assignment_list):
        # Combina fatti probabilistici e regole ASP in un unico output.
        assignments = assignment_list.assignments  # Ottiene la lista degli assegnamenti.
        facts = self.transform_to_facts(assignments)  # Trasforma gli assegnamenti in fatti.
        rules = self.transform_to_rules(assignments)  # Trasforma gli assegnamenti in regole.
        return facts + rules  # Ritorna la combinazione di fatti e regole.
