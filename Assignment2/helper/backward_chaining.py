from collections import defaultdict

class BackwardChaining:
    def __init__(self, tell_statements):
        # Separate tell_statements into facts and rules within the constructor
        self.facts = set([statement for statement in tell_statements if '=>' not in statement])  # Set of initial facts
        self.rules = defaultdict(list)  # Dictionary to store rules
        self.entailed_symbols = []  # List to store entailed propositions
        
        # Parse tell_statements and store rules in the dictionary
        for statement in tell_statements:
            if '=>' in statement:
                premises, conclusion = statement.split('=>')
                premises = [p.strip() for p in premises.split('&')]
                conclusion = conclusion.strip()
                self.rules[conclusion].append(premises)

    def backward_chain(self, query):
        # Check if the query is in the set of known facts
        if query in self.facts:
            if query not in self.entailed_symbols:
                self.entailed_symbols.append(query)  # Add to entailed symbols if it's a fact
            return True

        # If there are no rules leading to this query, return False
        if query not in self.rules:
            return False

        # Iterate through each rule that can infer this query
        for premises in self.rules[query]:
            # Check all premises of this rule
            if all(self.backward_chain(p) for p in premises):  # Recursively check each premise
                if query not in self.entailed_symbols:
                    self.entailed_symbols.append(query)  # Add to entailed symbols if the query is proven
                return True  # If all premises are true, the query is true

        # If no rules can prove the query, return False
        return False
