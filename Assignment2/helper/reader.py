class Reader():
    def __init__(self, filename):
        self.filename = filename

    def read(self):
        """
        Reads the file, processes its content, and returns knowledge base and query.
        Args:
            None
        Returns:
          - tell_statements (list): List of statements before the 'ask' keyword.
          - query_statement (str): The statement immediately following the 'ask' keyword.
        """
        with open(self.filename) as file:
            # Read the file, strip whitespace, convert to lowercase, and split by semicolon
            lines = [line.strip().lower().split(";") for line in file]
        # Flatten the list of lists into a single list
        flattened_lines = [item for sublist in lines for item in sublist]

        try:
            # Find the index of the 'ask' keyword in the flattened list
            ask_index = flattened_lines.index('ask')
        except ValueError:
            # If 'ask' is not found, set ask_index to the length of the flattened list
            ask_index = len(flattened_lines)

        # Extract tell statements by removing spaces and filtering out empty strings, 'tell', and 'ask'
        tell_statements = [statement.replace(
            " ", "") for statement in flattened_lines[:ask_index] if statement not in ["", "tell", "ask"]]

        # Extract the query statement by removing spaces, if it exists
        query_statement = flattened_lines[ask_index + 1].replace(
            " ", "") if ask_index + 1 < len(flattened_lines) else ''

        return tell_statements, query_statement
