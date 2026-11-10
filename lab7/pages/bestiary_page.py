from selenium.webdriver.common.by import By
from lab7.pages.base_page import BasePage

class BestiaryPage(BasePage):
    URL = 'https://dnd.su/bestiary/'

    CARDS = (By.CSS_SELECTOR, 'div.list-item__beast a.list-item-wrapper')
    DANGER_MARKS = (By.CSS_SELECTOR, 'span.list-mark__danger')
    ITEM_TITLES = (By.CSS_SELECTOR, 'div.list-item-title')

    def open_bestiary(self):
        self.open(self.URL)

    def get_first_monster_name(self):
        titles = self.find_all(self.ITEM_TITLES)
        return titles[0].text.strip()

    def click_first_monster(self):
        cards = self.find_all(self.CARDS)
        cards[0].click()

    def get_danger_marks_count(self):
        return len(self.find_all(self.DANGER_MARKS))
