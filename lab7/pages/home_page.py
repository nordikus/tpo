from selenium.webdriver.common.by import By
from lab7.pages.base_page import BasePage

class HomePage(BasePage):
    URL = 'https://dnd.su'

    SEARCH_INPUT = (By.CSS_SELECTOR, 'input.ya-site-form__input-text')
    SEARCH_FORM = (By.ID, 'ya-site-form0')
    LOGIN_INPUT = (By.NAME, 'login')
    PASSWORD_INPUT = (By.NAME, 'password')
    REMEMBER_ME_CHECKBOX = (By.NAME, 'remember_me')
    AUTH_SUBMIT_BUTTON = (By.CSS_SELECTOR, 'form[action*="/login"] input.btn.btn-primary')
    BESTIARY_LINK = (By.PARTIAL_LINK_TEXT, 'Бестиарий')

    def open_home(self):
        self.open(self.URL)

    def search_for(self, text):
        self.send_keys(self.SEARCH_INPUT, text)

    def get_search_value(self):
        return self.find_visible(self.SEARCH_INPUT).get_attribute('value')

    def fill_auth(self, login, password):
        self.send_keys(self.LOGIN_INPUT, login)
        self.send_keys(self.PASSWORD_INPUT, password)

    def toggle_remember_me(self):
        cb = self.find(self.REMEMBER_ME_CHECKBOX)
        self.driver.execute_script("arguments[0].click();", cb)
        return cb.is_selected()

    def submit_auth(self):
        self.click(self.AUTH_SUBMIT_BUTTON)

    def go_to_bestiary(self):
        self.click(self.BESTIARY_LINK)
