import re
import pytest
from playwright.sync_api import sync_playwright, expect, Playwright, Page

def test_just_store_cookie_preferences(playwright: Playwright):
   browser = playwright.chromium.launch(headless=True)
   context = browser.new_context()
   page = context.new_page() 
   page.goto("https://www.matchbook.com/")
   page.get_by_role("button", name="Allow Strictly Necessary").click()
   page.get_by_role("button").filter(has_text="CLOSE").click()
   expect(page.get_by_role("link", name="Log In")).to_be_visible()
   page.get_by_role("link", name="Log In").click()
   expect(page.locator("div").filter(has_text=re.compile(r"^UsernamePasswordLoginForgot Password\?$")).first).to_be_visible()
   expect(page.locator("input[name=\"username\"]")).to_be_visible()
   page.locator("input[name=\"username\"]").press("ControlOrMeta+c")
   # Save storage state
   context.storage_state(path="cookie_state.json")
   print("Cookie preferences saved to cookie_state.json")
   context.close()
   page.close()

def test_a_login(playwright: Playwright):
   browser = playwright.chromium.launch(headless=True)
   context = browser.new_context()
   page = context.new_page()   
   page.goto("https://www.matchbook.com/")
   page.get_by_role("button", name="Allow Strictly Necessary").click()
   page.get_by_role("button").filter(has_text="CLOSE").click()
   expect(page.get_by_role("link", name="Log In")).to_be_visible()
   page.get_by_role("link", name="Log In").click()
   expect(page.locator("div").filter(has_text=re.compile(r"^UsernamePasswordLoginForgot Password\?$")).first).to_be_visible()
   expect(page.locator("input[name=\"username\"]")).to_be_visible()
   page.locator("input[name=\"username\"]").press("ControlOrMeta+c")
   page.locator("input[name=\"username\"]").fill("MANQ625")
   page.locator("input[name=\"password\"]").fill("c961g8Iy")
   page.get_by_text("Login", exact=True).click()
   expect(page.get_by_role("button", name="Welcome to Matchbook Deposit")).to_be_visible()
   expect(page.get_by_role("button", name="account Account")).to_be_visible()
   # Save storage state
   context.storage_state(path="logged_in.json")
   print("Login state saved to logged_in.json")
   context.close()
   page.close()

def test_navigates_to_login_page(playwright: Playwright):
   page = cookies_accepted_browser(playwright)
   response = page.request.get('https://matchbook.com/login')
   expect(response).to_be_ok()
   page.close()

def test_stored_loggedin_state(playwright: Playwright):
   page = logged_in_browser(playwright)
   page.goto("https://www.matchbook.com/account/general-settings")  
   expect(page.get_by_role("heading", name="Settings", exact=True)).to_be_visible()
   # Verify login state - my settings should be visible
   if page.get_by_role("heading", name="Settings", exact=True).is_visible():
      print("Logged in.")
   else:
      print("Not logged in.")
   page.close()

def test_incorrect_login(playwright: Playwright):
   page = cookies_accepted_browser(playwright)
   response = page.request.get('https://matchbook.com/login')
   expect(response).to_be_ok()
   page.goto("https://www.matchbook.com/account/login")  
   page.locator("input[name=\"username\"]").fill("MANQ625")
   page.locator("input[name=\"password\"]").fill("sfsdfsdf")
   page.get_by_text("Login", exact=True).click()
   expect(page.get_by_text("Incorrect credentials. Please")).to_be_visible()
   expect(page.locator("form")).to_contain_text("Incorrect credentials. Please try again or reset your password.")
   expect(page.get_by_text("Incorrect credentials. Please")).to_be_visible()
   expect(response).to_be_ok()
   page.close()

def test_login_no_username(playwright: Playwright):
   page = cookies_accepted_browser(playwright)
   response = page.request.get('https://matchbook.com/login')
   expect(response).to_be_ok()
   page.goto("https://www.matchbook.com/account/login")  
   page.locator("input[name=\"password\"]").fill("sfsdfsdf")
   page.get_by_text("Login", exact=True).click()
   expect(page.get_by_text("Username cannot be blank. Username must be set to login.")).to_be_visible()
   expect(page.locator("form")).to_contain_text("Username cannot be blank. Username must be set to login.")
   page.close()

def test_login_no_password(playwright: Playwright):
   page = cookies_accepted_browser(playwright)
   response = page.request.get('https://matchbook.com/login')
   expect(response).to_be_ok()
   page.goto("https://matchbook.com/login")
   page.locator("input[name=\"username\"]").fill("MANQ625")
   page.get_by_text("Login", exact=True).click()
   expect(page.get_by_text("Password cannot be blank. Password must be set to login.")).to_be_visible()
   page.close()

def cookies_accepted_browser(playwright: Playwright):
   browser = playwright.chromium.launch(headless=True)
   # Load the saved cookie state to by pass popups and just test incorrect logins
   context = browser.new_context(storage_state="cookie_state.json")
   page = context.new_page()
   return page

def logged_in_browser(playwright: Playwright):
   browser = playwright.chromium.launch(headless=True)
   context = browser.new_context(storage_state="logged_in.json")
   page = context.new_page()
   return page

