import aiohttp
import asyncio
import json


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


async def fetch_urls(urls: list[str], file_path: str):
    semaphore = asyncio.Semaphore(5)
    results = []

    for url in urls:
        result = await fetch(url, semaphore)
        results.append(result)

    with open(file_path, "w") as file:
        for result in results:
            file.write(json.dumps(result) + "\n")


if __name__ == "__main__":
    urls = [
        "https://example.com",
        "https://httpbin.org/status/404",
        "https://nonexistent.url",
    ]
    asyncio.run(fetch_urls(urls, "./src/module3_task1/results.json"))
