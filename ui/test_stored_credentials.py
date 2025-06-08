import json
import pytest
from playwright.sync_api import sync_playwright, expect

# Load credentials from external JSON file
def load_credentials():
    with open("test_data/users.json") as f:
        return json.load(f)

@pytest.fixture(scope="session")
def credentials():
    return load_credentials()

def test_login(credentials):
    with sync_playwright() as p:
      browser = p.chromium.launch(headless=True)
      context = browser.new_context()
      page = context.new_page()

      # Go to the login page
      page.goto("https://www.matchbook.com/login")
      page.get_by_role("button", name="Close").click()
      page.locator(".mb-login__container-logo").click()
      page.locator("input[name=\"username\"]").click()

      # Fill in login form
      page.locator("input[name=\"username\"]").fill(credentials["username"])
      page.locator("input[name=\"password\"]").click()
      page.locator("input[name=\"password\"]").fill(credentials["password"])
      page.get_by_text("Login", exact=True).click()
      expect(page.get_by_role("button", name="Welcome to Matchbook Deposit")).to_be_visible()
      expect(page.get_by_role("button", name="account Account")).to_be_visible()
      context.close()
      browser.close()