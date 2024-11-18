import re


class Reader():
    def __init__(self, filename):
        self.filename = filename

    def read(self):
        """
        Reads the file, processes its content, and returns knowledge base and query.
        Validates that only allowed characters are present.
        Args:
            None
        Returns:
          - tell_statements (list): List of statements before the 'ask' keyword.
          - query_statement (str): The statement immediately following the 'ask' keyword.
        """

        allowed_pattern = re.compile(r'^[a-z0-9~&|=<>\s();]+$')

        with open(self.filename) as file:
            lines = [line.strip().lower().split(";") for line in file]
        flattened_lines = [item for sublist in lines for item in sublist]

        try:
            ask_index = flattened_lines.index('ask')
        except ValueError:
            ask_index = len(flattened_lines)

        tell_statements = []
        for statement in flattened_lines[:ask_index]:
            statement_no_space = statement.replace(" ", "")
            if statement_no_space in ["", "tell", "ask"]:
                continue
            if not allowed_pattern.match(statement_no_space):
                raise ValueError(
                    f"Invalid characters in statement: {statement}")
            tell_statements.append(statement_no_space)

        if ask_index + 1 < len(flattened_lines):
            query = flattened_lines[ask_index + 1].replace(" ", "")
            if not allowed_pattern.match(query):
                raise ValueError(
                    f"Invalid characters in query: {flattened_lines[ask_index + 1]}")
            query_statement = query
        else:
            query_statement = ''

        return tell_statements, query_statement
