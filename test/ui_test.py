import re
import time
from playwright.sync_api import Playwright, sync_playwright, expect

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.nytimes.com/games/wordle/index.html")
    page.get_by_test_id("Play").click()
    page.get_by_role("button", name="Close").click()
    page.get_by_role("button", name="add s").click()
    page.get_by_role("button", name="add l").click()
    page.get_by_role("button", name="add a").click()
    page.get_by_role("button", name="add t").click()
    page.get_by_role("button", name="add e").click()
    page.get_by_role("button", name="enter").click()
    time.sleep(3)
    page.get_by_role("button", name="add r").click()
    page.get_by_role("button", name="add i").click()
    page.get_by_role("button", name="add g").click()
    page.get_by_role("button", name="add i").click()
    page.get_by_role("button", name="add d").click()
    page.get_by_role("button", name="enter").click()
    page.get_by_test_id("login-container").locator("div").nth(2).click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
