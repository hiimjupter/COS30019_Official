import re
from itertools import product


class TruthTable():
    def __init__(self, kb, query):
        self.kb = kb  # Knowledge base: list of sentences
        self.query = query  # Query: a single sentence
        self.symbols = sorted(self.get_symbols())
        self.model_count = 0            # Total number of models where KB is true
        self.entail_count = 0          # Number of models where KB and query are true

    def get_symbols(self):
        # Extract unique symbols from KB and query
        symbols = set()
        for sentence in self.kb:
            symbols.update(self.extract_symbols(sentence))
        symbols.update(self.extract_symbols(self.query))
        return list(symbols)

    def extract_symbols(self, sentence):
        # Helper method to extract symbols from a sentence
        symbols = set()
        symbols.update(re.findall(r'\b[a-zA-Z][a-zA-Z0-9]*\b', sentence))
        return symbols

    def entails(self):
        # Generate all possible models
        models = product([False, True], repeat=len(self.symbols))

        for model_iter in models:
            model = dict(zip(self.symbols, model_iter))

            if all(self.evaluate(sentence, model) for sentence in self.kb):
                self.model_count += 1
                if self.evaluate(self.query, model):
                    self.entail_count += 1

        if self.entail_count:
            return True
        else:
            return False

    def evaluate(self, sentence, model):
        # Replace symbols in the sentence with their values from the model
        for symbol in self.symbols:
            sentence = re.sub(r'\b{}\b'.format(
                re.escape(symbol)), str(model[symbol]), sentence)

        # Iteratively replace logical operators with Python equivalents
        previous_sentence = None
        while sentence != previous_sentence:
            previous_sentence = sentence
            sentence = re.sub(r'(\w+)\s*=>\s*(\w+)',
                              r'not \1 or \2', sentence)  # Implication
            sentence = re.sub(r'(\w+)\s*<=>\s*(\w+)',
                              r'\1 == \2', sentence)    # Biconditional
            sentence = re.sub(r'(\w+)\s*&\s*(\w+)',
                              r'\1 and \2', sentence)      # Conjunction
            sentence = re.sub(r'(\w+)\s*\|\s*(\w+)',
                              r'\1 or \2', sentence)       # Disjunction
            # Negation
            sentence = re.sub(r'~', 'not ', sentence)

        # Evaluate the logical expression
        try:
            return eval(sentence)
        except Exception as e:
            print(f"Error evaluating sentence: {sentence}")
            print(e)
            return False
