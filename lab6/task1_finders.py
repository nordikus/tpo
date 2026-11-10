from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1920,1080')

driver = webdriver.Chrome(options=options)
driver.implicitly_wait(10)

try:
    driver.get('https://dnd.su')
    print('Сайт открыт успешно. Title:', driver.title)

    elem_id = driver.find_element(By.ID, 'aside')
    print('[1. By.ID] Найден элемент сайдбара (id=aside):', elem_id.tag_name)

    elem_name = driver.find_element(By.NAME, 'login')
    print('[1. By.NAME] Найдено поле входа (name=login):', elem_name.get_attribute('placeholder'))

    css_comp1 = driver.find_element(By.CSS_SELECTOR, 'div#ya-site-form0 table td input.ya-site-form__input-text')
    print('[2. CSS составной 1] Поле поисковой строки:', css_comp1.get_attribute('class'))

    css_comp2 = driver.find_element(By.CSS_SELECTOR, 'form[action*="/login"] div.grid input[name="password"]')
    print('[2. CSS составной 2] Поле пароля авторизации:', css_comp2.get_attribute('name'))

    xpath_comp1 = driver.find_element(By.XPATH, '//div[@id="ya-site-form0"]//table//input[contains(@class, "ya-site-form__input-text")]')
    print('[3. XPath составной 1]:', xpath_comp1.get_attribute('outerHTML')[:80])

    xpath_comp2 = driver.find_element(By.XPATH, '//form[contains(@action, "login")]//input[@name="remember_me" and @type="checkbox"]')
    print('[3. XPath составной 2]:', xpath_comp2.get_attribute('name'))

    partial_link = driver.find_element(By.PARTIAL_LINK_TEXT, 'Бестиарий')
    print('[4. By.PARTIAL_LINK_TEXT]:', partial_link.text, '->', partial_link.get_attribute('href'))

    nav_elements = driver.find_elements(By.CSS_SELECTOR, 'aside a, .sidebar a, nav a')
    print(f'[5. Список элементов]: Найдено {len(nav_elements)} элементов навигации:')
    for item in nav_elements[:5]:
        t = item.text.strip()
        h = item.get_attribute('href')
        if t:
            print(f'   - {t} ({h})')

finally:
    driver.quit()
