import re

# Function to parse a logical expression into individual tokens
def parse_expression(expr):
    """
    Parse the logical expression into tokens.
    """
    # Use regex to match operators, parentheses, and variables in the input expression
    tokens = re.findall(r'[a-zA-Z]+|~|&|\|\||=>|<=>|\(|\)|,|;', expr)
    return tokens


# Function to convert equivalence operators ('<=>') to implications
def convert_equivalence(expression):
    def handle_equivalence(expr):
        i = 0
        while i < len(expr):
            if expr[i] == '<=>':
                # Find the left-hand side of "<=>"
                left_expression = []
                j = i - 1
                if expr[j] == ')':  # If the left-hand side is a group within parentheses
                    bracket_count = 1
                    left_expression.append(expr[j])
                    j -= 1
                    while j >= 0 and bracket_count > 0:
                        left_expression.append(expr[j])
                        if expr[j] == ')':
                            bracket_count += 1
                        elif expr[j] == '(':
                            bracket_count -= 1
                        j -= 1
                    left_expression.reverse()
                else:  # If the left-hand side is a single variable or value
                    left_expression = [expr[j]]
                    j -= 1

                # Find the right-hand side of "<=>"
                right_expression = []
                k = i + 1
                if expr[k] == '(':  # If the right-hand side is a group within parentheses
                    bracket_count = 1
                    right_expression.append(expr[k])
                    k += 1
                    while k < len(expr) and bracket_count > 0:
                        right_expression.append(expr[k])
                        if expr[k] == '(':  # Count open parentheses
                            bracket_count += 1
                        elif expr[k] == ')':  # Count closed parentheses
                            bracket_count -= 1
                        k += 1
                else:  # If the right-hand side is a single variable or value
                    right_expression = [expr[k]]
                    k += 1

                # Recursively handle equivalence on the left and right expressions
                left_processed = handle_equivalence(left_expression)
                right_processed = handle_equivalence(right_expression)

                # Convert "A <=> B" into "(A => B) & (B => A)"
                left_implication = ['('] + left_processed + ['=>'] + right_processed + [')']
                right_implication = ['('] + right_processed + ['=>'] + left_processed + [')']
                new_expression = ['('] + left_implication + ['&'] + right_implication + [')']

                # Replace "<=>" in the expression with the new converted expression
                expr = expr[:j + 1] + new_expression + expr[k:]

                # Update index to continue after the newly inserted expression
                i = j + len(new_expression)
            else:
                i += 1
        return expr

    # Recursively handle equivalence operators in the entire expression
    return handle_equivalence(expression)

# Function to eliminate implication operators ('=>') from the logical expression
def eliminate_implication(expression):
    i = 0
    while i < len(expression):
        if expression[i] == '=>':
            # Find the left-hand side of "=>"
            if expression[i - 1] == ')':
                # If the left-hand side is a group, find the matching parentheses
                open_bracket_index = i - 1
                bracket_count = 1
                while open_bracket_index > 0:
                    open_bracket_index -= 1
                    if expression[open_bracket_index] == ')':
                        bracket_count += 1
                    elif expression[open_bracket_index] == '(':
                        bracket_count -= 1
                        if bracket_count == 0:
                            break

                # Add negation "~" before the left-hand side
                expression.insert(open_bracket_index, '~')
                i += 1  # Update index due to insertion
            else:
                # If it's a single variable, just negate it
                expression.insert(i - 1, '~')
                i += 1  # Update index due to insertion

            # Replace "=>" with "||" (logical OR)
            expression[i] = '||'
        
        i += 1  # Move to the next token
    return expression

