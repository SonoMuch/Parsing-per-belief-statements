# Il modulo Fact definisce una classe per rappresentare fatti e fatti composti utilizzati nel sistema.
# Un fatto è identificato da un nome e, opzionalmente, può contenere argomenti che sono altri fatti.

# Classi:
# - Fact:
#   - Rappresenta fatti in forma testuale.
#   - Rappresenta fatti in forma normalizzata per trasformazioni o calcoli.

class Fact:

    # Rappresenta un fatto.
    # - name: Nome del fatto.
    # - arguments: Lista di Fact per rappresentare fatti composti.

    def __init__(self, name, arguments=None):
        # Inizializza un oggetto Fact con un nome e, opzionalmente, una lista di argomenti.
        # Parametri:
        # - name: Stringa che rappresenta il nome del fatto.
        # - arguments: Lista di oggetti Fact (opzionale). Se non fornita, viene inizializzata come lista vuota.
        self.name = name  # Assegna il nome del fatto all'attributo name.
        self.arguments = arguments if arguments else []  # Inizializza gli argomenti come lista vuota se non forniti.

    def __str__(self):
        # Ritorna una rappresentazione testuale del fatto.
        # Se il fatto ha argomenti, li include in formato "nome(arg1,arg2,...)".
        if self.arguments:  # Controlla se il fatto ha argomenti.
            args_str = ",".join(str(a) for a in self.arguments)  # Concatena gli argomenti in una stringa separata da virgole.
            return f"{self.name}({args_str})"  # Ritorna il nome seguito dagli argomenti tra parentesi.
        else:
            return self.name  # Ritorna solo il nome se non ci sono argomenti.

    def to_normalized_str(self):
        # Rappresenta il fatto in forma lineare per uso nelle trasformazioni.
        # Gli argomenti vengono concatenati con il carattere di underscore "_".

        if self.arguments:  # Controlla se il fatto ha argomenti.
            args_normalized = "_".join(arg.to_normalized_str() for arg in self.arguments)  # Normalizza ogni argomento.
            return f"{self.name}_{args_normalized}"  # Ritorna il nome seguito dagli argomenti concatenati con "_".
        else:
            return self.name  # Ritorna solo il nome se non ci sono argomenti.
