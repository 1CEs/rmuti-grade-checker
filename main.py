from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from prettytable import PrettyTable
from time import sleep

def get_input(prompt, default=1):
    response = input(prompt)
    return int(response) if response.strip() else default

def scrape_table_data(driver, semester_id):
    try:
        wait = WebDriverWait(driver, 30)
        table = wait.until(EC.presence_of_element_located((By.ID, semester_id)))
        
        rows = table.find_elements(By.TAG_NAME, "tr")[2:-1]
        
        t = PrettyTable(["type", "name", "grade"])
        for row in rows:
            try:
                cols = row.find_elements(By.TAG_NAME, "td")
                if len(cols) >= 9:
                    course_type = cols[0].text.strip()
                    course_code = cols[1].text.strip()
                    grade = cols[2].text.strip()
                    if grade:
                        t.add_row([course_type, course_code, grade])
                    else:
                        t.add_row([course_type, course_code, "ไม่ทราบผล"])
            except Exception as e:
                continue
        print(t)
    except Exception as e:
        print(f"Error accessing {semester_id}: {str(e)}")

def get_only_grade_method(driver, year):
    year_tabs_id = [
        "ctl00_ContentPlaceHolderMain_tabsYear1",
        "ctl00_ContentPlaceHolderMain_tabsYear2",
        "ctl00_ContentPlaceHolderMain_tabsYear3",
        "ctl00_ContentPlaceHolderMain_tabsYear4"
    ]
    wait = WebDriverWait(driver, 30)
    side_tab = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_navBar_item_7_cell")))
    side_tab.click()
    sub_side_tab = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_navBar_item_11_cell")))
    sub_side_tab.click()
    year_tab = wait.until(EC.element_to_be_clickable((By.ID, year_tabs_id[year - 1])))
    year_tab.click()

    sleep(2)
    print("First Semester: ")
    scrape_table_data(driver, "ctl00_ContentPlaceHolderMain_dgFirstSemester")
    
    sleep(2)
    print("\nSecond Semester: ")
    scrape_table_data(driver, "ctl00_ContentPlaceHolderMain_dgSecondSemester")

    sleep(2)
    print("\nSummer Semester: ")
    scrape_table_data(driver, "ctl00_ContentPlaceHolderMain_dgSummerSemester")

if __name__ == "__main__":
    username = input("Username: ")
    password = input("Password: ")
    print("-" * 30)
    print("\tMethods\n#1 Get only grade (Fastest)\n#2 Get all")
    print("-" * 30)
    method = get_input("Select (default #1): ")
    year = int(input("Year: "))

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--ignore-ssl-errors")
    options.add_argument("--allow-insecure-localhost")
    options.add_argument("--disable-web-security")
    options.add_argument("--reduce-security-for-testing")
    
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option('useAutomationExtension', False)
    
    driver = webdriver.Edge(options=options)
    driver.set_page_load_timeout(30)
    
    try:
        driver.get("https://ess.rmuti.ac.th/RMUTI/Registration/Account/Login.aspx")
        wait = WebDriverWait(driver, 30)
        
        username_field = wait.until(EC.element_to_be_clickable((By.ID, "Username")))
        username_field.clear()
        username_field.send_keys(username)
        
        password_field = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolderMain_Password")))
        password_field.clear()
        password_field.send_keys(password)
        
        submit_button = wait.until(EC.element_to_be_clickable((By.NAME, "ctl00$ContentPlaceHolderMain$btnLogIn")))
        submit_button.click()

        match method:
            case 1:
                get_only_grade_method(driver, year)
                
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        driver.quit()