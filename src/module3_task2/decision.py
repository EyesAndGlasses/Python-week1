import aiohttp
import asyncio
import json
import os
from aiofiles import open as aio_open


async def fetch(
    queue: asyncio.Queue,
    semaphore: asyncio.Semaphore,
    session: aiohttp.ClientSession,
    results: list,
):
    while True:
        url = await queue.get()
        if url is None:
            break

        async with semaphore:
            try:
                async with session.get(
                    url, timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    results.append({"url": url, "status": response.status})
            except (aiohttp.ClientConnectionError, asyncio.TimeoutError):
                results.append({"url": url, "status": 0})
            except Exception as e:
                results.append({"url": url, "status": 0, "error": str(e)})

        queue.task_done()


async def fetch_urls(input_file: str, output_file: str):
    num_workers = 5
    queue = asyncio.Queue()
    results = []
    semaphore = asyncio.Semaphore(num_workers)

    async with aio_open(input_file, "r") as file:
        urls = [line.strip() for line in await file.readlines()]

    for url in urls:
        await queue.put(url)

    async with aiohttp.ClientSession() as session:
        workers = [
            asyncio.create_task(fetch(queue, semaphore, session, results))
            for _ in range(num_workers)
        ]

        await queue.join()

        for _ in range(num_workers):
            await queue.put(None)
        await asyncio.gather(*workers)

    async with aio_open(output_file, "w") as file:
        for result in results:
            await file.write(json.dumps(result) + "\n")


if __name__ == "__main__":
    asyncio.run(
        fetch_urls("./src/module3_task2/urls.txt", "./src/module3_task2/results.jsonl")
    )
