from collections import defaultdict, deque

class ForwardChaining:
    def __init__(self, kb, query):
        self.kb = self.parse_kb(kb)  # Convert KB from string format to data structure
        self.query = query  # Query to be inferred
        self.count = defaultdict(int)  # Number of premises needed to infer each Horn clause result
        self.inferred = defaultdict(bool)  # Inference status of each symbol
        self.agenda = deque()  # List of known true facts

        # Initialize count and agenda from KB
        for premises, head in self.kb:
            self.count[head] = len(premises)
            # If there are no premises, the conclusion is true and added to the agenda
            if len(premises) == 0:
                self.agenda.append(head)
            for symbol in premises + [head]:
                self.inferred[symbol] = False  # Mark all symbols as initially uninferred

    def parse_kb(self, kb_str):
        """
        Converts the knowledge base (KB) string into a list of (premises, head) pairs.
        Ensures the KB follows Horn clause rules.
        """
        kb = []
        clauses = kb_str.split(';')
        for clause in clauses:
            clause = clause.strip()
            if '<=>' in clause:
                # Raise error for unsupported biconditional
                raise ValueError(f"Invalid clause: '{clause}' contains '<=>' which is not allowed in Horn clauses.")
            elif '=>' in clause:
                # Properly split on '=>'
                premises, head = clause.split('=>')
                premises = [p.strip() for p in premises.split('&')]
                head = head.strip()
            elif '~' in clause or '||' in clause:
                # Disallow negation and disjunction
                raise ValueError(f"Invalid clause: '{clause}' contains unsupported operators (negation or disjunction).")
            else:
                # If there are no premises, this is an initial fact
                premises = []
                head = clause.strip()

            # Validate that the clause is a Horn clause
            if len(premises) > 1 and not head:
                raise ValueError(f"Invalid clause: '{clause}' is not a Horn clause. Horn clauses must have at most one head.")
            kb.append((premises, head))
        return kb

    def entails(self):
        """
        Perform Forward Chaining to check entailment.
        Returns:
            str: "YES: <entailed_symbols>" if the query can be inferred, otherwise "NO".
        """
        entailed_symbols = []  # Store symbols that have been inferred

        while self.agenda:
            p = self.agenda.popleft()  # Get a symbol from the agenda
            if not self.inferred[p]:   # If this symbol has not been inferred yet
                self.inferred[p] = True  # Mark it as inferred
                entailed_symbols.append(p)  # Add it to the list of inferred symbols

                # Process each clause that has p in its premises
                for premises, head in self.kb:
                    if p in premises:
                        self.count[head] -= 1
                        # If all premises are satisfied, infer the head
                        if self.count[head] == 0 and not self.inferred[head]:
                            self.agenda.append(head)

        # After processing the entire agenda, check if the query was entailed
        if self.inferred[self.query]:
            entailed_list = ', '.join(entailed_symbols)
            return f"YES: {entailed_list}"
        else:
            return "NO"
