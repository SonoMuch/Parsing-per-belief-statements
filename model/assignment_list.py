# AssignmentList definisce una classe per rappresentare una lista di Assignment, dove ogni Assignment
# corrisponde a un assegnamento probabilistico. Gestisce righe parseate correttamente.

# Classi:
# - AssignmentList:
#   - Verificare se la lista di assegnamenti è vuota.
#   - Generare una rappresentazione testuale della lista di assegnamenti.

class AssignmentList:
    def __init__(self, assignments):
        # Inizializza un oggetto AssignmentList con una lista di Assignment.
        # Parametri:
        # - assignments: Lista di oggetti Assignment.
        self.assignments = assignments  # Memorizza la lista di assegnamenti nell'attributo assignments.

    def __str__(self):
        # Ritorna una rappresentazione testuale della lista di Assignment.
        # Gli Assignment sono separati da "; " e il risultato termina con un punto.
        return "; ".join(str(a) for a in self.assignments) + "."

    def is_empty(self):
        # Verifica se la lista di Assignment è vuota.
        # Ritorna True se non ci sono elementi nella lista, altrimenti False.
        return len(self.assignments) == 0
