import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'index.html'))
    driver.get(f"file:///{file_path.replace(os.sep, '/')}")
    yield driver
    driver.quit()

def test_page_load(driver):
    assert "Генератор персонажа" in driver.title
    h1 = driver.find_element(By.ID, 'page-title')
    assert h1.is_displayed()
    assert driver.find_element(By.ID, 'char-name').is_displayed()
    assert driver.find_element(By.ID, 'submit-btn').is_displayed()

def test_validation_empty_name(driver):
    submit_btn = driver.find_element(By.ID, 'submit-btn')
    submit_btn.click()

    error_div = driver.find_element(By.ID, 'name-error')
    assert error_div.is_displayed()
    assert "Имя не может быть пустым" in error_div.text

    result_box = driver.find_element(By.ID, 'result-box')
    assert not result_box.is_displayed()

def test_successful_creation(driver):
    wait = WebDriverWait(driver, 10)

    name_input = driver.find_element(By.ID, 'char-name')
    name_input.clear()
    name_input.send_keys('Гэндальф')

    class_select = Select(driver.find_element(By.ID, 'char-class'))
    class_select.select_by_value('Волшебник')

    level_input = driver.find_element(By.ID, 'char-level')
    level_input.clear()
    level_input.send_keys('5')

    driver.find_element(By.ID, 'submit-btn').click()

    result_box = wait.until(EC.visibility_of_element_located((By.ID, 'result-box')))
    assert result_box.is_displayed()

    assert driver.find_element(By.ID, 'res-name').text == 'Гэндальф'
    assert driver.find_element(By.ID, 'res-class').text == 'Волшебник'
    assert driver.find_element(By.ID, 'res-level').text == '5'

def test_class_selection_dropdown(driver):
    class_elem = driver.find_element(By.ID, 'char-class')
    select = Select(class_elem)

    select.select_by_visible_text('Жрец')
    assert select.first_selected_option.text == 'Жрец'

    select.select_by_visible_text('Плут')
    assert select.first_selected_option.text == 'Плут'
