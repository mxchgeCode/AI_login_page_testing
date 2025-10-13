# 6.5 Тип данных defaultdict


def solve_task_one():
    data = [
        ("Books", 1343),
        ("Books", 1166),
        ("Merch", 616),
        ("Courses", 966),
        ("Merch", 1145),
        ("Courses", 1061),
        ("Books", 848),
        ("Courses", 964),
        ("Tutorials", 832),
        ("Merch", 642),
        ("Books", 815),
        ("Tutorials", 1041),
        ("Books", 1218),
        ("Tutorials", 880),
        ("Books", 1003),
        ("Merch", 951),
        ("Books", 920),
        ("Merch", 729),
        ("Tutorials", 977),
        ("Books", 656),
    ]
    # Словарь для накопления прибыли по каждому продукту
    products = {}
    for name, profit in data:
        products[name] = products.get(name, 0) + profit
    for name in sorted(products):
        print(f"{name}: ${products[name]}")


def solve_task_two():
    staff = [
        ("Sales", "Robert Barnes"),
        ("Developing", "Thomas Porter"),
        ("Accounting", "James Wilkins"),
        ("Sales", "Connie Reid"),
        ("Accounting", "Brenda Davis"),
        ("Developing", "Miguel Norris"),
        ("Accounting", "Linda Hudson"),
        ("Developing", "Deborah George"),
        ("Developing", "Nicole Watts"),
        ("Marketing", "Billy Lloyd"),
        ("Sales", "Charlotte Cox"),
        ("Marketing", "Bernice Ramos"),
        ("Sales", "Jose Taylor"),
        ("Sales", "Katie Warner"),
        ("Accounting", "Steven Diaz"),
        ("Accounting", "Kimberly Reynolds"),
        ("Accounting", "John Watts"),
        ("Accounting", "Dale Houston"),
        ("Developing", "Arlene Gibson"),
        ("Marketing", "Joyce Lawrence"),
        ("Accounting", "Rosemary Garcia"),
        ("Marketing", "Ralph Morgan"),
        ("Marketing", "Sam Davis"),
        ("Marketing", "Gail Hill"),
        ("Accounting", "Michelle Wright"),
        ("Accounting", "Casey Jenkins"),
        ("Sales", "Evelyn Martin"),
        ("Accounting", "Aaron Ferguson"),
        ("Marketing", "Andrew Clark"),
        ("Marketing", "John Gonzalez"),
        ("Developing", "Wilma Woods"),
        ("Sales", "Marie Cooper"),
        ("Accounting", "Kay Scott"),
        ("Sales", "Gladys Taylor"),
        ("Accounting", "Ann Bell"),
        ("Accounting", "Craig Wood"),
        ("Accounting", "Gloria Higgins"),
        ("Marketing", "Mario Reynolds"),
        ("Marketing", "Helen Taylor"),
        ("Marketing", "Mary King"),
        ("Accounting", "Jane Jackson"),
        ("Marketing", "Carol Peters"),
        ("Sales", "Alicia Mendoza"),
        ("Accounting", "Edna Cunningham"),
        ("Developing", "Joyce Rivera"),
        ("Sales", "Joseph Lee"),
        ("Sales", "John White"),
        ("Marketing", "Charles Bailey"),
        ("Sales", "Chester Fernandez"),
        ("Sales", "John Washington"),
    ]

    departments = {}

    for dept, person in staff:
        departments[dept] = departments.get(dept, 0) + 1

    for dept in sorted(departments):
        print(f"{dept}: {departments[dept]}")


