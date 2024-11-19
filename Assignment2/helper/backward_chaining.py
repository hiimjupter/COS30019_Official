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

    def backward_chain(self, query, visited=None):
        if visited is None:
            visited = set()

        # If the query is already a fact, it is entailed
        if query in self.facts:
            if query not in self.entailed_symbols:
                self.entailed_symbols.append(query)  # Add to entailed symbols if it's a fact
            return True

        # If the query is in the current branch's visited set, return False to prevent infinite recursion
        if query in visited:
            return False

        # Mark this query as visited in the current branch
        visited.add(query)

        # If there are no rules to infer the query, return False
        if query not in self.rules:
            return False

        # Check all rules that can infer this query
        for premises in self.rules[query]:
            # Check all premises in this rule recursively
            if all(self.backward_chain(p, visited) for p in premises):
                if query not in self.entailed_symbols:
                    self.entailed_symbols.append(query)  # Add to entailed symbols if the query is proven
                visited.remove(query)  # Remove query from visited as we exit this branch
                return True  # If all premises are true, the query is true

        # Remove query from visited as we exit this branch (backtrack)
        visited.remove(query)
        return False  # If no rule could infer the query
