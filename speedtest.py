#!/usr/bin/env python3
"""Замер скорости скачивания: 10 запросов подряд к одному адресу."""

import sys
import time
import urllib.request

REQUESTS = 10
TIMEOUT = 30


def fetch(url):
    """Качает url целиком, возвращает (время в секундах, размер в байтах)."""
    start = time.perf_counter()
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        data = resp.read()
    return time.perf_counter() - start, len(data)


def main():
    if len(sys.argv) != 2:
        print("Запуск: python speedtest.py <адрес файла>")
        print("Пример: python speedtest.py https://speed.hetzner.de/100MB.bin")
        sys.exit(1)

    url = sys.argv[1]
    times = []
    total_bytes = 0

    for i in range(1, REQUESTS + 1):
        try:
            sec, size = fetch(url)
        except Exception as e:
            print(f"Запрос {i}: не удалось — {e}")
            sys.exit(2)
        times.append(sec)
        total_bytes += size
        print(f"Запрос {i:>2}: {sec:.2f} с, {size / 1024 / 1024:.2f} МБ")

    avg_time = sum(times) / len(times)
    total_mb = total_bytes / 1024 / 1024
    speed = total_mb / sum(times)

    print()
    print(f"Среднее время запроса: {avg_time:.2f} с")
    print(f"Всего скачано: {total_mb:.2f} МБ")
    print(f"Средняя скорость скачивания: {speed:.2f} МБ/с ({speed * 8:.1f} Мбит/с)")


if __name__ == "__main__":
    main()
