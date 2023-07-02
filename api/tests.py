quiz = [
    {
        "title": "What is the correct way to declare a variable in Python?",
        "variants": [
            "var x = 5",
            "x = 5",
            "int x = 5",
            "x = int(5)"
        ],
        "correct": 1
    },
    {
        "title": "Which of the following variable names is valid in Python?",
        "variants": [
            "my_var",
            "my-var",
            "my var",
            "_myvar"
        ],
        "correct": 0
    },
    {
        "title": "What is the scope of a global variable in Python?",
        "variants": [
            "It can only be accessed within the function where it is declared",
            "It can be accessed from anywhere in the program",
            "It can only be accessed from the module where it is declared",
            "It can be accessed from any module in the program"
        ],
        "correct": 3
    },
    {
        "title": "What is the correct way to assign multiple variables in a single line in Python?",
        "variants": [
            "x, y = 1, 2",
            "x = y = 1, 2",
            "x, y := 1, 2",
            "x = 1, y = 2"
        ],
        "correct": 0
    },
    {
        "title": "Which of the following is NOT a valid Python variable type?",
        "variants": [
            "int",
            "float",
            "string",
            "var"
        ],
        "correct": 3
    },
    {
        "title": "What is the correct way to declare a constant variable in Python?",
        "variants": [
            "const PI = 3.14",
            "PI = 3.14",
            "constant PI = 3.14",
            "PI := 3.14"
        ],
        "correct": 1
    },
    {
        "title": "What is the result of the following code? \n\nx = 5 \nprint(type(x))",
        "variants": [
            "int",
            "float",
            "string",
            "bool"
        ],
        "correct": 0
    },
    {
        "title": "What is the correct way to concatenate two strings in Python?",
        "variants": [
            "string1 + string2",
            "string1 - string2",
            "string1 * string2",
            "string1 / string2"
        ],
        "correct": 0
    },
    {
        "title": "What is the output of the following code? \n\nx = 5 \nprint(type(x))",
        "variants": [
            "<class 'int'>",
            "<class 'float'>",
            "<class 'string'>",
            "<class 'bool'>"
        ],
        "correct": 0
    },
    {
        "title": "What is the correct way to convert a string to an integer in Python?",
        "variants": [
            "int(string)",
            "string.toInt()",
            "convert(string, int)",
            "int.convert(string)"
        ],
        "correct": 0
    },
    {
        "title": "What is the result of the following code? \n\nx = 5 \nprint(x * 2)",
        "variants": [
            "10",
            "7",
            "25",
            "0"
        ],
        "correct": 0
    },
    {
        "title": "What is the correct way to declare a floating-point variable in Python?",
        "variants": [
            "x = 5.0",
            "float x = 5",
            "x = 5",
            "x = float(5)"
        ],
        "correct": 0
    },
    {
        "title": "Which of the following is a valid Python identifier?",
        "variants": [
            "my-variable",
            "_myvar",
            "2myvar",
            "myvar@"
        ],
        "correct": 1
    },
    {
        "title": "What is the result of the following code? \n\nx = 5 \nprint(x + '2')",
        "variants": [
            "7",
            "52",
            "57",
            "Error: cannot concatenate 'str' and 'int' objects"
        ],
        "correct": 3
    },
    {
        "title": "What is the correct way to assign a value to a variable in Python?",
        "variants": [
            "x == 5",
            "x = 5",
            "5 = x",
            "= 5 x"
        ],
        "correct": 1
    }
]

for i in quiz:
    print(i["title"])