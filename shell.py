from parser import parse
from expression import Environment
from constants import special 

def main_loop():
    parent_env = Environment(special)
    while(True):
        s = input("$ ")
        parsed = parse(s, parent_env)
        print(parsed.evaluate(parent_env))

if __name__ == "__main__":
    main_loop()