def solve_task_three():
    staff_broken = [
        ("Developing", "Miguel Norris"),
        ("Sales", "Connie Reid"),
        ("Sales", "Joseph Lee"),
        ("Marketing", "Carol Peters"),
        ("Accounting", "Linda Hudson"),
        ("Accounting", "Ann Bell"),
        ("Marketing", "Ralph Morgan"),
        ("Accounting", "Gloria Higgins"),
        ("Developing", "Wilma Woods"),
        ("Developing", "Wilma Woods"),
        ("Marketing", "Bernice Ramos"),
        ("Marketing", "Joyce Lawrence"),
        ("Accounting", "Craig Wood"),
        ("Developing", "Nicole Watts"),
        ("Sales", "Jose Taylor"),
        ("Accounting", "Linda Hudson"),
        ("Accounting", "Edna Cunningham"),
        ("Sales", "Jose Taylor"),
        ("Marketing", "Helen Taylor"),
        ("Accounting", "Kimberly Reynolds"),
        ("Marketing", "Mary King"),
        ("Sales", "Joseph Lee"),
        ("Accounting", "Gloria Higgins"),
        ("Marketing", "Andrew Clark"),
        ("Accounting", "John Watts"),
        ("Accounting", "Rosemary Garcia"),
        ("Accounting", "Steven Diaz"),
        ("Marketing", "Mary King"),
        ("Sales", "Gladys Taylor"),
        ("Developing", "Thomas Porter"),
        ("Accounting", "Brenda Davis"),
        ("Sales", "Connie Reid"),
        ("Sales", "Alicia Mendoza"),
        ("Marketing", "Mario Reynolds"),
        ("Sales", "John White"),
        ("Developing", "Joyce Rivera"),
        ("Accounting", "Steven Diaz"),
        ("Developing", "Arlene Gibson"),
        ("Sales", "Robert Barnes"),
        ("Sales", "Charlotte Cox"),
        ("Accounting", "Craig Wood"),
        ("Marketing", "Carol Peters"),
        ("Marketing", "Ralph Morgan"),
        ("Accounting", "Kay Scott"),
        ("Sales", "Evelyn Martin"),
        ("Marketing", "Billy Lloyd"),
        ("Sales", "Gladys Taylor"),
        ("Developing", "Deborah George"),
        ("Sales", "Charlotte Cox"),
        ("Marketing", "Sam Davis"),
        ("Sales", "John White"),
        ("Sales", "Marie Cooper"),
        ("Marketing", "John Gonzalez"),
        ("Sales", "John Washington"),
        ("Sales", "Chester Fernandez"),
        ("Sales", "Alicia Mendoza"),
        ("Sales", "Katie Warner"),
        ("Accounting", "Jane Jackson"),
        ("Sales", "Chester Fernandez"),
        ("Marketing", "Charles Bailey"),
        ("Marketing", "Gail Hill"),
        ("Accounting", "Casey Jenkins"),
        ("Accounting", "James Wilkins"),
        ("Accounting", "Casey Jenkins"),
        ("Marketing", "Mario Reynolds"),
        ("Accounting", "Aaron Ferguson"),
        ("Accounting", "Kimberly Reynolds"),
        ("Sales", "Robert Barnes"),
        ("Accounting", "Aaron Ferguson"),
        ("Accounting", "Jane Jackson"),
        ("Developing", "Deborah George"),
        ("Accounting", "Michelle Wright"),
        ("Accounting", "Dale Houston"),
    ]

    departments = {}

    for dept, person in staff_broken:
        departments.setdefault(dept, set()).add(person)

    for dept in sorted(departments):
        sorted_employees = sorted(departments[dept])
        print(f"{dept}: {', '.join(sorted_employees)}")


def solve_task_four():
    pairs = [("Тимур", "Артур"), ("Тимур", "Дима"), ("Дима", "Артур")]
    result = {}
    for winner, loser in pairs:
        result.setdefault(winner, set()).add(loser)
    for winner, losers in sorted(result.items()):
        print(winner, "->", *sorted(losers))


import random


def solve_ternary_operator():
    a = random.uniform(0, 100)
    b = random.uniform(0, 100)
    d = a if a > b else b
    print(d)


print("\n * solve_task_one:")
solve_task_one()
print("\n * solve_task_two:")
solve_task_two()
print("\n * solve_task_three:")
solve_task_three()
print("\n * solve_task_four:")
solve_task_four()
print("\n * solve_ternar_operator:")
solve_ternary_operator()
