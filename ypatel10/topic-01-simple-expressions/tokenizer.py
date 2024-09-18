#
# file: tokenizer.py
# author: Yug Patel
# last modified: 14 September 2024 
#
"""
Break character stream into tokens and provide a token stream
"""
# In the real world we would create generators

import re
# Each \ in regex needs to be a \\ in python
patterns = [
    ["\\+\\+", "++"],# [pattern, tag]
    ["\\-\\-", "--"],
    ["\\+", "+"],
    ["\\-", "-"],
    ["\\*", "*"],
    ["\\/", "/"],
    ["\\(", "("],
    ["\\)", ")"],
    ["==", "=="],
    ["!=", "!="],
    [">=", ">="],
    ["<=", "<="],
    [">", ">"],
    ["<", "<"],
    ["=", "="],
    # "==" | "!=" | "<" | ">" | "<=" | ">="
    [
        "(\\d*\\.\\d+)|(\\d+\\.\\d*)|(\\d+)",
        "number",
    ],
    ["and", "and"], ["or", "or"], ["not", "not"],
]

for pattern in patterns:
    pattern[0] = re.compile(pattern[0])

def tokenize(characters: str):
    tokens = []
    position = 0
    while position < len(characters):
        for pattern, tag in patterns:
            match = pattern.match(characters, position)
            if match:
                break
        assert match
        token = {
            'tag': tag,
            'value': match.group(0),
            'position': position,
        }
        tokens.append(token)
        position = match.end()

    for token in tokens: # token post processing
        if token["tag"] == "number":
            if "." in token["value"]:
                token["value"] = float(token["value"])
            else:
                token["value"] = int(token["value"])
    token = {
        "tag": None,
        "value": None,
        "position": position,
    }
    tokens.append(token)
    return tokens

def test_simple_tokens():
    print("Testing simple tokens")
    assert tokenize("+") == [{'tag': '+', 'value': '+', 'position': 0}, {'tag': None, 'value': None, 'position': 1}]
    assert tokenize("_") == [{'tag': '-', 'value': '0', 'position': 0}, {'tag': None, 'value': None, 'position': 1}]
    assert tokenize("+") == [{'tag': '+', 'value': '+', 'position': 0}]
    i = 0
    for char in ["+-/*()"]:
        tokens = tokenize(char)
        assert tokens[0]["tag"] == char
        assert tokens[0]["value"] == char
        assert tokens[0]["position"] == i
        i += 1
    for characters in [")", "(", "+","++","-", "*", "/", "==", "<", ">", ">=", "<=", "==", "!="], "=":
        tokens = tokenize(characters)
        assert tokens[0]["tag"]  == characters, f"Expecting {characters}, got {tokens[0]['tag']}"
        assert tokens[0]["value"]  == characters
    for number in ["123.45", "1.", ".1", "123"]:
        tokens = tokenize(number)
        assert tokens[0]["tag"] == "number"
        assert tokens[0]["value"] == float(number)

if __name__ == "__main__":
    test_simple_tokens()
    print("Testing Done")
    
