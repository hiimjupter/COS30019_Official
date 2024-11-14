import re
from itertools import product


class TruthTable():
    def __init__(self, kb, query):
        self.kb = kb  # Knowledge base: list of sentences
        self.query = query  # Query: a single symbol or sentence
        self.symbols = sorted(self.get_symbols())
        self.satisfying_models = []
        self.model_count = 0

    def extract_symbols(self, sentence):
        # Helper method to extract symbols from a sentence
        symbols = set()
        symbols.update(re.findall(r'\b[a-zA-Z][a-zA-Z0-9]*\b', sentence))
        return symbols

    def get_symbols(self):
        # Extract unique symbols from KB and query
        symbols = set()
        for sentence in self.kb:
            symbols.update(self.extract_symbols(sentence))
        symbols.update(self.extract_symbols(self.query))
        return list(symbols)

    def tokenizer(self, sentence):
        return re.findall(r'[a-zA-Z0-9]+|=>|&|\||~|\(|\)', sentence)

    def evaluate(self, sentence, model):
        if not sentence.strip():
            return True
        tokens = self.tokenizer(sentence)
        stack = []
        operators = []

        for token in tokens:
            if token in ('=>', '&', '|'):
                operators.append(token)
            elif token == '~':
                if not stack:
                    raise ValueError(f"Invalid NOT operation: no operand.")
                operand = stack.pop()
                stack.append(not operand)
            else:
                stack.append(model.get(token, False))
                if operators:
                    operator = operators.pop()
                    if operator == '=>':
                        if len(stack) < 2:
                            raise ValueError(
                                f"Invalid implication operation: insufficient operands.")
                        right = stack.pop()
                        left = stack.pop()
                        stack.append(not left or right)
                    elif operator == '&':
                        if len(stack) < 2:
                            raise ValueError(
                                f"Invalid AND operation: insufficient operands.")
                        right = stack.pop()
                        left = stack.pop()
                        stack.append(left and right)
                    elif operator == '|':
                        if len(stack) < 2:
                            raise ValueError(
                                f"Invalid OR operation: insufficient operands.")
                        right = stack.pop()
                        left = stack.pop()
                        stack.append(left or right)
        if len(stack) != 1:
            raise ValueError(
                f"Invalid clause evaluation: incorrect stack state.")
        return stack.pop()

    def checking(self):
        # Generate all possible models
        models = product([False, True], repeat=len(self.symbols))

        for model_iter in models:
            model = dict(zip(self.symbols, model_iter))

            if all(self.evaluate(sentence, model) for sentence in self.kb):
                self.model_count += 1
                self.satisfying_models.append(model)

        if not self.satisfying_models:
            return "NO"

        entailments = all(model[self.query]
                          for model in self.satisfying_models)

        for model in self.satisfying_models:
            print('Satisfying model:', model)

        if entailments:
            return f"YES: {self.model_count}"
        else:
            return "NO"
