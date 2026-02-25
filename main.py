import sys

import json

def main():
    # Скрипт может брать путь файла через командную строку
        #   py main.py data/events.json
        #   py main.py data/events.json docs/report.json
    # Если без аргументов, то использует дефолтные пути
    input_path = "data/events.json"
    output_path = "docs/report.json"

    if len(sys.argv) >= 2:
        input_path = sys.argv[1]
    if len(sys.argv) >= 3:
        output_path = sys.argv[2]

    # читаем события
    with open(input_path, "r", encoding="utf-8") as f:
        events = json.load(f)

    # сортируем по времени
    events.sort(key=lambda e: e["date"])

    # считаем кто сейчас активен по каждому компу
    machines = {}  # machine to set(users)

    for e in events:
        machine = e["machine"]
        user = e["user"]
        t = e["type"]

        if machine not in machines:
            machines[machine] = set()

        if t == "login":
            machines[machine].add(user)
        elif t == "logout":
            # discard не вызывает ошибку, если пользователя нет (удобно для неполных логов)
            machines[machine].discard(user)

    # делаем отчёт (чтобы сохранить в json, set to list)
    report = {}
    for machine, users in machines.items():
        report[machine] = sorted(list(users))

    # печать в консоль
    for machine, users in report.items():
        if users:
            print(machine + ": " + ", ".join(users))
        else:
            print(machine + ": (no active users)")

    # сохраняем отчёт
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print("\nSaved report to: ", output_path)
#\n чтоб отчет аккуратнее сделать

if __name__ == "__main__":
    main()