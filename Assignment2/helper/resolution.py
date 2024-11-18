import re

def parse_to_clauses(cnf_expression):
    """
    Parse a CNF string into a list of clauses, ensuring negations (~) are preserved.
    Example: "a , ~a" -> [["a"], ["~a"]]
    """
    clauses = []
    # Split the input string by ',' or ';' to separate clauses
    clause_tokens = re.split(r'[;,]', cnf_expression)
    for token in clause_tokens:
        if token.strip():  # Ignore empty tokens
            # Extract literals, allowing for spaces after '~'
            literals = re.findall(r'~?\s*\w+', token.strip())
            # Remove internal spaces within literals (e.g., "~ a" -> "~a")
            literals = [literal.replace(" ", "") for literal in literals]
            clauses.append(tuple(sorted(literals)))
    return clauses

def pl_resolution(kb, alpha):
    """
    Perform the PL-RESOLUTION algorithm.
    :param kb: list of clauses representing the knowledge base (in CNF)
    :param alpha: list of clauses representing the negation of the query (in CNF)
    :return: True if a contradiction is found, False otherwise
    """
    # Combine the knowledge base (KB) and the negation of the query (not alpha)
    clauses = set([tuple(sorted(clause)) for clause in kb] + [tuple(sorted(clause)) for clause in alpha])
    new = set()

    while True:
        # Pairwise resolution of all clauses
        clause_list = list(clauses)
        for i in range(len(clause_list)):
            for j in range(i + 1, len(clause_list)):
                resolvents = pl_resolve(clause_list[i], clause_list[j])
                if () in resolvents:  # Check if the empty clause is generated
                    print("Contradiction found.")
                    return True
                new.update(resolvents)

        # If no new clauses are generated, stop and return False
        if new.issubset(clauses):
            print("No contradiction found.")
            return False

        # Add the new clauses to the knowledge base
        clauses.update(new)

def pl_resolve(ci, cj):
    """
    Perform the resolution between two clauses.
    :param ci: tuple representing the first clause
    :param cj: tuple representing the second clause
    :return: set of resolvent clauses
    """
    resolvents = set()
    for literal in ci:
        # Check if there's a negation of this literal in cj
        if literal.startswith("~"):
            complementary_literal = literal[1:]
        else:
            complementary_literal = "~" + literal

        if complementary_literal in cj:
            # Create a resolvent by removing the negated pair and combining the rest
            new_clause = set(ci).union(set(cj))
            new_clause.discard(literal)
            new_clause.discard(complementary_literal)
            resolvents.add(tuple(sorted(new_clause)))

    return resolvents

def run_resolution(kb, query):
    """
    Main function to execute PL-Resolution from CNF input.
    :param kb: String representing the knowledge base in CNF
    :param query: String representing the query in CNF
    :return: True if the query can be proven, False otherwise
    """
    kb_clauses = parse_to_clauses(kb)
    query_clauses = parse_to_clauses(query)
    negated_query = [tuple(sorted(["~" + literal if not literal.startswith("~") else literal[1:] for literal in clause])) for clause in query_clauses]
    return pl_resolution(kb_clauses, negated_query)