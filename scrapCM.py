
from playwright.sync_api import Playwright, sync_playwright, expect
import cv2 as cv
import numpy as np
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
def run(playwright: Playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    # Open new page
    page = context.new_page()
    # Go to https://cmharyanacell.nic.in/index
    page.goto("https://cmharyanacell.nic.in/index")
    # Click [placeholder="Userid"]
    page.locator("[placeholder=\"Userid\"]").click()
    # Fill [placeholder="Userid"]
    page.locator("[placeholder=\"Userid\"]").fill("sat11")
    # Click [placeholder="Password"]
    page.locator("[placeholder=\"Password\"]").click()
    # Fill [placeholder="Password"]
    page.locator("[placeholder=\"Password\"]").fill("sat11")
    # Click text=उपयोगकर्ता पहचान / User ID पासवर्ड / Password केप्चा भरे / Enter Captcha >> [placeholder="Captcha"]
    page.locator("text=उपयोगकर्ता पहचान / User ID पासवर्ड / Password केप्चा भरे / Enter Captcha >> [placeholder=\"Captcha\"]").click()
    # take screemshot of captcha image
    page.wait_for_timeout(1000)
    page.locator("text=उपयोगकर्ता पहचान / User ID पासवर्ड / Password केप्चा भरे / Enter Captcha >> #imgCaptcha").screenshot(path='cptch.png')
    srcImage = cv.imread('cptch.png')
    ret, threshImage = cv.threshold(srcImage,100,200, cv.THRESH_BINARY_INV)
    cv.bitwise_not(threshImage, threshImage)
    test_message = Image.fromarray(threshImage)
    text = pytesseract.image_to_string(test_message,config="-c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
    



    
    page.locator("text=उपयोगकर्ता पहचान / User ID पासवर्ड / Password केप्चा भरे / Enter Captcha >> [placeholder=\"Captcha\"]").fill(text)
    # Click text=Login / लॉग इन करें
    page.locator("text=Login / लॉग इन करें").click()
    try:
        expect(page).to_have_url("https://cmharyanacell.nic.in/office/activegriev.php")
        page.locator("text=Close").click()
        # GET PARAGRAPH TEXT IN DIV having text "in action"
        d=page.locator('div.adata').all_text_contents()
        d=np.array(d)
        #save d as text file
        np.savetxt("cmpt.csv", 
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
    



    






















