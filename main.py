from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

def get_input(prompt, default=1):
    response = input(prompt)
    return int(response) if response.strip() else default

def action_by_method(method):
    match method:
        case 1 :
            pass
        case 2 :
            pass

if __name__ == "__main__":
    username = input("Username: ")
    password = input("Password: ")
    print("-" * 30)
    print("\tMethods\n#1 Get only grade (Fastest)\n#2 Get all")
    print("-" * 30)
    method = get_input("Select (default #1): ")
    print(method)

    driver = webdriver.Chrome()
    driver.get("https://ess.rmuti.ac.th/RMUTI/Registration/Account/Login.aspx")
    wait = WebDriverWait(driver, 30)
    
    try:
        username_field = wait.until(EC.element_to_be_clickable((By.ID, "Username")))
        username_field.clear()
        username_field.send_keys(username)
        
        password_field = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolderMain_Password")))
        password_field.clear()
        password_field.send_keys(password)
        
        submit_button = wait.until(EC.element_to_be_clickable((By.NAME, "ctl00$ContentPlaceHolderMain$btnLogIn")))
        submit_button.click()

        action_by_method(method=method)
        sleep(2)
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        driver.quit()
        exit(1)