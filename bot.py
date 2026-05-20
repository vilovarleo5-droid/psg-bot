import asyncio
import requests
from playwright.async_api import async_playwright

DISCORD_WEBHOOK = "COLLE TON LIEN ICI"

URL = "https://billetterie.psg.fr/fr/ticketplace"

seen = set()

def send(msg):
    requests.post(DISCORD_WEBHOOK, json={"content": msg})

async def main():

    async with async_playwright() as p:

        browser = await p.chromium.launch(headless=True)

        while True:

            page = await browser.new_page()

            await page.goto(URL)

            await page.wait_for_timeout(5000)

            text = await page.inner_text("body")

            if "auteuil" in text.lower() and "1 place" in text.lower():

                key = hash(text)

                if key not in seen:

                    seen.add(key)

                    send("🚨 PLACE AUTEUIL DISPONIBLE !")

            await page.close()

            await asyncio.sleep(20)

asyncio.run(main())