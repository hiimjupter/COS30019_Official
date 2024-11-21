import re


class TruthTable:
    def __init__(self, kb, query):
        # Initialize the knowledge base and query
        self.kb = kb  # Knowledge base: list of logical sentences
        self.query = query  # Query: a single symbol or sentence to prove
        # Extract and sort all unique symbols from KB and query
        self.symbols = sorted(self.get_symbols())
        # Counter for satisfying models where KB and query are true
        self.satisfying_model_count = 0

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

    def tt_check_all(self, symbols, model):
        # Recursive function to evaluate all models
        if not symbols:
            # When all symbols are assigned, check KB and query
            kb_is_true = all(self.evaluate(sentence, model)
                             for sentence in self.kb)
            if not kb_is_true:
                # If KB is false, return True (vacuous entailment)
                return True
            query_is_true = self.evaluate(self.query, model)
            if query_is_true:
                # Count the model where both KB and query are true
                self.satisfying_model_count += 1
            return query_is_true

        # Assign truth values dynamically
        first_symbol = symbols[0]
        rest_symbols = symbols[1:]

        # Assign `True` to the first symbol and check recursively
        model[first_symbol] = True
        if not self.tt_check_all(rest_symbols, model):
            return False  # Early termination if query is false

        # Assign `False` to the first symbol and check recursively
        model[first_symbol] = False
        if not self.tt_check_all(rest_symbols, model):
            return False  # Early termination if query is false

        return True  # If all branches succeed, return True

    def checking(self):
        # Initialize an empty model and start recursive evaluation
        model = {}
        result = self.tt_check_all(self.symbols, model)

        if self.satisfying_model_count == 0:
            # If no models satisfy the KB, the KB is inconsistent
            return "NO"

        if result:
            # If the query is true in all satisfying models, return YES with the count
            return f"YES: {self.satisfying_model_count}"
        else:
            # If the query is false in any satisfying model, return NO
            return "NO"
