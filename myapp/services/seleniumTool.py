# -*- coding: UTF-8 -*-

from pyvirtualdisplay import Display
from selenium import webdriver
import time, sys, logging
from myapp.settings import *
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


class SeleniumTool:

    def __init__(self, url=None):
        self.url = url
        self.display = None
        osType = sys.platform
        dirverFirefoxPath = ''
        if "linux" in osType:
            dirverFirefoxPath = os.path.abspath(APP_PATH + "/services/geckodriverlinux")
            # now Firefox will run in a virtual display.
            # you will not see the browser.
            self.display = Display(visible=0, size=(1024, 768))
            self.display.start()
        elif "darwin" in osType:
            dirverFirefoxPath = os.path.abspath(APP_PATH + "/services/geckodrivermac")
        else:
            dirverChromePath = os.path.abspath(APP_PATH + "/services/chromedriverlinux")  # not support windows for now

        self.driver = webdriver.Firefox(executable_path=dirverFirefoxPath)

    def __del__(self):
        import sys
        osType = sys.platform
        if "linux" in osType:
            self.display.stop()
        self.driver.quit()

    def getDriver(self):
        return self.driver

    def openUrl(self, url=None):
        ''' test purpose '''
        if url:
            self.url = url
        logging.info("Opening url:" + self.url)
        self.driver.get(self.url)

    def getEleByName(self, name):
        '''
        find element by name
        :param name: element name
        :return: element
        '''
        locator = (By.NAME, name)
        logging.info("Waiting element {} appear ".format(name))
        print "wait name:" + name
        WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located(locator))
        logging.info("Got element {}, return it".format(name))
        print "Got name:" + name
        return self.driver.find_element_by_name(name)

    def getEleById(self, id):
        '''
        get element by id
        :param id: element id
        :return: element
        '''
        locator = (By.ID, id)
        WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located(locator))
        return self.driver.find_element_by_id(id)

    def setDatePickerValueById(self, id, value):
        '''
        设置日期控件的日期指，2018-04-09
        :param id:
        :param value:
        :return:
        '''
        datePicker = self.getEleById(id)
        js = "document.getElementById('" + id + "').removeAttribute('readonly')"
        self.driver.execute_script(js)
        datePicker.clear()
        datePicker.send_keys(value)

    def isExist(self, by, value, waitSecods = 0):
        '''
        判断element是否存在
        :param by:
        :param value:
        :return:
        '''
        existFlag = True
        try:
            ret = self.driver.find_element(by, value)
        except NoSuchElementException, e:
            existFlag = False
        return existFlag

    def getText(self, by, avgPERatioValueXpath):
        try:
            ret = self.driver.find_element(by, avgPERatioValueXpath)
            return ret.text
        except Exception, e:
            logging.error("get elment "+avgPERatioValueXpath+ " failed")


if __name__ == "__main__":
    st = SeleniumTool("http://www.baidu.com")
    st.openUrl()
    ele = st.driver.find_element(By.ID, "mCon")
    print ele.text