
class AssignmentList:
    def __init__(self, assignments):

        self.assignments = assignments  # Memorizza la lista

    def __str__(self): #separatori

        return "; ".join(str(a) for a in self.assignments) + "."

    def is_empty(self): # check lista se piena o vuota

        return len(self.assignments) == 0
