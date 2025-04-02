import aiohttp
import asyncio
import json
from aiofiles import open as aio_open


async def fetch(url, semaphore):
    async with semaphore:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    url, timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    return {"url": url, "status": response.status}
        except aiohttp.ClientConnectionError:
            return {"url": url, "status": 0}
        except asyncio.TimeoutError:
            return {"url": url, "status": 0}
        except Exception as e:
            return {"url": url, "status": 0, "error": str(e)}


async def fetch_urls(input_file: str, output_file: str):
    semaphore = asyncio.Semaphore(5)

    async with aio_open(input_file, "r") as file:
        urls = [line.strip() for line in await file.readlines()]

    tasks = [fetch(url, semaphore) for url in urls]
    results = await asyncio.gather(*tasks)

    async with aio_open(output_file, "w") as file:
        for result in results:
            if result:
                await file.write(json.dumps(result) + "\n")


if __name__ == "__main__":
    asyncio.run(
        fetch_urls("./src/module3_task2/urls.txt", "./src/module3_task2/results.jsonl")
    )
