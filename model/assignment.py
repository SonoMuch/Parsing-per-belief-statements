
class Assignment:


    def __init__(self, facts, probability):
        self.facts = facts
        self.probability = probability


    def __str__(self):
        facts_str = ",".join(str(f) for f in self.facts)  # Combinazione dei fatti.
        return f"{{{facts_str}}}:{self.probability}"  #assegnamento.
