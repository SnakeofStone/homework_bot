import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

def get_hw(usr: str, pwd: str, url: str) -> str:
    """
    Return a string of the current homework assignments that need to be delivered
    in the upcoming days.

    Args:
        driver  --- Instance of a selenium webdriver for Google Chrome
        usr     --- Username used to login to campus.uag.mx
        pwd     --- Password used to login to campus.uag.mx
    """
    DELAY = 45

    #opts = webdriver.ChromeOptions()
    #opts.add_argument('headless')
    #driver = webdriver.Chrome(options=opts)
    driver = webdriver.Chrome()

    driver.get(url)

    assert "Campus Digital" in driver.title

    try:
        user, password = driver.find_element_by_name("usuario"), \
                         driver.find_element_by_name("password")
    except NoSuchElementException:
        print("Input form not found")
        driver.close()

    user.clear()
    user.send_keys(usr)

    password.clear()
    password.send_keys(pwd)
    password.send_keys(Keys.RETURN)

    try:
        btn = WebDriverWait(driver, DELAY).until(\
            EC.presence_of_element_located((By.ID, 'btn-sistemas')))
        btn.click()
    except TimeoutException:
        print("Timeout while trying to find the 'Botón sistemas' element")
        driver.close()
        exit(-1)

    try:
        a = WebDriverWait(driver, DELAY).until(\
            EC.presence_of_element_located((\
            By.XPATH, "//a[@title='Mis Cursos CU']")))
    except TimeoutException:
        print("Timeout while trying to find the 'Mis Cursos CU' element")
        driver.close()
        exit(-1)

    driver.get(a.get_attribute("href"))

    assert "Tablero" in driver.title

    try:
        table = WebDriverWait(driver, DELAY).until(
                EC.presence_of_element_located((By.XPATH, "//div[@data-region=\
                'timeline-view-dates']//div[@class='border-0 pb-2']")))
    except TimeoutException:
        print("Timeout while trying to find the 'Timeline' table element")
        driver.close()
        exit(-1)
    except NoSuchElementException:
        print("No such element 'Línea de tiempo' specified in the script")
        driver.close()
        exit(-1)

    hws = table.text

    driver.close()

    return hws

def get_credentials(filename: str) -> dict:
    with open(filename, 'r') as credentials_file:
        creds = credentials_file.read()
    
    return json.loads(creds)

credentials = get_credentials("credentials.json")

homeworks = get_hw(credentials["username"], 
                   credentials["password"], 
                   credentials["campus_url"])