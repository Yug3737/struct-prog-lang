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
        node, tokens = parse_expression(tokens[1:]) # Why not use parse_simple_expression()
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

    tokens = tokenize("-(2)")
    ast, tokens = parse_simple_expression(tokens) # what we get back are the remaining tokens we did not use
    assert ast == {
        "tag": "negate",
        "value": {"position": 2, "tag":"number", "value":2},
    }

    # Test Cases for HW1
    # test 1 
    tokens = tokenize("-(100)")
    ast, tokens = parse_simple_expression(tokens)
    assert ast == {
        "tag": "negate",
        "value": {"position": 2, "tag": "number", "value":100},
    }
    # Position 2 tells where our number token 100 starts in the input string

    # test 2
    tokens = tokenize("1.5")
    ast, tokens = parse_simple_expression(tokens)
    assert ast["tag"] == "number"
    assert ast["value"] == 1.5
    assert ast["position"] == 0
    pprint(ast)

def parse_factor(tokens):
    """
    factor = simple_expression
    """
    return parse_simple_expression(tokens)

def test_parse_factor():
    """
    factor = simple_expression
    """
    print("testing parse factor")
    for s in ["2", "(2)", "-2"]:
        assert parse_factor(tokenize(s)) == parse_simple_expression(tokenize(s))

    # Tests for HW1
    for s in ["-1.5", "(10)"]:
        assert parse_factor(tokenize(s)) == parse_simple_expression(tokenize(s))

def parse_term(tokens):
    """
    term = factor { "*"|"/" factor } 
    """
    node, tokens = parse_factor(tokens)
    while tokens[0]["tag"] in ["*","/"]:
        tag = tokens[0]["tag"]
        right_node, tokens = parse_factor(tokens[1:])
        node = {"tag": tag, "left": node, "right": right_node}
    return node, tokens

def test_parse_term():
    """
    term = factor {"*"|"/" factor}
    """
    tokens = tokenize("2*3")
    ast, tokens = parse_term(tokens)
    assert ast == {"left": {'position': 0, 'tag': 'number', 'value': 2},
                    'right': {'position': 2, 'tag': 'number', 'value': 3},
                    'tag': '*'}

    tokens = tokenize("2*3/4*5")
    ast, tokens = parse_term(tokens)
    # pprint(ast)
    assert ast == {
        'left': {
            'left': {
                'left': {'position': 0, 'tag': 'number', 'value': 2},
                'right': {'position': 2, 'tag': 'number', 'value': 3},
                'tag': '*'
            },
            'right': {'position': 4, 'tag': 'number', 'value': 4},
            'tag': '/'
        },
        'right': {'position': 6, 'tag': 'number', 'value': 5},
        'tag': '*'
    }

    # Test Case for HW1
    tokens = tokenize("2/3*6")
    ast, tokens = parse_term(tokens)
    assert ast == {
        'left': {
            'left': {'position': 0, 'tag': 'number', 'value': 2},
            'right': {'position': 2, 'tag': 'number', 'value': 3},
            'tag': '/',
            },
        'right': {'position': 4, 'tag': 'number', 'value': 6},
        'tag': '*'
    }
    

def parse_expression(tokens):
    """
    expression = term { "+"|"-" term }
    """
    node, tokens = parse_term(tokens)
    while tokens[0]["tag"] in ["+","-"]:
        tag = tokens[0]["tag"]
        right_node, tokens = parse_term(tokens[1:])
        # What is happening here?
        node = {"tag": tag, "left": node, "right": right_node}
    return node, tokens

def test_parse_expression():
    """
    expression = term { "+"|"-" term }
    """
    print("testing parse expression")
    tokens = tokenize("2+3")
    ast, tokens = parse_expression(tokens)
    assert ast == {
        "left": {"position": 0, "tag": "number", "value": 2},
        "right": {"position": 2, "tag": "number", "value": 3},
        "tag": "+",
    }
    
    tokens = tokenize("2+3-4+5")
    ast, tokens = parse_expression(tokens)
    assert ast == {
        "left": {
            "left": {
                "left": {"position": 0, "tag": "number", "value": 2},
                "right": {"position": 2, "tag": "number", "value": 3},
                "tag": "+",
            },
            "right": {"position": 4, "tag": "number", "value": 4},
            "tag": "-",
        },
        "right": {"position": 6, "tag": "number", "value": 5},
        "tag": "+",
    }

    tokens = tokenize("2+3*4+5")
    ast, tokens = parse_expression(tokens)
    assert ast == {
        "left": {
            "left": {"position": 0, "tag": "number", "value": 2},
            "right": {
                "left": {"position": 2, "tag": "number", "value": 3},
                "right": {"position": 4, "tag": "number", "value": 4},
                "tag": "*",
            },
            "tag": "+",
        },
        "right": {"position": 6, "tag": "number", "value": 5},
        "tag": "+",
    }
    
    # Test Case for HW1
    tokens = tokenize("2*3+4*5")
    ast, tokens = parse_expression(tokens)
    assert ast == {
        'left': {
            'left': {'position': 0, 'tag': 'number', 'value': 2},
            'right': {'position': 2, 'tag': 'number', 'value': 3},
            'tag': '*'},
        'right': {
            'left': {'position': 4, 'tag': 'number', 'value': 4},
            'right': {'position': 6, 'tag': 'number', 'value': 5},
            'tag': '*'},
        'tag': '+'
    }

def parse(tokens):
    ast, tokens = parse_expression(tokens)
    return parse_expression(tokens)

def test_parse():
    print("testing parse")
    tokens = tokenize("2+3*4+5")
    ast, _ = parse_expression(tokens)
    print(tokens)
    assert parse(tokens) == ast
    
if __name__ == "__main__":
    test_parse_simple_expression()
    test_parse_factor()
    test_parse_term()
    test_parse_expression()
    test_parse()
    print("done")
