# Il modulo Assignment definisce la classe Assignment, utilizzata per rappresentare un assegnamento probabilistico
# nel formato {fact1,fact2,...}:prob.

class Assignment:
    # Rappresenta un singolo assignment: {fact1,fact2,...}:prob
    # - facts: Lista di Fact che rappresentano i fatti inclusi nell'assegnamento.
    # - probability: Valore di probabilità (float) associato all'assegnamento.

    def __init__(self, facts, probability):
        # Inizializza un oggetto Assignment con una lista di fatti e un valore di probabilità.
        # Parametri:
        # - facts: Lista di oggetti Fact che rappresentano i fatti inclusi nell'assegnamento.
        # - probability: Un numero float che rappresenta la probabilità associata all'assegnamento.
        self.facts = facts  # Assegna la lista di fatti all'attributo facts.
        self.probability = probability  # Assegna la probabilità all'attributo probability.

    def __str__(self):
        # Ritorna una rappresentazione testuale dell'assegnamento nel formato specifico.
        # Formatta i fatti come una stringa separata da virgole e aggiunge la probabilità dopo i due punti.
        facts_str = ",".join(str(f) for f in self.facts)  # Combina i fatti in una stringa separata da virgole.
        return f"{{{facts_str}}}:{self.probability}"  # Restituisce la rappresentazione completa dell'assegnamento.
