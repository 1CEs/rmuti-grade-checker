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

def get_all_method(driver):
    wait = WebDriverWait(driver, 30)
    side_tab = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_navBar_item_27_cell")))
    side_tab.click()
    sub_side_tab = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_navBar_item_28_cell")))
    sub_side_tab.click()

    sleep(2)

    try:
        table = wait.until(EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolderMain_DLGrade")))
        rows = table.find_elements(By.CSS_SELECTOR, "#ctl00_ContentPlaceHolderMain_DLGrade > tbody > tr")
        latest_row = rows[-1] 
        latest_count = len(rows) - 1

        try:
            header = latest_row.find_element(By.CSS_SELECTOR, "td > table > tbody > tr:first-child")
            semester = header.find_element(By.ID, f"ctl00_ContentPlaceHolderMain_DLGrade_ctl0{latest_count}_lblSemester")
            year = header.find_element(By.ID, f"ctl00_ContentPlaceHolderMain_DLGrade_ctl0{latest_count}_lblYear")
            print(f"\nSemester {semester.text} Year {year.text}")
            
            grade_table = latest_row.find_element(By.CLASS_NAME, "grid")
            grade_rows = grade_table.find_elements(By.TAG_NAME, "tr")[1:]
            
            t = PrettyTable(["Number", "Code", "Name", "Unit", "Grade"])
            for grade_row in grade_rows:
                cols = grade_row.find_elements(By.TAG_NAME, "td")
                if len(cols) >= 5:
                    seq = cols[0].text.strip()
                    code = cols[1].text.strip()
                    name_span = cols[2].find_element(By.CSS_SELECTOR, "span[id*='Label3']")
                    name = name_span.text.strip()
                    credit = cols[3].text.strip()
                    grade = cols[4].text.strip()
                    t.add_row([seq, code, name, credit, grade])
            print(t)
            
            stats_table = latest_row.find_element(By.CSS_SELECTOR, "td > table > tbody > tr:nth-child(3) > td > table")
            stats_rows = stats_table.find_elements(By.TAG_NAME, "tr")
            
            ca = stats_rows[0].find_element(By.ID, f"ctl00_ContentPlaceHolderMain_DLGrade_ctl0{latest_count}_lblCA").text
            gps = stats_rows[0].find_element(By.ID, f"ctl00_ContentPlaceHolderMain_DLGrade_ctl0{latest_count}_lblGPS").text
            cp = stats_rows[0].find_element(By.ID, f"ctl00_ContentPlaceHolderMain_DLGrade_ctl0{latest_count}_lblCP").text
            gpa = stats_rows[1].find_element(By.ID, f"ctl00_ContentPlaceHolderMain_DLGrade_ctl0{latest_count}_lblGPA").text
            
            t_stat = PrettyTable([
                "CA (Registered Units)", 
                "CP (หน่วยกิตสอบผ่าน)",
                "GPS (In-Semester Average Grade)",
                "GPA (Average Grade)"
            ])
            t_stat.add_row([ca, cp, gps, gpa])
            print(t_stat)
            
        except Exception as e:
            print(f"Error processing row: {str(e)}")
                
    except Exception as e:
        print(f"Error accessing grade data: {str(e)}")

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
    print("\tMethods\n#1 Get only grade (Fastest)\n#2 Get all (Latest Semester)")
    print("-" * 30)
    method = get_input("Select (default #1): ")
    year = 0
    if method == 1:
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
            case 2:
                get_all_method(driver)
                
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        driver.quit()