# Function to apply negation rules (De Morgan's laws)
def convert_negation(expression):
    def process_sub_expression(sub_expr):
        # Recursively process sub-expressions
        if '&' in sub_expr:
            # Split sub-expression by '&'
            parts = []
            temp = []
            for item in sub_expr:
                if item == '&':
                    parts.append(temp)
                    temp = []
                else:
                    temp.append(item)
            parts.append(temp)

            # Apply De Morgan's law to convert ~(F & G & H) to ~F || ~G || ~H
            transformed = []
            for part in parts:
                if transformed:
                    transformed.extend(['||'])
                transformed.extend(['~'] + part)
            return transformed

        elif '||' in sub_expr:
            # Split sub-expression by '||'
            parts = []
            temp = []
            for item in sub_expr:
                if item == '||':
                    parts.append(temp)
                    temp = []
                else:
                    temp.append(item)
            parts.append(temp)

            # Apply De Morgan's law to convert ~(F || G || H) to ~F & ~G & ~H
            transformed = []
            for part in parts:
                if transformed:
                    transformed.extend(['&'])
                transformed.extend(['~'] + part)
            return transformed

        return ['~'] + sub_expr

    # Main loop to process the entire expression
    result = []
    i = 0
    while i < len(expression):
        if expression[i] == '~' and i + 1 < len(expression) and expression[i + 1] == '(':
            # Handle negation of a sub-expression
            j = i + 2
            sub_expression = []
            bracket_count = 1
            while j < len(expression) and bracket_count > 0:
                if expression[j] == '(':
                    bracket_count += 1
                elif expression[j] == ')':
                    bracket_count -= 1
                if bracket_count > 0:
                    sub_expression.append(expression[j])
                j += 1

            # Recursively process the sub-expression
            transformed_sub_expression = process_sub_expression(sub_expression)
            result.extend(transformed_sub_expression)
            i = j  # Skip processed part
        else:
            result.append(expression[i])
            i += 1

    return result

# Function to simplify double negation (~~) in the expression
def simplify_double_negation(expression):
    def process_sub_expression(sub_expr):
        # Recursive function to handle nested expressions
        result = []
        i = 0
        while i < len(sub_expr):
            if sub_expr[i] == '~' and i + 1 < len(sub_expr) and sub_expr[i + 1] == '~':
                # Remove double negation by skipping both
                i += 2
            elif sub_expr[i] == '(':
                # Extract and process the inner sub-expression
                j = i + 1
                bracket_count = 1
                inner_expression = []
                while j < len(sub_expr) and bracket_count > 0:
                    if sub_expr[j] == '(':
                        bracket_count += 1
                    elif sub_expr[j] == ')':
                        bracket_count -= 1
                    if bracket_count > 0:
                        inner_expression.append(sub_expr[j])
                    j += 1
                # Recursively process the inner expression
                processed_inner = process_sub_expression(inner_expression)
                result.append('(')
                result.extend(processed_inner)
                result.append(')')
                i = j
            else:
                result.append(sub_expr[i])
                i += 1
        return result

    # Main processing loop
    result = []
    i = 0
    while i < len(expression):
        if expression[i] == '~' and i + 1 < len(expression) and expression[i + 1] == '~':
            # Simplify double negation by skipping both '~'
            i += 2
        elif expression[i] == '(':
            # Extract and process the inner expression
            j = i + 1
            bracket_count = 1
            inner_expression = []
            while j < len(expression) and bracket_count > 0:
                if expression[j] == '(':
                    bracket_count += 1
                elif expression[j] == ')':
                    bracket_count -= 1
                if bracket_count > 0:
                    inner_expression.append(expression[j])
                j += 1
            # Recursively process the inner expression
            processed_inner = process_sub_expression(inner_expression)
            result.append('(')
            result.extend(processed_inner)
            result.append(')')
            i = j
        else:
            result.append(expression[i])
            i += 1

    return result

# Main function to convert an expression to CNF (Conjunctive Normal Form)
def convert_to_cnf(expression):

    # Step 1: Convert equivalence operators
    equivalence_tokens = convert_equivalence(expression)
    # print("After Equivalence: ", " ".join(equivalence_tokens))

    # Step 2: Eliminate implications
    implication_tokens = eliminate_implication(equivalence_tokens)
    # print("After Implication: ", " ".join(implication_tokens))

    # Step 3: Apply negation rules (De Morgan's law)
    convert_negation_tokens = convert_negation(implication_tokens)
    # print("After Negation: ", " ".join(convert_negation_tokens))

    # Step 4: Simplify double negations
    double_negation_tokens = simplify_double_negation(convert_negation_tokens)
    # print("After Double Negation: ", " ".join(double_negation_tokens))

    # Convert list of tokens to a single string representation
    result = " ".join(double_negation_tokens)

    return result