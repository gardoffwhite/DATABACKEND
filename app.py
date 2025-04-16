from flask import Flask, request, render_template
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)

# Function to update character stats using Selenium
def update_character(char_name, lv, exp, str_stat, dex_stat, int_stat, money):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode (without opening a browser window)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # Step 1: Login as admin
    driver.get("http://nage-warzone.com/admin/index.php")
    driver.find_element(By.NAME, "username").send_keys("admin")
    driver.find_element(By.NAME, "password").send_keys("3770")
    driver.find_element(By.NAME, "login").click()

    # Step 2: Navigate to character editor
    driver.get(f"http://nage-warzone.com/admin/charedit.php?charname={char_name}")

    # Step 3: Update character stats
    driver.find_element(By.NAME, "lv").clear()
    driver.find_element(By.NAME, "lv").send_keys(str(lv))
    
    driver.find_element(By.NAME, "exp").clear()
    driver.find_element(By.NAME, "exp").send_keys(str(exp))
    
    driver.find_element(By.NAME, "str").clear()
    driver.find_element(By.NAME, "str").send_keys(str(str_stat))
    
    driver.find_element(By.NAME, "dex").clear()
    driver.find_element(By.NAME, "dex").send_keys(str(dex_stat))
    
    driver.find_element(By.NAME, "int").clear()
    driver.find_element(By.NAME, "int").send_keys(str(int_stat))
    
    driver.find_element(By.NAME, "money").clear()
    driver.find_element(By.NAME, "money").send_keys(str(money))
    
    # Step 4: Submit the form to update the character
    driver.find_element(By.NAME, "update").click()

    # Wait for a moment to ensure the update is processed
    driver.implicitly_wait(3)  # Adjust the waiting time as needed

    # Step 5: Optionally, verify the update
    updated_lv = driver.find_element(By.NAME, "lv").get_attribute("value")
    updated_exp = driver.find_element(By.NAME, "exp").get_attribute("value")

    driver.quit()
    return updated_lv, updated_exp

@app.route('/')
def home():
    return render_template("index.html")  # Assuming you have a simple form in index.html

@app.route('/update_character', methods=['POST'])
def update_character_stats():
    char_name = request.form['char_name']
    lv = int(request.form['lv'])
    exp = int(request.form['exp'])
    str_stat = int(request.form['str_stat'])
    dex_stat = int(request.form['dex_stat'])
    int_stat = int(request.form['int_stat'])
    money = int(request.form['money'])
    
    updated_lv, updated_exp = update_character(char_name, lv, exp, str_stat, dex_stat, int_stat, money)
    
    return f"Character {char_name} updated: Lv = {updated_lv}, EXP = {updated_exp}"

if __name__ == '__main__':
    app.run(debug=True)
if __name__ == "__main__":
    # ระบุพอร์ตที่ต้องการใช้
    app.run(host="0.0.0.0", port=port)
