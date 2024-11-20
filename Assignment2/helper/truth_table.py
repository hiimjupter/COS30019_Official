import re
from itertools import product


class TruthTable():
    def __init__(self, kb, query):
        # Initialize the knowledge base and query
        self.kb = kb  # Knowledge base: list of logical sentences
        self.query = query  # Query: a single symbol or sentence to prove
        # Extract and sort all unique symbols from KB and query
        self.symbols = sorted(self.get_symbols())
        self.satisfying_models = []  # Stores models that satisfy the KB
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
        return re.findall(r'[a-zA-Z0-9]+|<=>|=>|&|\|||~|\(|\)', sentence)

    def evaluate(self, sentence, model):
        # Evaluate the truth value of the sentence under the given model
        if not sentence.strip():
            # An empty sentence is considered True
            return True
        tokens = self.tokenizer(sentence)
        stack = []      # Operand stack
        operators = []  # Operator stack

        for token in tokens:
            if token in ('=>', '&', '||'):
                # Push operators onto the operator stack
                operators.append(token)
            elif token == '~':
                # Handle NOT operator
                if not stack:
                    raise ValueError("Invalid NOT operation: no operand.")
                operand = stack.pop()
                # Apply NOT to the operand and push result back to stack
                stack.append(not operand)
            else:
                # Token is a symbol, push its value from the model onto the stack
                stack.append(model.get(token, False))
                if operators:
                    operator = operators.pop()
                    if operator == '=>':
                        # Handle implication: (A => B)
                        if len(stack) < 2:
                            raise ValueError(
                                "Invalid implication operation: insufficient operands.")
                        right = stack.pop()
                        left = stack.pop()
                        # A => B is equivalent to (not A) or B
                        stack.append(not left or right)
                    elif operator == '&':
                        # Handle logical AND: (A & B)
                        if len(stack) < 2:
                            raise ValueError(
                                "Invalid AND operation: insufficient operands.")
                        right = stack.pop()
                        left = stack.pop()
                        stack.append(left and right)
                    elif operator == '||':
                        # Handle logical OR: (A | B)
                        if len(stack) < 2:
                            raise ValueError(
                                "Invalid OR operation: insufficient operands.")
                        right = stack.pop()
                        left = stack.pop()
                        stack.append(left or right)
        if len(stack) != 1:
            raise ValueError("Invalid clause evaluation: not in horn form.")
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
                self.satisfying_models.append(model)

        if not self.satisfying_models:
            # No satisfying models found
            return "NO"

        # Check if the query is true in all satisfying models
        entailments = all(model[self.query]
                          for model in self.satisfying_models)

        for model in self.satisfying_models:
            print('Satisfying model:', model)

        if entailments:
            # Query is entailed by the KB
            return f"YES: {self.model_count}"
        else:
            # Query is not entailed
            return "NO"
