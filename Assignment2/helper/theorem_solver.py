import re
from collections import deque


class Clause:
    def __init__(self, literals):
        self.literals = set(literals)

    def is_contradictory(self):
        return len(self.literals) == 0

    def __eq__(self, other):
        return self.literals == other.literals

    def __hash__(self):
        return hash(frozenset(self.literals))

    def __str__(self):
        return ' | '.join(map(str, self.literals))


class Literal:
    def __init__(self, predicate, args, negated=False):
        self.predicate = predicate
        self.args = args
        self.negated = negated

    def __neg__(self):
        return Literal(self.predicate, self.args, not self.negated)

    def __eq__(self, other):
        return (self.predicate == other.predicate and
                self.args == other.args and
                self.negated == other.negated)

    def __hash__(self):
        return hash((self.predicate, tuple(self.args), self.negated))

    def __str__(self):
        neg = '~' if self.negated else ''
        args = ','.join(self.args)
        return f"{neg} {self.predicate}({args})"


def parse_literal(literal_str):
    literal_str = literal_str.strip()
    negated = False
    if literal_str.startswith('~'):
        negated = True
        literal_str = literal_str[1:]
    match = re.match(r'(\w+)\((.*)\)', literal_str)
    if match:
        predicate = match.group(1)
        args = match.group(2).split(',')
        args = [arg.strip() for arg in args]
        return Literal(predicate, args, negated)
    else:
        raise ValueError(f"Invalid literal: {literal_str}")


def parse_clause(clause_str):
    literals = clause_str.strip().split('|')
    literals = [parse_literal(lit_str) for lit_str in literals]
    return Clause(literals)


def standardize_clause(clause, index):
    var_mapping = {}
    new_literals = []
    for lit in clause.literals:
        new_args = []
        for arg in lit.args:
            if is_variable(arg):
                if arg not in var_mapping:
                    var_mapping[arg] = f"{arg}_{index}"
                new_args.append(var_mapping[arg])
            else:
                new_args.append(arg)
        new_literals.append(Literal(lit.predicate, new_args, lit.negated))
    return Clause(new_literals)


def is_variable(term):
    return term.islower() and term[0].islower()


def unify(x, y, theta=None):
    if theta is None:
        theta = {}
    if x == y:
        return theta
    elif is_variable(x):
        return unify_var(x, y, theta)
    elif is_variable(y):
        return unify_var(y, x, theta)
    elif isinstance(x, list) and isinstance(y, list) and len(x) == len(y):
        for xi, yi in zip(x, y):
            theta = unify(xi, yi, theta)
            if theta is None:
                return None
        return theta
    else:
        return None


def unify_var(var, x, theta):
    if var in theta:
        return unify(theta[var], x, theta)
    elif x in theta:
        return unify(var, theta[x], theta)
    elif occurs_check(var, x, theta):
        return None
    else:
        theta[var] = x
        return theta


def occurs_check(var, x, theta):
    if var == x:
        return True
    elif is_variable(x) and x in theta:
        return occurs_check(var, theta[x], theta)
    return False


def resolve(ci, cj):
    resolvents = set()
    for li in ci.literals:
        for lj in cj.literals:
            if li.predicate == lj.predicate and li.negated != lj.negated:
                theta = unify(li.args, lj.args)
                if theta is not None:
                    ci_literals = substitute(ci.literals - {li}, theta)
                    cj_literals = substitute(cj.literals - {lj}, theta)
                    new_literals = ci_literals.union(cj_literals)
                    resolvent = Clause(new_literals)
                    resolvents.add(resolvent)
    return resolvents


def substitute(literals, theta):
    new_literals = set()
    for lit in literals:
        new_args = [theta.get(arg, arg) for arg in lit.args]
        new_literals.add(Literal(lit.predicate, new_args, lit.negated))
    return new_literals


def resolution(kb_clauses, query_clause):
    clauses = set()
    index = 0
    for clause in kb_clauses:
        clauses.add(standardize_clause(clause, index))
        index += 1
    clauses.add(standardize_clause(negate_clause(query_clause), index))
    index += 1
    new = set()
    while True:
        pairs = []
        clause_list = list(clauses)
        for i in range(len(clause_list)):
            for j in range(i+1, len(clause_list)):
                pairs.append((clause_list[i], clause_list[j]))
        for (ci, cj) in pairs:
            resolvents = resolve(ci, cj)
            if Clause(set()) in resolvents:
                return True
            new = new.union(resolvents)
        if new.issubset(clauses):
            return False
        clauses = clauses.union(new)


def negate_clause(clause):
    new_literals = []
    for lit in clause.literals:
        new_literals.append(Literal(lit.predicate, lit.args, not lit.negated))
    return Clause(set(new_literals))


def main():
    # Example knowledge base and query
    kb = [
        'Mother(x,y) => Parent(x,y)',
        'Father(x,y) => Parent(x,y)',
        'Mother(Alice,Bob)',
        'Father(Tom,Bob)',
    ]
    query = 'Parent(Alice,Bob)'

    # Parse clauses
    kb_clauses = [parse_clause(s) for s in kb]
    query_clause = parse_clause(query)

    print('Knowledge Base: ', kb_clauses)
    print('Query: ', query_clause)

    # Perform resolution
    result = resolution(kb_clauses, query_clause)

    if result:
        print('YES')
    else:
        print('NO')


if __name__ == '__main__':
    main()
