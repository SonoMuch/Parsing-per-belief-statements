
class Fact:

    def __init__(self, name, arguments=None):
        self.name = name
        self.arguments = arguments if arguments else []

    def __str__(self):
        if self.arguments:  #check se ci sono argomenti
            args_str = ",".join(str(a) for a in self.arguments)  # Concatena
            return f"{self.name}({args_str})"  #return argomenti
        else:
            return self.name  #return solo il nome (caso no argomenti)

    def to_normalized_str(self):
        if self.arguments:
            args_normalized = "_".join(arg.to_normalized_str() for arg in self.arguments)  # Normalizza
            return f"{self.name}_{args_normalized}" # concatena nome+argomenti
        else:
            return self.name
