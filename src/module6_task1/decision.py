import json
import aiohttp
from datetime import datetime
from aiohttp import web


async def fetch_exchange_rate(currency: str):
    url = f"https://api.exchangerate-api.com/v4/latest/{currency}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                return None


async def handle(request):
    currency = request.match_info.get("currency", "USD").upper()
    data = await fetch_exchange_rate(currency)

    if data:
        return web.Response(text=json.dumps(data), content_type="application/json")
    else:
        return web.Response(
            text=json.dumps({"error": "Unable to fetch exchange rates"}),
            content_type="application/json",
            status=500,
        )


app = web.Application()
app.router.add_get("/{currency}", handle)

if __name__ == "__main__":
    web.run_app(app, host="localhost", port=8000)
