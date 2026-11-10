import urllib.request
import json
from playwright.sync_api import sync_playwright

# 1. THE ALERT FUNCTION (Your new secret weapon)
def send_webhook_alert(message):
    webhook_url = "https://webhook.site/62529e72-818f-411c-8327-4ea73be2a6d7"
    
    data = {"text": message}
    req = urllib.request.Request(
        webhook_url,
        data=json.dumps(data).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    try:
        urllib.request.urlopen(req)
        print("✅ Alert successfully sent to Webhook.site!")
    except Exception as e:
        print(f"❌ Failed to send alert: {e}")

def run_test():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://www.saucedemo.com/")
        
        page.fill("#user-name", "standard_user")
        page.fill("#password", "wrong_password") # Keeping it broken to test the alarm!
        page.click("#login-button")
        
        # 2. THE TRAP: Try to verify login, catch the error if it fails
        try:
            assert "inventory.html" in page.url
            print("✅ Login Successful!")
        except AssertionError:
            # 3. THE ALARM: This runs ONLY if the website is broken
            print("❌ LOGIN FAILED! The website is broken!")
            send_webhook_alert("🚨 URGENT BOSS: The login page is BROKEN! Customers cannot log in! Fix it now!")
        
        browser.close()
        print("🎉 Bot finished its check.")

if __name__ == "__main__":
    run_test()