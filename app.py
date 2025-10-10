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

print('\n * solve_task_one:')
solve_task_one()
print('\n * solve_task_two:')
solve_task_two()
