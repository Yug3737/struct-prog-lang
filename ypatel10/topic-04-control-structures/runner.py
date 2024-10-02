import sys
from tokenizer import tokenize
from parser import parse
from evaluator import evaluate
from pprint import pprint

def main():
    # check for arguments
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r") as f:
            source_code = f.read()
        enviornment = {}
        tokens = tokenize(source_code)
        ast = parse(tokens)
        evaluate(ast)
        exit()
    # REPL Loop
    debug = False
    environment = {}
    while True:
        try:
            # read the input
            source_code = input(">> ")
            if source_code.strip() in ["exit", "quit"]:
                break
            if source_code.strip() in ["debug"]:
                debug = not debug
                if debug:
                    print("debugger is on.")
                    pprint(environment)
                else:
                    print("debugger is off")
                continue

            tokens = tokenize(source_code)
            ast = parse(tokens)
            evaluate(ast)
            if debug:
                pprint(environment)
            
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()