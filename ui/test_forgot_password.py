import re
import pytest
from playwright.sync_api import sync_playwright, expect, Playwright, Page

def test_reset_password_and_enter_username(playwright: Playwright):
   browser = playwright.chromium.launch(headless=True)
   context = browser.new_context()
   page = context.new_page()
   page.goto("https://www.matchbook.com/login")
   page.get_by_role("button", name="Close").click()
   page.get_by_text("Forgot Password?").click()
   page.get_by_text("UsernameReset PasswordCancel").get_by_role("textbox").click()
   page.get_by_text("UsernameReset PasswordCancel").get_by_role("textbox").fill("MANQ625")
   page.get_by_label("Mb Modal").get_by_text("Reset Password").click()
   context.close()
   browser.close()

def test_reset_password_but_cancel(playwright: Playwright):
   browser = playwright.chromium.launch(headless=True)
   context = browser.new_context()
   page = context.new_page()
   page.goto("https://www.matchbook.com/login")
   page.get_by_role("button", name="Close").click()
   page.get_by_text("Forgot Password?").click()
   page.get_by_text("UsernameReset PasswordCancel").get_by_role("textbox").click()
   page.get_by_text("UsernameReset PasswordCancel").get_by_role("textbox").fill("MANQ625")
   page.get_by_label("Mb Modal").get_by_text("Cancel").click()
   context.close()
   browser.close()

