import sys
import os

# Aggiunge la root del progetto al percorso di ricerca dei moduli
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from parser.belief_parser import BeliefParser
from model import AssignmentList


def test_valid_parsing():  # Test per verificare che il parser riconosca correttamente assegnamenti validi.
    parser = BeliefParser()
    input_line = "{red}:0.3 ; {blue}:0.1 ; {blue,yellow}:0.6"
    assignments, errors = parser.parse_line(input_line)

    assert isinstance(assignments, AssignmentList)
    assert len(assignments.assignments) == 3  # Deve riconoscere 3 assegnamenti: red, blue, blue_yellow.
    assert len(errors) == 0



def test_invalid_parsing():  # Test per verificare che il parser gestisca correttamente assegnamenti con probabilità invalide.
    parser = BeliefParser()
    input_line = "{a}:1.2; {b,c}:0.7."
    assignments, errors = parser.parse_line(input_line)

    assert assignments is None
    assert len(errors) > 0

