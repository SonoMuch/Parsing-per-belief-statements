from lark import Lark, Transformer
from model import Fact, Assignment, AssignmentList

class AssignmentTransformer(Transformer):

    def FLOAT(self, v): #conversioni
        return float(v)

    def NAME(self, v):
        return str(v)

    def fact(self, items): #trasforma fatto
        if len(items) == 1:
            return Fact(items[0])
        else:
            name = items[0]
            args = items[1]
            return Fact(name, args)


    def argument_list(self, items):
        return items

    def fact_list(self, items):
        return items

    def assignment(self, items):
        return Assignment(items[0], items[1])

    def assignment_list(self, items):
        return AssignmentList(items)

class BeliefParser: #analisi input con lark
    def __init__(self):
        with open("grammar.lark", "r", encoding="utf-8") as f:
            grammar = f.read()
        self.parser = Lark(grammar, parser='lalr', maybe_placeholders=False)
        self.transformer = AssignmentTransformer()

    def parse_line(self, line): #trasforma righe in oggetti
        try:
            tree = self.parser.parse(line)
            return self.transformer.transform(tree)
        except Exception:
            return None
