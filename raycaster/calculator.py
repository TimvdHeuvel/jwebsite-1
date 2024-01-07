while True:
    x = float(input("x: "))
    y = float(input("y: "))
    op = input("op: ")
    match op:
        case "+":
            print(x+y)
        case "-":
            print(x-y)
        case "*":
            print(x*y)
        case "/":
            print(x/y)
        case "^":
            print(x**y)
        case _:
            print(x+y)