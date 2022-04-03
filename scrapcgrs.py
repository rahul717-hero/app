from playwright.sync_api import Playwright, sync_playwright, expect
import numpy as np
def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    # Open new page
    page = context.new_page()
    # Go to https://ecgrs.dhbvn.org.in/
    page.goto("https://ecgrs.dhbvn.org.in/")
    # Click [placeholder="Username"]
    page.locator("[placeholder=\"Username\"]").click()
    # Fill [placeholder="Username"]
    page.locator("[placeholder=\"Username\"]").fill("h21cgrs")
    # Click [placeholder="Password"]
    page.locator("[placeholder=\"Password\"]").click()
    # Fill [placeholder="Password"]
    page.locator("[placeholder=\"Password\"]").fill("dhbvnl11")
    # Click input:has-text("Login")
    page.locator("input:has-text(\"Login\")").click()
    # expect(page).to_have_url("https://ecgrs.dhbvn.org.in/DashBoard.aspx")
    # Click #dvConfirmBox >> text=Close
    page.locator("#dvConfirmBox >> text=Close").click()
    # Click #txtStartDate
    page.locator("#txtStartDate").click()
    # Select 2016
    page.locator("select").nth(4).select_option("2018")
    # Click .ui-state-default >> nth=0
    page.locator(".ui-state-default").first.click()
    # Click text=Filter Record
    page.locator("text=Filter Record").click()
    page.wait_for_timeout(5000)
    cmpt= page.locator("#tbodyCategoryWiseList").all_inner_texts()
    # save cmpt to file
    np.savetxt("cmlt.csv", 
           cmpt,
           delimiter =", ",
           fmt = "%s")
    
    context.close()
    browser.close()
    # ---------------------
with sync_playwright() as playwright:
    run(playwright)