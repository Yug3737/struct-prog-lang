# Notes - Simple Expressions

## Readings

* Regular expressions: 
https://en.wikipedia.org/wiki/Regular_expression

* Backus-Naur Form (BNF):
https://en.wikipedia.org/wiki/Backus%E2%80%93Naur_form

* Extended Backus-Naur Form (EBNF):
https://en.wikipedia.org/wiki/Extended_Backus%E2%80%93Naur_form

## Tutorials

* Python RegEx Library: https://www.w3schools.com/python/python_regex.asp

## Tokenizer Comments

This code defines a simple tokenizer, which breaks a stream of characters into a stream of tokens. Tokens are meaningful sequences of characters, such as numbers, operators, or parentheses, that a parser might later process. Here's a breakdown of the code:

### Imports
- **`import re`**: This imports Python's regular expression module, which is used to match patterns in strings.

### Patterns
- **`patterns`**: This is a list of pairs, where each pair consists of a regular expression pattern and a corresponding tag. The patterns cover:
  - Parentheses `(` and `)`.
  - Arithmetic operators `+`, `-`, `*`, `/`.
  - Numbers, which can be integers or floating-point numbers.

- **`re.compile`**: The loop converts each pattern string in `patterns` into a compiled regular expression object, which allows for faster matching.

### Tokenizer Function
- **`def tokenize(characters):`**: This function takes a string of characters as input and returns a list of tokens.
  
- **`tokens = []`**: Initializes an empty list to store the tokens.
  
- **`position = 0`**: Tracks the current position in the character stream.
  
- **`while position < len(characters):`**: Loops through the character stream until all characters have been processed.
  
- **`for pattern, tag in patterns:`**: Iterates through the compiled regular expression patterns.

- **`match = pattern.match(characters, position)`**: Tries to match the pattern starting at the current position in the character stream. If a match is found, the loop breaks.

- **`assert match`**: This ensures that a match was found; otherwise, the program will raise an error. It's a simple form of error checking.

- **`token = { ... }`**: Creates a token as a dictionary containing:
  - `tag`: The type of token (e.g., `"number"`, `"+"`, `"("`).
  - `value`: The actual string that matched the pattern.
  - `position`: The starting position of the token in the original character stream.

- **`tokens.append(token)`**: Adds the token to the `tokens` list.

- **`position = match.end()`**: Moves the position to the end of the matched string, preparing for the next iteration.

### Post-Processing Numbers
- **`for token in tokens:`**: Iterates through the generated tokens.
  
- **`if token["tag"] == "number":`**: Checks if the token is a number.
  
- **`token["value"] = float(token["value"])`**: Converts the token's value to a `float` if it contains a decimal point.
  
- **`else: token["value"] = int(token["value"])`**: Converts the token's value to an `int` if it is an integer.

- **`return tokens`**: The function returns the list of tokens.

### Testing
- **`def test_simple_tokens():`**: This is a simple test function to verify the correctness of the tokenizer.

- **`assert tokenize("+") == ...`**: These assertions check that the tokenizer correctly identifies individual tokens for `+`, `-`, `*`, `/`, `(`, `)`.

- **`for number in ["123.45", "1.", ".1", "123"]:`**: This loop tests that numbers, whether integers or floating-point, are correctly tokenized and converted to the appropriate numeric type.

### Main Execution
- **`if __name__ == "__main__":`**: This block runs the `test_simple_tokens` function when the script is executed directly. If the assertions pass, "done." is printed.

### Summary
The code is a straightforward implementation of a tokenizer, designed to break down a stream of characters (such as a mathematical expression) into meaningful tokens. It identifies numbers and basic arithmetic operators and checks its own functionality with a test function. This is useful in the initial stages of creating a parser or interpreter for a programming language.

