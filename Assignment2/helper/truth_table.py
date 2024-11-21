import re
from itertools import product


class TruthTable():
    def __init__(self, kb, query):
        # Initialize the knowledge base and query
        self.kb = kb  # Knowledge base: list of logical sentences
        self.query = query  # Query: a single symbol or sentence to prove
        # Extract and sort all unique symbols from KB and query
        self.symbols = sorted(self.get_symbols())
        self.model_count = 0  # Counter for satisfying models

    def extract_symbols(self, sentence):
        # Helper method to extract unique symbols from a sentence
        symbols = set()
        # Use regex to find all symbols (variables) in the sentence
        symbols.update(re.findall(r'\b[a-zA-Z][a-zA-Z0-9]*\b', sentence))
        return symbols

    def get_symbols(self):
        # Extract all unique symbols from the knowledge base and query
        symbols = set()
        for sentence in self.kb:
            # Update the symbols set with symbols from each sentence
            symbols.update(self.extract_symbols(sentence))
        # Include symbols from the query
        symbols.update(self.extract_symbols(self.query))
        return list(symbols)

    def tokenizer(self, sentence):
        # Tokenize the sentence into symbols and logical operators using regex
        return re.findall(r'[a-zA-Z0-9]+|<=>|=>|&|\|\||~|\(|\)', sentence)

    def evaluate(self, sentence, model):
        # Evaluate the truth value of the sentence under the given model
        if not sentence.strip():
            # An empty sentence is considered True
            return True
        tokens = self.tokenizer(sentence)
        stack = []      # Operand stack
        operators = []  # Operator stack

        precedence = {'~': 3, '&': 2, '||': 1, '=>': 0, '<=>': 0}
        associativity = {'~': 'right', '&': 'left',
                         '||': 'left', '=>': 'right', '<=>': 'right'}

        def apply_operator():
            operator = operators.pop()
            if operator == '~':
                operand = stack.pop()
                stack.append(not operand)
            else:
                right = stack.pop()
                left = stack.pop()
                if operator == '&':
                    stack.append(left and right)
                elif operator == '||':
                    stack.append(left or right)
                elif operator == '=>':
                    stack.append(not left or right)
                elif operator == '<=>':
                    stack.append(left == right)

        for token in tokens:
            if token in precedence:
                while (operators and operators[-1] in precedence and
                       ((associativity[token] == 'left' and precedence[token] <= precedence[operators[-1]]) or
                        (associativity[token] == 'right' and precedence[token] < precedence[operators[-1]]))):
                    apply_operator()
                operators.append(token)
            elif token == '(':
                operators.append(token)
            elif token == ')':
                while operators and operators[-1] != '(':
                    apply_operator()
                operators.pop()  # Remove '('
            else:
                stack.append(model.get(token, False))

        while operators:
            apply_operator()

        if len(stack) != 1:
            raise ValueError("Invalid clause evaluation.")
        # Return the final truth value
        return stack.pop()

    def checking(self):
        # Generate all possible models (combinations of truth values)
        models = product([False, True], repeat=len(self.symbols))

        for model_iter in models:
            # Create a model mapping symbols to truth values
            model = dict(zip(self.symbols, model_iter))

            # Check if the model satisfies all sentences in the KB
            if all(self.evaluate(sentence, model) for sentence in self.kb):
                # If it does, add to satisfying models
                self.model_count += 1
                # Evaluate the query in the model
                query_result = self.evaluate(self.query, model)
                # Early termination: the query is false in a satisfying model
                if not query_result:
                    return "NO"

        if self.model_count == 0:
            # No satisfying models found
            return "NO"

        # All satisfying models also satisfy the query
        return f"YES: {self.model_count}"
