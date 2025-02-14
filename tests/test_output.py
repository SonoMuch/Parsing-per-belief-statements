import sys
import os
import pytest
import time

# Aggiunge la root del progetto al percorso di ricerca dei moduli
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from io_manager.file_processor import FileProcessor

def test_generated_output():  # Test per confrontare l'output generato con quello atteso
    base_dir = os.path.dirname(os.path.dirname(__file__))  # Torna alla root del progetto
    input_file = os.path.join(base_dir, "input.txt")
    expected_output_file = os.path.join(base_dir, "output.txt")
    generated_output_file = os.path.join(base_dir, "generated_output.txt")

    # Esegue il processo di generazione dell'output
    processor = FileProcessor(input_file=input_file, output_file=generated_output_file)
    processor.process()

    # Debug: Controllo percorsi
    print(f"DEBUG: Controllando se esiste {generated_output_file}")
    print(f"DEBUG: Controllando se esiste {expected_output_file}")

    # Attesa fino a 2 secondi per la creazione del file
    for _ in range(10):
        if os.path.exists(generated_output_file):
            break
        time.sleep(0.2)

    if not os.path.exists(generated_output_file):
        pytest.fail(f"Errore: il file {generated_output_file} non è stato generato!")

    if not os.path.exists(expected_output_file):
        pytest.fail(f"Errore: il file {expected_output_file} non esiste!")

    # Confronta i file di output
    with open(generated_output_file, "r", encoding="utf-8") as gen_out, open(expected_output_file, "r", encoding="utf-8") as expected_out:
        generated_lines = gen_out.readlines()
        expected_lines = expected_out.readlines()

    assert generated_lines == expected_lines, "L'output generato non corrisponde a quello atteso!"
