"""
parser.py -- implement parser for simple expressions
Accept a string of tokens, return an AST expressed as a stack of dictionaries
"""

"""
    simple_expression = number | "(" expression ")" | "-" simple_expresssion
    factor = simple_expression // a  factor is a component of a 
    term = factor { "*"|"/" factor } // curly brackets means 0 or more
    expression = term { "+"|"-" term }
"""
from pprint import pprint
from tokenizer import tokenize

def parse_simple_expression(tokens):
    """simple_expression = number | "(" expression ")" | "-" simple_expresssion """
    
    if tokens[0]["tag"] == "number":
        return tokens[0], tokens[1:]
    if tokens[0]["tag"] == "(":
        node, tokens = parse_expression(tokens[1:])
        assert tokens[0]["tag"] == ")", "Error: expected ')'"
        return node, tokens[1:]
    if tokens[0]["tag"] == "-":
        node, tokens = parse_simple_expression(tokens[1:])
        # Its tempting to write the negation here, but we dont know what the expression is going to be
        node = {"tag":"negate", "value":node}
        return node, tokens
    
    # If code reaches here , it shouldn't be here
    
def parse_expression(tokens):
    return parse_simple_expression(tokens)
       
def test_parse_simple_expression():
    """simple_expression = number | "(" expression ")" | "-" simple_expresssion """
    print("testing parse simple expression")
    tokens = tokenize("2")
    ast, tokens = parse_simple_expression(tokens) # what we get back are the remaining tokens we did not use
    assert ast["tag"] == "number"
    assert ast["value"] == 2

    # tokens = tokenize("(2)")
    # ast, tokens = parse_simple_expression(tokens) # what we get back are the remaining tokens we did not use
    # assert ast["tag"] == "number"
    # assert ast["value"] == 2

    tokens = tokenize("-(2)")
    ast, tokens = parse_simple_expression(tokens) # what we get back are the remaining tokens we did not use
    assert ast["value"] == 2
    assert ast == {
        "tag": "negate",
        "value": {"position": 2, "tag":"number", "value":2},
    }
    # pprint(ast)

def parse_factor(tokens):
    """
    factor = simple_expression
    """
    return parse_simple_expression(tokens)

def test_parse_factor():
    """
    factor = simple_expression
    """
    for s in ["2", "(2)", "-2"]:
        assert parse_factor(tokenize(s) == parse_expression(tokenize(s)))

if __name__ == "__main__":
    test_parse_simple_expression()
    test_parse_factor()
    print("done")
