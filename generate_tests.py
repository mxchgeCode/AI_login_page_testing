import os
import requests

API_URL = "https://openrouter.ai/api/v1/chat/completions"
API_KEY = os.getenv("OPENROUTER_API_KEY")


def extract_code_from_response(text: str) -> str:
    """
    Извлекает Python-код из ответа модели.
    Удаляет строки с маркерами кода (``````python).
    """
    lines = text.split('\n')
    cleaned_lines = []
    for line in lines:
        if line.strip() in ('``````python'):
            continue
        cleaned_lines.append(line)
    return '\n'.join(cleaned_lines).strip()


def generate_unit_test_for_code(code: str) -> str:
    prompt = f"""
    You are a Python developer. Generate pytest unit tests for the following code.
    Assume the code resides in the module named 'app'.

    Write ONLY Python code, no explanations or markdown.

    Tests should import necessary functions or classes from 'app' module, e.g.:

    from app import test_login

    Write tests that cover main cases and use mocking where needed.

    Here is the code:

    {code}
    """

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": "deepseek/deepseek-chat-v3.1:free",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0,
        "max_tokens": 2000,
    }

    print("Отправляем запрос в API...")
    response = requests.post(API_URL, headers=headers, json=data)

    print(f"Статус ответа: {response.status_code}")

    if response.status_code != 200:
        print("Текст ошибки:")
        print(response.text)
        response.raise_for_status()

    result = response.json()
    raw_response = result['choices'][0]['message']['content']

    print("=== Сырой ответ модели (первые 300 символов) ===")
    print(raw_response[:300])
    print("=" * 50)

    code_only = extract_code_from_response(raw_response)

    print("=== Извлеченный код (первые 300 символов) ===")
    print(code_only[:300])
    print("=" * 50)

    return code_only


def main():
    source_file = 'app.py'
    output_tests_file = 'test_generated.py'

    if not os.path.isfile(source_file):
        raise FileNotFoundError(f"Файл {source_file} не найден!")

    with open(source_file, 'r', encoding='utf-8') as f:
        raw_code = f.read()

    print("Файл прочитан, генерируем тесты...")

    tests = generate_unit_test_for_code(raw_code)

    # Добавляем импорт функции test_login из app.py в начало сгенерированных тестов,
    # чтобы избежать NameError при вызове test_login() внутри тестов
    import_line = "from app import test_login\n\n"
    tests_with_import = import_line + tests

    try:
        compile(tests_with_import, '<string>', 'exec')
        print("Сгенерированный код валиден")
    except SyntaxError as e:
        print(f"Синтаксическая ошибка в сгенерированном коде: {e}")
        print("Сохраняем как есть...")

    with open(output_tests_file, 'w', encoding='utf-8') as f:
        f.write(tests_with_import)

    print(f"Тесты записаны в {output_tests_file}")


if __name__ == "__main__":
    main()
