from parser import parse

def main_loop():
    while(True):
        s = input("$ ")
        parsed = parse(s)
        print(parsed.evaluate())

if __name__ == "__main__":
    main_loop()
