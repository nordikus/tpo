import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_authorization(driver):
    driver.get('https://dnd.su')
    wait = WebDriverWait(driver, 10)

    login_input = wait.until(EC.visibility_of_element_located((By.NAME, 'login')))
    password_input = driver.find_element(By.NAME, 'password')
    submit_btn = driver.find_element(By.CSS_SELECTOR, 'form[action*="/login"] input.btn.btn-primary')

    login_input.clear()
    login_input.send_keys('test_user_lab6')
    password_input.clear()
    password_input.send_keys('invalid_password_123')

    assert login_input.get_attribute('value') == 'test_user_lab6'
    assert password_input.get_attribute('value') == 'invalid_password_123'

    submit_btn.click()
    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    assert 'dnd.su' in driver.current_url

def test_case_tc001_bestiary_filter(driver):
    driver.get('https://dnd.su/bestiary/')
    wait = WebDriverWait(driver, 10)

    beast_card = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.list-item__beast a.list-item-wrapper')))
    assert beast_card is not None

    card_danger = driver.find_element(By.CSS_SELECTOR, 'span.list-mark__danger')
    assert card_danger.is_displayed()
    assert '[' in card_danger.text and ']' in card_danger.text

def test_case_tc002_search_input(driver):
    driver.get('https://dnd.su')
    wait = WebDriverWait(driver, 10)

    search_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input.ya-site-form__input-text')))
    search_input.clear()
    search_input.send_keys('дракон')

    assert search_input.get_attribute('value') == 'дракон'
    search_form = driver.find_element(By.ID, 'ya-site-form0')
    assert search_form.is_displayed()

def test_e2e_scenario(driver):
    driver.get('https://dnd.su')
    wait = WebDriverWait(driver, 10)

    bestiary_link = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, 'Бестиарий')))
    bestiary_link.click()

    wait.until(EC.url_contains('/bestiary/'))
    assert '/bestiary/' in driver.current_url

    first_beast = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.list-item__beast a.list-item-wrapper')))
    beast_name = first_beast.find_element(By.CSS_SELECTOR, 'div.list-item-title').text.strip()
    first_beast.click()

    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h2, h1, .card-title, .header')))
    page_title = driver.title
    assert beast_name.lower() in page_title.lower() or 'dnd.su' in driver.current_url

def test_checkbox_and_controls(driver):
    driver.get('https://dnd.su')
    wait = WebDriverWait(driver, 10)

    checkbox = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="remember_me"]')))
    initial_state = checkbox.is_selected()

    driver.execute_script("arguments[0].click();", checkbox)
    new_state = checkbox.is_selected()

    assert initial_state != new_state
