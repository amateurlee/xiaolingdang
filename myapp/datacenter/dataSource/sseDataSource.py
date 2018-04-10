# -*- coding: UTF-8 -*-
from myapp.services.seleniumTool import SeleniumTool
from myapp.services.commonTool import CommonTool
from selenium.webdriver.common.by import By
import logging, time


class SseDataSource:
    sseDatePickerId = "start_date2"
    sseQueryButtenID = "btnQuery"
    avgPERatioCaptureRootUrl = "http://www.sse.com.cn/market/stockdata/overview/day/"
    avgNoDataTDXpath = "//td[contains(text(),'没有数据')]"
    avgPERatioValueXpath = "//td[contains(text(),'平均市盈率')]/../td[3]/div"
    avgTurnoverRatioValueXpath = "//td[contains(text(),'换手率')]/../td[3]/div"
    avgPERatioRealDate = "//div[@class='sse_table_title2']/p"

    def __init__(self):
        # http://img1.money.126.net/data/[沪深拼音]/[是否复权]/[周期]/times/[股票代码].jso
        # http://img1.money.126.net/data/hs/kline/day/times/0000300.json
        self.allDataUrl = "http://img1.money.126.net/data/hs/{stockrightprice}/{period}/times/{stocktype}{stockcode}.json"

    def getSSEPERatio(self, beginDate, toDate=None):
        if beginDate > toDate:
            logging.error("Getting PERatio data from date({}) to date({}) error".format(beginDate, toDate))
            return False
        st = SeleniumTool(SseDataSource.avgPERatioCaptureRootUrl)
        st.openUrl()
        time.sleep(10)  # 网址有脚本执行自动填充时间
        dateList = CommonTool.dateRange(beginDate, toDate)
        PERatio = []
        bakPERatio = bakTORatio = -1
        hasNoDataDateDelta = 0 # no more than 2
        for date in dateList:
            # 查询某一天的数据
            while True: # 提交请求拿不到请求日期的页面时继续重试
                st.setDatePickerValueById(SseDataSource.sseDatePickerId, date)  # "2018-04-08"
                searchBtn = st.getEleById(SseDataSource.sseQueryButtenID)
                searchBtn.click()
                realDateText = st.getText(By.XPATH, SseDataSource.avgPERatioRealDate)

                if realDateText == u"数据日期：{}".format(date):
                    break # 已经加载了当前日期
                else:
                    s = "Request data for date:{} failed, retry".format(date)
                    logging.warn (s)
                    print s
                    time.sleep(3)
            exist = st.isExist(By.XPATH, SseDataSource.avgNoDataTDXpath)
            if exist:
                hasNoDataDateDelta +=1
                if hasNoDataDateDelta >=3:
                    s = "Empty date delta larger than 3, need to be check for date:{}".format(date)
                    logging.warn (s)
                    print s
            else:
                peRatio = st.getText(By.XPATH, SseDataSource.avgPERatioValueXpath)
                turnoverRate = st.getText(By.XPATH, SseDataSource.avgTurnoverRatioValueXpath)
                retryTime = 5 ## 获取pe值失败时重试5次
                while (peRatio == bakPERatio and turnoverRate == bakTORatio) or \
                        peRatio==None or turnoverRate == None:
                    logging.warn("retrying to get data for date:" + date)
                    print "retrying to get data for date:" + date
                    retryTime -= 1
                    # 两次获得的结果一样的时候，任务获取失败，需要重试
                    st.setDatePickerValueById(SseDataSource.sseDatePickerId, date)  # "2018-04-08"
                    searchBtn = st.getEleById(SseDataSource.sseQueryButtenID)
                    searchBtn.click()
                    time.sleep(2)
                    peRatio = st.getText(By.XPATH, SseDataSource.avgPERatioValueXpath)
                    turnoverRate = st.getText(By.XPATH, SseDataSource.avgTurnoverRatioValueXpath)
                    if retryTime <= 0:
                        break

                if (retryTime <= 0):
                    # 当然日期的数据获取失败
                    logging.error("Getting PE data for SSE failed on date:" + date)
                    continue
                else:
                    ratio = (date.replace("-", ""), peRatio, turnoverRate)
                    PERatio.append(ratio)
                    bakPERatio = peRatio
                    bakTORatio = turnoverRate
                    hasNoDataDateDelta = 0

        return PERatio


if __name__ == "__main__":
    sse = SseDataSource()
    sse.getSSEPERatio(beginDate="2018-02-03", toDate="2018-04-04")

    # st = SeleniumTool(SseDataSource.peRatioCaptureRootUrl)
    # d = st.getDriver()
    # d.find_element_by_id(SseDataSource.sseDatePickerId)
    #
