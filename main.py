import sys

import json

from datetime import datetime
now = datetime.now()

def main():
    # Скрипт может брать путь файла через командную строку
        # py main.py data/events.json
        # py main.py data/events.json docs/report.json
    # Если без аргументов, то использует дефолтные пути
    input_path = "data/events.json"
    output_path = "docs/report.json"

    if len(sys.argv) >= 2:
        input_path = sys.argv[1]
    if len(sys.argv) >= 3:
        output_path = sys.argv[2]

    # читаем события
    with open(input_path, "r", encoding="utf-8") as file:
        events = json.load(file)

    # сортируем по времени
    events.sort(key=lambda event: event["date"])
    
    # репорт количества за компом времени и когда
    login_time = {}      # (machine, user) to datetime of login
    total_seconds = {}   # (machine, user) to total seconds online

    for event in events:
        machine = event["machine"]
        user = event["user"]
        ty = event["type"]
        event_time = datetime.fromisoformat(event["date"])

        key = (machine, user)

        if ty == "login":
            login_time[key] = event_time
        elif ty == "logout":
            if key in login_time:
                duration = (event_time - login_time[key]).total_seconds()
                total_seconds[key] = total_seconds.get(key, 0) + duration
                del login_time[key]

    print("\nSession duration report (minutes):")

    # завершенные сессии
    for (machine, user), seconds in total_seconds.items():
        minutes = round(seconds / 60, 1)
        print(f"{machine} | {user}: {minutes} min (completed)")

    # активные сейчас
    for (machine, user), login_dt in login_time.items():
        seconds = (now - login_dt).total_seconds()
        minutes = round(seconds / 60, 1)
        print(f"{machine} | {user}: {minutes} min (active now, since {login_dt})")
    
    # считаем кто сейчас активен по каждому компу
    machines = {}  # machine to set(users)

    for event in events:

        machine = event["machine"]
        user = event["user"]
        ty = event["type"]

        if machine not in machines:
            machines[machine] = set()

        if ty == "login":
            machines[machine].add(user)
        elif ty == "logout":
            # discard не вызывает ошибку, если пользователя нет (удобно для неполных логов)
            machines[machine].discard(user)

    # делаем отчёт (чтобы сохранить в json, set to list)
    report = {}
    for machine, users in machines.items():
        report[machine] = sorted(list(users))

    # сохраняем отчёт
    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(report, file, ensure_ascii=False, indent=2)

    print("\nSaved report to:", output_path)
#\n чтоб отчет аккуратнее сделать

if __name__ == "__main__":
    main()