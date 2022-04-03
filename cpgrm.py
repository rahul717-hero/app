from playwright.sync_api import Playwright, sync_playwright, expect
import cv2 as cv
import numpy as np
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
from playwright.sync_api import Playwright, sync_playwright, expect
def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    # Open new page
    page = context.new_page()
    # Go to https://pgportal.gov.in/CPGOFFICE/
    page.goto("https://pgportal.gov.in/CPGOFFICE/")
    # Click [placeholder="Username"]
    page.locator("[placeholder=\"Username\"]").click()
    page.locator("[placeholder=\"Username\"]").fill("Bvngr")
    # Click [placeholder="Password"]
    page.locator("[placeholder=\"Password\"]").click()
    page.locator("[placeholder=\"Password\"]").fill("India123")

    page.locator("img[alt=\"Captcha\"]").screenshot(path='cptch.png')
    def recognize_text(image):
        #  edge preserving filter denoising 
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        #  binarization 
        ret, binary = cv.threshold(gray,200, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)
        #  morphological manipulation corrosion    expansion 
        erode = cv.erode(binary, None, iterations=1)
        dilate = cv.dilate(erode, None, iterations=1)
        #  logical operation makes the background white    the font is black for easy recognition. 
        cv.bitwise_not(dilate, dilate)
        #  identify 
        test_message = Image.fromarray(dilate)
        text = pytesseract.image_to_string(test_message,config="-c tessedit_char_whitelist=0123456789")
        return text


    src = cv.imread('cptch.png')
    text=recognize_text(src)


    # Click [placeholder="Security Code"]
    page.locator("[placeholder=\"Security Code\"]").click()
    # Fill [placeholder="Security Code"]
    page.locator("[placeholder=\"Security Code\"]").fill(text)



    # Click button:has-text("Login")
    page.locator("button:has-text(\"Login\")").click()
    # Click text=Grievances Under Process

    try:
        
        expect(page).to_have_url("https://pgportal.gov.in/CPGOFFICE/OperationalDesk")
        page.locator("text=Grievances Under Process").click()
        # Click section:has-text("0 At Our Office View list of grievance(s) 0 With Subordinate View list of grieva")
        page.wait_for_timeout(5000)
        d=page.locator("//section[contains(@class,'content-small')]").all_inner_texts()
        # Click a:has-text("My Account")
        page.locator("a:has-text(\"My Account\")").click()
        # Click text=Sign out
        page.locator("text=Sign out").click()
        #save d as text file
        np.savetxt("cpgm.csv", 
            d,
            delimiter =", ",
            fmt="%s")
    

        context.close()
        browser.close()
        return 0
    except Exception as e:
        context.close()
        browser.close()
        return 1
        

with sync_playwright() as playwright:
    x=1
    count=0
    while x:
        x=run(playwright)
        count+=1
        if count > 10:
            break

