import json
import math
import random
import time
from concurrent.futures import ThreadPoolExecutor
import multiprocessing


def generate_data(n):
    return [random.randint(1, 1000) for _ in range(n)]


def is_prime(number):
    if number < 2:
        return False
    for i in range(2, int(math.sqrt(number)) + 1):
        if number % i == 0:
            return False
    return True


def process_number(data):
    primes = [num for num in data if is_prime(num)]

    return primes


def process_numberA(data):
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(is_prime, data))

    primes = [num for num, prime in zip(data, results) if prime]
    return primes


def process_numberB(data):
    cpu_count = multiprocessing.cpu_count()
    with multiprocessing.Pool(cpu_count) as pool:
        results = pool.map(is_prime, data)

    primes = [num for num, prime in zip(data, results) if prime]
    return primes


def worker(task_queue, result_queue):
    while True:
        number = task_queue.get()
        if number is None:
            break
        result_queue.put((number, is_prime(number)))


def process_numberC(data):
    num_workers = multiprocessing.cpu_count()
    task_queue = multiprocessing.Queue()
    result_queue = multiprocessing.Queue()

    processes = [
        multiprocessing.Process(target=worker, args=(task_queue, result_queue))
        for _ in range(num_workers)
    ]
    for p in processes:
        p.start()

    for number in data:
        task_queue.put(number)

    for _ in processes:
        task_queue.put(None)

    primes = []
    for _ in range(len(data)):
        num, is_prime_result = result_queue.get()
        if is_prime_result:
            primes.append(num)

    for p in processes:
        p.join()

    return primes


def main(n, output_file):
    data = generate_data(n)

    start_time = time.time()
    primes = process_number(data)
    processing_time = time.time() - start_time

    start_time = time.time()
    primesA = process_numberA(data)
    processing_timeA = time.time() - start_time

    start_time = time.time()
    primesB = process_numberB(data)
    processing_timeB = time.time() - start_time

    start_time = time.time()
    primesC = process_numberC(data)
    processing_timeA = time.time() - start_time
    # Итоговый результат
    result = {
        "one_stream": processing_time,
        "multy_stream": processing_timeA,
        "multy_process": processing_timeB,
    }

    # Сохранение в JSON
    with open(output_file, "w") as f:
        json.dump(result, f, indent=4)


if __name__ == "__main__":
    main(1000000, "./src/module4_task1/result.json")
