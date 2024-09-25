
from tokenizer import tokenize
from parser import parse

def evaluate(ast, environment):
    if ast["tag"] == 'number':
        assert type(ast["value"]) in [float, int], f"unexpected numerical type { type(ast['value'])}"
        return ast['value'], False # False for the event chain which we are not a part of right now
    if ast["tag"] == "+":
        left_value, _ = evaluate(ast["left"], environment)
        right_value, _ = evaluate(ast["right"], environment)
        return left_value + right_value, False
    if ast["tag"] == "-":
        left_value, _ = evaluate(ast["left"], environment)
        right_value, _ = evaluate(ast["right"], environment)
        return left_value - right_value, False
    if ast["tag"] == "*":
        left_value, _ = evaluate(ast["left"], environment)
        right_value, _ = evaluate(ast["right"], environment)
        return left_value * right_value, False
    if ast["tag"] == "/":
        left_value, _ = evaluate(ast["left"], environment)
        right_value, _ = evaluate(ast["right"], environment)
        assert right_value != 0, "Division by 0"
        return left_value / right_value, False
    if ast["tag"] == "negate":
        value, _ = evaluate(ast["value"], environment)
        return -value, False
    if ast["tag"] == "&&":
        left_value, _ = evaluate(ast["left"], environment)
        right_value, _ = evaluate(ast["right"], environment)
        return left_value and right_value, False
    if ast["tag"] == "||":
        left_value, _ = evaluate(ast["left"], environment)
        right_value, _ = evaluate(ast["right"], environment)
        return left_value or right_value, False
    if ast["tag"] == "!":
        value, _ = evaluate(ast["value"], environment)
        return not value, False
    if ast["tag"] == ">":
        left_value, _ = evaluate(ast["left"], environment)
        right_value, _ = evaluate(ast["right"], environment)
        return left_value > right_value, False
    if ast["tag"] == ">=":
        left_value, _ = evaluate(ast["left"], environment)
        right_value, _ = evaluate(ast["right"], environment)
        return left_value >= right_value, False
    if ast["tag"] == "<":
        left_value, _ = evaluate(ast["left"], environment)
        right_value, _ = evaluate(ast["right"], environment)
        return left_value < right_value, False
    if ast["tag"] == "<=":
        left_value, _ = evaluate(ast["left"], environment)
        right_value, _ = evaluate(ast["right"], environment)
        return left_value <= right_value, False
    if ast["tag"] == "==":
        left_value, _ = evaluate(ast["left"], environment)
        right_value, _ = evaluate(ast["right"], environment)
        return left_value == right_value, False
    if ast["tag"] == "!=":
        left_value, _ = evaluate(ast["left"], environment)
        right_value, _ = evaluate(ast["right"], environment)
        return left_value != right_value, False
    if ast["tag"] == "print":
        if ast["value"]:
            value, _ = evaluate(ast["value", environment])
            print(value)
        else:
            print()
            return None, False
    assert False, "Unknown operator in AST"

def equals(code, environment, expected_result, expected_environment=None):
    result, _ = evaluate(parse(tokenize(code)), environment)
    assert (result == expected_result), f"""ERROR: When executing
    {[code]} 
    -- expected result -- 
    {[expected_result]}
    -- got --
    {[result]}."""
    if expected_environment != None:
        assert (
            environment == expected_environment
        ), f"""ERROR: When executing
        {[code]} 
        -- expected environment -- 
        {[expected_environment]}
        -- got --
        {[environment]}."""

def test_evaluate_single_value():
    print("test evaluate single value")
    equals("3",{},3,{})
    equals("4",{},4,{})
    equals("4.2",{},4.2,{})

def test_evaluate_addition():
    print("testing evaluate addition")
    equals("1+1", {}, 2, {})
    equals("1+2+3", {}, 6, {})
    equals("1.2+2.3+3.4", {}, 6.9, {})

def test_evaluate_subtraction():
    print("testing evaluate subtraction")
    equals("1-1", {}, 0, {})
    equals("3-2-1", {}, 0, {})

def test_evaluate_multiplication():
    print("testing evaluate multiplication")
    equals("1*1", {}, 1, {})
    equals("3+2*2", {}, 7, {})
    equals("3*2*2", {}, 12, {})
    equals("(3+2)*2", {}, 10,{})

def test_evaluate_division():
    print("testing evaluate division")
    equals("4/2", {}, 2, {})
    equals("8/4/2", {}, 1, {})

def test_evaluate_negate():
    print("testing evaluate multiplication")
    equals("-4", {}, -4, {})
    equals("--3", {}, 3, {})

def test_print_statement():
    print("testing print statement")
    equals("print()", {}, None, {})
    equals("print(50+7)", {}, None, {})

if __name__ == "__main__":
    test_evaluate_single_value()
    test_evaluate_addition()
    test_evaluate_multiplication()
    test_evaluate_division()
    test_print_statement()
    test_evaluate_negate()
    print("done.")
