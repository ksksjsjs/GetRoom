import requests
import selenium.webdriver.common.by
from selenium import webdriver
from selenium.webdriver.edge.webdriver import Service
import time
import pickle
from selenium.webdriver.common.by import By
import datetime

login_url = 'http://ids.xidian.edu.cn/authserver/login?service=https%3A%2F%2Fauth.scientia.com.cn%2Fv2%2Fsignin-cas%3Fstate%3DCfDJ8CaQIIr2J39Ijme2Hz0wYvbE0GccOeJI7wJUd-VmDp1JNJDdLZ0fBwc3Z4zhAwsgzx6jIoZU7HVyOknxzrVpyfqFvFW3QzrFppWaidfFroFcvxWm9KATsMNjnEeZFGvEEMACjT2EIZ8KKqy0ur2obMI97toaPGG8VJfnRmGu5uxyXQeSSGrXleDXwdKCiH8uOpq4KeFdUyKdEsMEqTNFC5JRhhZBdLf0mpyuVu6viJHf096Updhq5LZ_vu2-dmVZO2puWy-IacP6LPYK3K3VUKzPiiH7w6kuHTATvLAcRvpF5WHDy86X0R4VDWoJqwCMX5v9cPS53PY_2JFI52cTH1skzyI61G7warvPCi7URC6N'
target_url = 'https://booking.xidian.edu.cn/#/app/booking-types/e22f3c4e-0a9b-43b0-b42f-81000ab730c7'
month_day = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)


class Room:
    def __init__(self):
        self.driver = webdriver.Edge()
        self.driver.implicitly_wait(5)
        self.login_method = 1

    def get_room(self):
        self.driver.implicitly_wait(5)
        # self.set_cookie()
        # 找日期（因为修身室比较火，所以只能预约到七天后得时间了）
        self.choose_time()

        # 找时间（在此处改时间，注意时间最多三个小时）
        self.driver.find_element(By.CSS_SELECTOR, "option[value='19']").click()
        self.driver.find_element(By.CSS_SELECTOR, "option[value='22']").click()

        # 点击修身室
        self.driver.find_element(By.CLASS_NAME, 'resourcesList-item-infos').click()

        elements = self.driver.find_elements(By.CSS_SELECTOR, 'li > div > a > span > .resourcesList-item-name')
        element = elements[2]
        if element.text == '修身室9-108':
            element.click()
        else:
            self.driver.find_element(By.CSS_SELECTOR, 'div.k-title > .k-btn-next-month').click()
            self.choose_time()
            element = elements[2]
            element.click()

        # 转换页面到抢房间页面
        for handle in self.driver.window_handles:
            time.sleep(0.1)
            self.driver.switch_to.window(handle)
            if "修身室9-108" in self.driver.title:
                break

        # 开始循环抢房间
        self.element = self.driver.find_element(By.CSS_SELECTOR, 'footer > button')
        while self.driver.title.find('我的预定 — 资源预约平台') == -1:
            self.element = self.driver.find_element(By.CSS_SELECTOR, 'footer > button')
            print('正在选取')
            self.element.click()
            time.sleep(0.05)
            if self.driver.title == '修身室9-108':
                self.driver.refresh()
        print('选房间成功')

    # 选时间

    def choose_time(self):
        now_time = datetime.datetime.now()
        time_day = int(now_time.isoformat()[8]) * 10 + int(now_time.isoformat()[9]) + 7 + 1
        time_month_day = month_day[(int(now_time.isoformat()[5]) * 10 + int(now_time.isoformat()[6])) - 1]
        if time_day > time_month_day:
            time_day %= time_month_day
        time_str = str(time_day)
        day = self.driver.find_element(By.CLASS_NAME, 'k-days')
        elements = day.find_elements(By.TAG_NAME, 'span')
        for element in elements[2:]:
            if element.text == time_str:
                element.click()
                break
        time.sleep(0.5)

    def login(self):
        self.driver.get(target_url)
        while self.driver.title.find('统一身份认证平台') != -1:
            time.sleep(3)
        print('登录成功')
        self.get_room()


if __name__ == '__main__':
    room = Room()
    room.login()
