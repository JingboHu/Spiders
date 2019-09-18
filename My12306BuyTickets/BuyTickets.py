# -*- coding:utf-8 -*-
# author: hu jingbo
# date:2019-03-26

import time
from io import BytesIO
from PIL import Image

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

from ruokuai import RClient

# log in and click pictures
class LoginAndCrack():
    def __init__(self):
        self.login_url = 'https://kyfw.12306.cn/otn/login/init'
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser,20)
        self.account = 'bokingo'
        self.password = 'hjb19940809dm'
        self.soft_id = '125392'
        self.soft_key = '47718eebc7914c419f65c68c3f591ce2'
        self.ruokuai = RClient(self.account,self.password,self.soft_id,self.soft_key)

    def open(self):
        '''
        打开网页输入用户密码
        :return: None
        '''
        self.browser.get(self.login_url)
        account = self.browser.find_element_by_id('username')
        account.send_keys(self.account)
        password = self.browser.find_element_by_id('password')
        password.send_keys(self.password)

    def get_click_button(self):
        '''
        获取初始验证按钮
        :return:
        '''
        button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'touclick-wrapper')))
        return  button

    def get_touclick_element(self):
        '''
        获取验证码图片对象
        :return: 图片对象
        '''
        element = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME,'touclick-pub-content')))
        return element

    def get_position(self):
        '''
        获取验证码位置
        :return: 验证码位置元组
        '''
        element = self.get_touclick_element()
        time.sleep(2)
        location = element.location
        size = element.size
        top,bottom,left,right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size['width']
        return (top, bottom, left, right)

    def get_screenshot(self):
        '''
        获取网页截图
        :return: 截图对象
        '''
        screenshot = self.browser.get_screenshot_as_png()
        screenshot = image.open(BytesIO(screenshot))
        return screenshot

    def get_touclick_image(self,name = 'captcha.png'):
        '''
        获取验证码图片
        :param name:
        :return: 图片对象
        '''
        top,bottom,left,right = self.get_position()
        print('验证码位置',top,bottom,left,right)
        screenshot = self.get_screenshot()
        captcha = screenshot.crop(left,top,right,bottom)
        captcha.save(name)
        return captcha

    def get_points(self,captcha_result):
        '''
        解析识别结果
        :param captcha_result: 识别结果
        :return: 转化后的结果
        '''
        groups = captcha_result.get('pic_str').split('|')
        locations = [[int(number) for number in group.split(',')] for group in groups]
        return locations

    def touch_click_words(self,locations):
        '''
        点击验证图片
        :param locations:点击位置
        :return: None
        '''
        for location in locations:
            print(location)
            ActionChains(self.browser).move_to_element_with_offset(self.get_touclick_element(),location[0],
                                                                   location[1]).click().perform()
            time.sleep(1)

    def touch_click_verify(self):
        '''
        点击验证按钮
        :return: None
        '''
        button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME,'touclick-pub-submit')))
        button.click()

    def login(self):
        '''
        登录
        :return:None
        '''
        submit = self.wait.until(EC.element_to_be_clickable((By.ID,'_submit')))
        submit.click()
        time.sleep(10)
        print('登录成功')

    def crack(self):
        '''
        破解入口
        :return:
        '''
        self.open()
        # 点击验证按钮
        button = self.get_click_button()
        button.click()
        # 获取验证码图片
        images = self.get_touclick_image()
        bytes_array = BytesIO()
        images.save(bytes_array,format='PNG')
        # 识别验证码,9102为验证码类型
        result = self.ruokuai.rk_create(bytes_array.getvalue(),9102)
        print(result)
        locations = self.get_points(result)
        self.touch_click_words(locations)
        self.touch_click_verify()
        # 判断是否成功
        success = self.wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME
                                                                    ,'touclick-hod-note','验证成功')))
        print(success)

        # 失败后重试
        if not success:
            self.crack()
        else:
            self.login()

if __name__ == '__main__':
    crack = LoginAndCrack()
    crack.crack()

# ticket_url = 'https://www.12306.cn/index/index.html'