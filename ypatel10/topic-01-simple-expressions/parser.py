"""
parser.py -- implement parser for simple expressions

Accept a string of tokens, return an AST expressed as stack of dictionaries
"""
"""
    simple_expression = number | "(" expression ")" | "-" simple_expression
    factor = simple_expression
    term = factor { "*"|"/" factor }
    arithmetic_expression = term { "+"|"-" term }
    comparison_expression = arithmetic_expression ["==" | "!=" | "<" | ">" | "<=" | ">=" arithmetic_expression]
    boolean_expression == comparision_expression {"or" comparision_expression}
    boolean_term == boolean_term {or boolean_term} # curly braces means multiples
    expression = boolean_expression
"""

from pprint import pprint

from tokenizer import tokenize

def parse_simple_expression(tokens):
    """
    simple_expression = number | "(" expression ")" | "-" simple_expression
    """
    if tokens[0]["tag"] == "number":
        return tokens[0], tokens[1:]
    if tokens[0]["tag"] == "(":
        node, tokens = parse_expression(tokens[1:])
        assert tokens[0]["tag"] == ")", "Error: expected ')'"
        return node, tokens[1:]
    if tokens[0]["tag"] == "-":
        node, tokens = parse_simple_expression(tokens[1:])
        node = {"tag":"negate", "value":node}
        return node, tokens


def parse_expression(tokens):
    return parse_simple_expression(tokens)

def test_parse_simple_expression():
    """
    simple_expression = number | "(" expression ")" | "-" simple_expression
    """
    print("testing parse_simple_expression")
    tokens = tokenize("2")
    ast, tokens = parse_simple_expression(tokens)
    assert ast["tag"] == "number"
    assert ast["value"] == 2
    # pprint(ast)
    tokens = tokenize("(2)")
    ast, tokens = parse_simple_expression(tokens)
    assert ast["tag"] == "number"
    assert ast["value"] == 2
    # pprint(ast)
    tokens = tokenize("-2")
    ast, tokens = parse_simple_expression(tokens)
    assert ast == {
        "tag": "negate",
        "value": {"position": 1, "tag": "number", "value": 2},
    }
    # pprint(ast)
    tokens = tokenize("-(2)")
    ast, tokens = parse_simple_expression(tokens)
    assert ast == {
        "tag": "negate",
        "value": {"position": 2, "tag": "number", "value": 2},
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
    print("testing parse_factor")
    for s in ["2", "(2)", "-2"]:
        assert parse_factor(tokenize(s)) == parse_simple_expression(tokenize(s))


def parse_term(tokens):
    """
    term = factor { "*"|"/" factor }
    """
    node, tokens = parse_factor(tokens)
    while tokens[0]["tag"] in ["*", "/"]:
        tag = tokens[0]["tag"]
        right_node, tokens = parse_factor(tokens[1:])
        node = {"tag": tag, "left": node, "right": right_node}
    return node, tokens


def test_parse_term():
    """
    term = factor { "*"|"/" factor }
    """
    print("testing parse_term")
    tokens = tokenize("2*3")
    ast, tokens = parse_term(tokens)
    assert ast == {'left': {'position': 0, 'tag': 'number', 'value': 2},'right': {'position': 2, 'tag': 'number', 'value': 3},'tag': '*'}    
    tokens = tokenize("2*3/4*5")
    ast, tokens = parse_term(tokens)
    assert ast == {
        "left": {
            "left": {
                "left": {"position": 0, "tag": "number", "value": 2},
                "right": {"position": 2, "tag": "number", "value": 3},
                "tag": "*",
            },
            "right": {"position": 4, "tag": "number", "value": 4},
            "tag": "/",
        },
        "right": {"position": 6, "tag": "number", "value": 5},
        "tag": "*",
    }


def parse_expression(tokens):
    """
    expression = term { "+"|"-" term }
    """
    node, tokens = parse_term(tokens)
    while tokens[0]["tag"] in ["+", "-"]:
        tag = tokens[0]["tag"]
        right_node, tokens = parse_term(tokens[1:])
        node = {"tag": tag, "left": node, "right": right_node}
    return node, tokens

def parse_arithmetic_expression(tokens):
    """
    expression = term { "+"|"-" term }
    """
    node, tokens = parse_term(tokens)
    while tokens[0]["tag"] in ["+", "-"]:
        tag = tokens[0]["tag"]
        right_node, tokens = parse_term(tokens[1:])
        node = {"tag": tag, "left": node, "right": right_node}
    return node, tokens

def parse_comparison_expression(tokens):
    return parse_arithmetic_expression(tokens)

def test_parse_comparison_expression():
    """comparison_expression = arithmetic_expression ["==" | "!=" | "<" | ">" | "<=" | ">=" arithmetic_expression] """
    print("testing parse_comparison_expression")
    for op in ["<", ">"]:
        tokens = tokenize(f"2{op}3")
        ast, tokens = parse_comparison_expression(tokens)
        assert ast == {
            "left": {"position": 0, "tag": "number", "value": 2},
            "right": {"position": 2, "tag": "number", "value": 3},
            "tag": op,
        }
    for op in ["==", ">=", "<=", "!="]:
        tokens = tokenize(f"2{op}3")
        ast, tokens = parse_comparison_expression(tokens)
        assert ast == {
            "left": {"position": 0, "tag": "number", "value": 2},
            "right": {"position": 2, "tag": "number", "value": 3},
            "tag": op,
        }


def test_parse_arithmetic_expression():
    """
    expression = term { "+"|"-" term }
    """
    print("testing parse_arithmetic_expression")
    tokens = tokenize("2+3")
    ast, tokens = parse_arithmetic_expression(tokens)
    assert ast == {
        "left": {"position": 0, "tag": "number", "value": 2},
        "right": {"position": 2, "tag": "number", "value": 3},
        "tag": "+",
    }
    tokens = tokenize("2+3-4+5")
    ast, tokens = parse_arithmetic_expression(tokens)
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
    ast, tokens = parse_arithmetic_expression(tokens)
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

def test_parse_expression():
    """
    expression = term { "+"|"-" term }
    """
    print("testing parse_expression")
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

def parse_boolean_expression(tokens):
    """ boolean_expression == comparision_expression {"or" comparision_expression} """
    pass

def test_parse_boolean_expression(tokens):
    """ boolean_expression == comparision_expression {"or" comparision_expression} """
    pass

def test_parse_boolean_term(tokens):
    """ boolean_term == boolean_term {or boolean_term} # curly braces means multiples """
    pass

def parse_boolean_term(tokens):
    """ boolean_term == boolean_term {or boolean_term} # curly braces means multiples """
    pass

def parse(tokens):
    ast, tokens = parse_comparision_expression(tokens)
    return ast 

def test_parse():
    print("testing parse")
    tokens = tokenize("2+3*4+5")
    ast, _ = parse_boolean_expression(tokens)
    assert parse(tokens) == ast
    tokens = tokenize("1*2<3*4or5>6and7")
    ast, _ = parse_boolean_expression(tokens)
    assert ast == {}
    print(ast)
    exit()

if __name__ == "__main__":
    test_parse_simple_expression()
    test_parse_factor()
    test_parse_term()
    test_parse_expression()
    test_parse()
    test_parse_arithmetic_expression()
    print("done")