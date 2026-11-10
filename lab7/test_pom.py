import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from lab7.pages.home_page import HomePage
from lab7.pages.bestiary_page import BestiaryPage

@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--incognito')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@pytest.mark.smoke
def test_pom_home_search(driver):
    home = HomePage(driver)
    home.open_home()
    home.search_for('дракон')
    assert home.get_search_value() == 'дракон'

@pytest.mark.smoke
def test_pom_bestiary_cards(driver):
    bestiary = BestiaryPage(driver)
    bestiary.open_bestiary()
    assert bestiary.get_danger_marks_count() > 0
    name = bestiary.get_first_monster_name()
    assert len(name) > 0

@pytest.mark.regression
def test_pom_e2e_navigation(driver):
    home = HomePage(driver)
    home.open_home()
    home.go_to_bestiary()

    bestiary = BestiaryPage(driver)
    assert '/bestiary/' in bestiary.get_current_url()

    monster_name = bestiary.get_first_monster_name()
    bestiary.click_first_monster()
    assert 'dnd.su' in driver.current_url

@pytest.mark.regression
def test_cookies_management(driver):
    home = HomePage(driver)
    home.open_home()

    initial_cookies = driver.get_cookies()
    assert isinstance(initial_cookies, list)

    test_cookie = {'name': 'qa_session_id', 'value': 'lab7_cookie_value_999'}
    driver.add_cookie(test_cookie)

    retrieved_cookie = driver.get_cookie('qa_session_id')
    assert retrieved_cookie is not None
    assert retrieved_cookie['value'] == 'lab7_cookie_value_999'

    cookies_dump_path = os.path.join(os.path.dirname(__file__), 'cookies_dump.txt')
    with open(cookies_dump_path, 'w', encoding='utf-8') as f:
        for c in driver.get_cookies():
            f.write(f"{c['name']}={c['value']}\n")

    assert os.path.exists(cookies_dump_path)
    assert os.path.getsize(cookies_dump_path) > 0

    driver.delete_cookie('qa_session_id')
    assert driver.get_cookie('qa_session_id') is None

@pytest.mark.regression
def test_screenshot_capture(driver):
    home = HomePage(driver)
    home.open_home()

    screenshot_path = os.path.join(os.path.dirname(__file__), 'screenshot_home.png')
    if os.path.exists(screenshot_path):
        os.remove(screenshot_path)

    home.take_screenshot(screenshot_path)
    assert os.path.exists(screenshot_path)
    assert os.path.getsize(screenshot_path) > 1000

@pytest.mark.parametrize("query", ["дракон", "гоблин", "орк"])
def test_parametrized_search(driver, query):
    home = HomePage(driver)
    home.open_home()
    home.search_for(query)
    assert home.get_search_value() == query

@pytest.mark.skip(reason="Демонстрация пропуска теста")
def test_skipped_example(driver):
    home = HomePage(driver)
    home.open_home()
    assert False

@pytest.mark.xfail(reason="Демонстрация ожидаемо падающего теста")
def test_expected_failure(driver):
    home = HomePage(driver)
    home.open_home()
    assert driver.title == "Несуществующий заголовок dnd"
