'''Created by Adrian Price, 30588812 for FIT 1053'''
from math import pow

'''Global scope variable declaration and instantiation'''
validOperators = ["+", "-", "*", "/", "^"]
parenthesis = ["(", ")"]
whiteSpace = " "

def stringToNumber (strExpression):
    '''Input: takes a string
       Output: if it is a whole number an integer version, if it is a decimal a float version'''
    if isNumber(strExpression):
        num = float(strExpression)
    else:
        print("Invalid input for stringToNumber function")
        print(strExpression)
        exit()
    return num

def isNumber(strExpression):
    '''Input: takes a string
       Output: true if it is a number and false if it is not'''
    try:
        float(strExpression)
        return True
    except:
        if strExpression == ".":
            return True
        else:
            return False

def containsParenthesis(tokens):
    for x in range(len(tokens)):
        if  tokens[x] in parenthesis:
            return True
    return False

def doOperation (num1, num2, op):
    '''Input: two numbers and an operator
       Outpuut: an answer with respect to the inputed numbers and the operator'''
    if op in validOperators:
        if op == "+":
            answer = num1 + num2
        elif op == "-":
            answer = num1 - num2
        elif op == "*":
            answer = num1 * num2
        elif op == "/":
            answer = num1 / num2
        elif op == "^":
            answer = pow(num1, num2)
    else:
        print("Invalid op input for doOperation")
        print(op)
        exit()

    return answer

def tokenization(expr):
    '''Input: a string representing a mathematical expression or non-negative numbers
       Output: a list of tokens (operators, numbers, parenthesis, not whitespaces etc) from the given expression'''
    tokens = []
    x = 0
    while x < len(expr):
        '''Adds first string of numbers into token list'''
        numToken = ""
        validNum = False

        while True and x < len(expr):
            isNum = isNumber(expr[x])
            if isNum:
                numToken += expr[x]
                x += 1
                validNum = True
            else:
                break

        '''White space is ignored'''
        if numToken != whiteSpace and validNum:
            tokens.append(stringToNumber(numToken))

        '''Looks for operators that are non-numbers and validates them'''
        while True and x < len(expr):
            opToken = ""
            isNum = isNumber(expr[x])
            if not isNum:
                opToken += expr[x]
                x += 1
                if opToken not in validOperators and opToken not in parenthesis and opToken != whiteSpace:
                    print("INVALID OPERATOR")
                    exit()
            else:
                break

            '''White space is ignored'''
            if opToken != whiteSpace:
                tokens.append(opToken)

    return tokens

def has_precedence(op1, op2):
    '''Input: two operator tokens, i.e., strings from the set {"+", "-", "*", "/", "∧"}
       Outpt: True if op1 has higher precedence than op2; otherwise False'''
    op1Index = -1
    op2Index = -1

    if  op1 in validOperators and op2 in validOperators:
        for x in range(len(validOperators)):
            if validOperators[x] == op1:
                op1Index = x
            if  validOperators[x] == op2:
                op2Index = x

            if op1Index != -1 and op2Index != -1:
                break

        '''Checks to see which op has higher precedence based on index'''
        if op1Index > op2Index:
            return True
        else:
            return False
    else:
        if op1 == "" or op1 == " ":
            return False
        elif op2 == "" or op2 == " ":
            return True
        else:
            print("INVALID INPUT FOR HAS_PRECEDENCE FUNCTION")
            print(op1, op2)
            exit()

def simple_evalation(tokens):
    '''Input: a list of tokens (excluding parentheses)
       Process: finds op with highest precedence, then does that equation, replace that equation with the answer then
                repeats until only 1 element left
       Output: a float corresponding to the result of the expression'''
    expression = tokens

    while len(expression) > 1:

        '''Goes through the expression checking for  the op with the highest precedence'''
        highestPrecedenceOp = ""
        highestPrecedenceOpIndex = -1

        for x in range (len(expression)):
            if not isNumber(expression[x]):
                if has_precedence(expression[x], highestPrecedenceOp):
                    highestPrecedenceOp = expression[x]
                    highestPrecedenceOpIndex = x

        '''Checks to see whether a single number with no operators has been inputted'''
        if highestPrecedenceOp == "":
            break

        num1 = expression[highestPrecedenceOpIndex - 1]
        num2 = expression[highestPrecedenceOpIndex + 1]

        answer = doOperation(num1, num2, highestPrecedenceOp)

        del expression[highestPrecedenceOpIndex + 1]
        del expression[highestPrecedenceOpIndex]
        del expression[highestPrecedenceOpIndex - 1]

        expression.insert(highestPrecedenceOpIndex - 1, answer)

    return expression

def complex_evaluation(tokens):
    '''Input: a list of tokens (this time including parentheses)
       Output: the single floating point number corresponding to the result of the tokenized arithmetic expression'''
    expression = tokens
    counter = 0
    while len(expression) > 1:
        if containsParenthesis(expression):
            for x in range (len(expression)):
                if  expression[x] == "(":
                    openingIndex = x
                elif expression[x] == ")":
                    closingIndex = x
                    break
            print(expression, expression[openingIndex + 1:closingIndex])
            answer = simple_evalation(expression[openingIndex + 1:closingIndex])

            for x in range(closingIndex, openingIndex - 1, -1):
                del expression[x]

            expression.insert(openingIndex, answer[0])
        else:
            answer = simple_evalation(expression)

    return answer[0]

def evaluation(string):
    expression = tokenization(string)

    answer = complex_evaluation(expression)

    return answer

def driver():
    '''Kick starts the program by asking for user input then calling functions to solve the problem'''
    print("Parsing by Adrian Price")
    print("Type 'exit' to exit")
    while True:
        userExpression = input("Enter a math expression: ")
        if userExpression == "exit":
            print("Program has successfully exited")
            exit()
        else:
            print(userExpression, " = ", evaluation(userExpression))

'''This line must be commented out when using the testing_modules file'''
#driver()