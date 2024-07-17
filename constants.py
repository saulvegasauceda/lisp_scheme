special = {
    "+": lambda x: sum(x),
    "-": lambda x: 
}

def add(args):
    return sum(args)

def subtract(args):
    if len(args) == 1:
        return -args[0]
    
    result = a[0]
    for a in args[1:]:
        result -= a
    return result
        
