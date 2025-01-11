from parser import BeliefParser
from transformer_module import ASPTransformer
from model import AssignmentList

class FileProcessor:

    #FileProcessor gestisce la lettura di un file di input.txt, il parsing delle righe secondo un formato specifico,
    #e genera un output che include i risultati trasformati e i messaggi di errore. Ogni riga di input viene
    #elaborata separatamente, con un'intestazione "Output riga N:" per indicare l'origine dell'output.
    #es:

#input:
#{f(a)}:0.2; {f(b)}:0.2; {f(c)}:0.2; {f(a,b)}:0.2; {f(a,b,c)}:0.2.
#{red}:0.3; {blue}:0.1; {blue,yellow}:0.6.

#Output riga 1:
#0.200000000::f_af.
#0.250000000::f_bf.
#0.333333333::f_cf.
#0.500000000::f_a_bf.
#1.000000000::f_a_b_cf.
#f_a:- f_af.
#f_b:- not f_af, f_bf.
#f_c:- not f_af, not f_bf, f_cf.
#f_a_b:- not f_af, not f_bf, not f_cf, f_a_bf.
#f_a_b_c:- not f_af, not f_bf, not f_cf, not f_a_bf.
#f;a;b;c:- f_a_b_c.

#Output riga 2:
#0.300000000::redf.
#0.142857143::bluef.
#1.000000000::blue_yellowf.
#red:- redf.
#blue:- not redf, bluef.
#blue_yellow:- not redf, not bluef.
#blue;yellow:- blue_yellow.



   #Funzionalità principali:
    #- Rimuove spazi orizzontali (spazi vuoti) e normalizza i punti finali nelle righe di input.
    #- Utilizza il parser per analizzare le righe secondo una sintassi specifica.
    #- Trasforma i dati di input in output ASP tramite un trasformatore dedicato.
    #- Gestisce righe non valide aggiungendo messaggi di errore all'output.


    #Il file di output.txt risultante contiene i dati trasformati e gli eventuali errori organizzati per ogni riga di input.

    # Classe che gestisce la lettura di un file di input, il parsing delle righe e la generazione di un file di output
    # contenente i risultati trasformati e i messaggi di errore. Ogni riga di input viene elaborata separatamente.

    def __init__(self, input_file="input.txt", output_file="output.txt"):
        # Costruttore della classe.
        # Parametri:
        # - input_file: nome del file di input (default "input.txt").
        # - output_file: nome del file di output (default "output.txt").
        self.input_file = input_file  # Salva il nome del file di input.
        self.output_file = output_file  # Salva il nome del file di output.
        self.parser = BeliefParser()  # Inizializza il parser per analizzare le righe di input.
        self.asp_transformer = ASPTransformer()  # Inizializza il trasformatore per convertire i dati in formato ASP.

    def process(self):
        # Metodo principale per processare il file di input e generare il file di output.
        results = []  # Lista per accumulare i risultati trasformati e i messaggi di errore.

        # Apertura del file di input in modalità lettura con encoding UTF-8.
        with open(self.input_file, "r", encoding="utf-8") as fin:
            for idx, line in enumerate(fin, start=1):  # Itera su ogni riga del file, con indice a partire da 1.
                original_line = line.strip().replace(' ', '')  # Rimuove spazi e normalizza la riga.
                if not original_line:  # Salta righe vuote.
                    continue

                while original_line.endswith("."):
                    # Rimuove eventuali punti finali dalla riga.
                    original_line = original_line[:-1]

                # Esegue il parsing della riga e restituisce:
                # - assignment_list: lista di assegnamenti validi.
                # - invalid_segments: segmenti non validi che non rispettano la grammatica.
                assignment_list, invalid_segments = self.parser.parse_line(original_line)

                results.append(f"Output riga {idx}:")  # Aggiunge un'intestazione per identificare la riga di output.

                if assignment_list and not assignment_list.is_empty():
                    # Se esistono assegnamenti validi, li trasforma in formato ASP.
                    transformed_lines = self.asp_transformer.transform(assignment_list)
                    if any("% Errore:" in line for line in transformed_lines):
                        # Se ci sono errori nella trasformazione, li aggiunge all'output e passa alla prossima riga.
                        results.extend([line for line in transformed_lines if "% Errore:" in line])
                        continue
                    results.extend(transformed_lines)  # Aggiunge i risultati trasformati.

                for invalid in invalid_segments:
                    # Per ogni segmento non valido, aggiunge un messaggio di errore.
                    results.append(f"% La riga '{invalid}.' non rispetta la grammatica.")
                results.append("")  # Aggiunge una riga vuota per separare l'output delle righe.

        # Scrive i risultati accumulati nel file di output.
        with open(self.output_file, "w", encoding="utf-8") as fout:
            for r in results:
                fout.write(r + "\n")  # Scrive ogni riga con un ritorno a capo.
