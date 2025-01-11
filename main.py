# File coinvolti:
# - input.txt: File di input contenente i dati da elaborare.
# - output.txt: File di output generato con i risultati dell'elaborazione.

from io_manager.file_processor import FileProcessor  # Importa la classe FileProcessor per gestire l'elaborazione dei file.

def main():
    # Funzione principale che esegue il processo di elaborazione.

    processor = FileProcessor(input_file="input.txt", output_file="output.txt")
    # Inizializza un oggetto FileProcessor specificando i file di input e output.

    processor.process()
    # Chiama il metodo process per elaborare il file di input e generare il file di output.

    print("Elaborazione completata.")
    # Stampa un messaggio per indicare il completamento del processo.

if __name__ == "__main__":
    main()  # Esegue la funzione principale se il file viene eseguito come script.
