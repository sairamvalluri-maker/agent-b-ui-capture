import asyncio
from playwright.async_api import async_playwright

USER_DATA_DIR = ".playwright-linear-profile"


async def main() -> None:
    async with async_playwright() as p:
        # Persistent context stores cookies/session in USER_DATA_DIR
        context = await p.chromium.launch_persistent_context(
            USER_DATA_DIR,
            headless=False,
        )
        page = await context.new_page()
        await page.goto("https://linear.app/test916/team/TES/active")

        print(
            "\n[login_linear] A browser window opened."
            "\n  1. Log in to Linear completely in that window."
            "\n  2. Make sure you can see your team workspace."
            "\n  3. Then come back here and press ENTER.\n"
        )
        input("Press ENTER here after you finish logging in... ")

        await context.close()


if __name__ == "__main__":
    asyncio.run(main())
