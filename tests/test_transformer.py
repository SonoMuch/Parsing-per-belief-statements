import pytest
from transformer_module import ASPTransformer
from model import Assignment, Fact, AssignmentList


def test_transform_to_facts():  # Test per verificare la trasformazione degli assegnamenti in fatti probabilistici.
    transformer = ASPTransformer()
    assignments = AssignmentList([
        Assignment([Fact("a")], 0.3),
        Assignment([Fact("b"), Fact("c")], 0.7)
    ])
    facts = transformer.transform_to_facts(assignments.assignments)

    assert len(facts) > 0
    assert facts[0].startswith("0.3::") or facts[0].startswith("0.300000000::af.")  # Permette entrambe le versioni
  # Controlla solo la parte numerica senza precisione eccessiva
  # Verifica il formato dell'output trasformato.


def test_transform_to_rules():  # Test per verificare la trasformazione degli assegnamenti in regole ASP.
    transformer = ASPTransformer()
    assignments = AssignmentList([
        Assignment([Fact("a")], 0.5),
        Assignment([Fact("b")], 0.5)
    ])
    rules = transformer.transform_to_rules(assignments.assignments)

    assert len(rules) > 0
    assert "a:- a" in rules[0]  # Controlla la corretta generazione della regola.


def test_transform_complete():  # Test per verificare la trasformazione completa degli assegnamenti.
    transformer = ASPTransformer()
    assignments = AssignmentList([
        Assignment([Fact("x")], 0.4),
        Assignment([Fact("y")], 0.6)
    ])
    output = transformer.transform(assignments)

    assert len(output) > 0
    assert any("x:-" in line for line in output)  # Verifica che la regola per x sia stata generata.
