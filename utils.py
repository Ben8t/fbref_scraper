import re

def is_date_format(input_string):
    pattern = r'^\d{4}-\d{2}-\d{2}$'
    return bool(re.match(pattern, input_string))

def snake_case_column_names(df):
    # Define a function to convert a string to snake_case
    def to_snake_case(s):
        s = re.sub(r'[^a-zA-Z0-9]+', '_', s)  # Replace all non-alphanumeric characters with underscores
        s = re.sub(r'(?<=[a-z])([A-Z0-9])', r'_\1', s)  # Insert underscore before capital letters or digits following lowercase letters
        return s.lower()

    # Rename the columns using the to_snake_case function
    df.columns = [to_snake_case(col) for col in df.columns]

    return df