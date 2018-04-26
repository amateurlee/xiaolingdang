# -*- coding: UTF-8 -*-
from myapp.tools.seleniumTool import SeleniumTool
from myapp.tools.commonTool import CommonTool
from selenium.webdriver.common.by import By
import logging, time


class SseDataSource:
    sseDatePickerId = "start_date2"
    sseQueryButtenID = "btnQuery"
    szzsCode = "000001"
    ### 上证市场平均市盈率和平均换手率的XPATH
    avgPERatioCaptureRootUrl = "http://www.sse.com.cn/market/stockdata/overview/day/"
    avgNoDataTDXpath = "//td[contains(text(),'没有数据')]"
    avgPERatioValueXpath = "//td[contains(text(),'平均市盈率')]/../td[3]/div"
    avgTurnoverRatioValueXpath = "//td[contains(text(),'换手率')]/../td[3]/div"
    avgPERatioRealDate = "//div[@class='sse_table_title2']/p"

    def __init__(self):
        pass

    def getSSEPERatio(self, beginDate, toDate=None):
        '''
        通过selenium工具获取上证指数指定时间段的平均市盈率，
        :param beginDate:
        :param toDate:
        :return:数组格式：（IndexCode, Date, PE市盈率， 市净率）
        :sample:[('000001', '20180402', '17.73', '0.5638'), ('000001', '20180403', '17.57', '0.4829'), ('000001', '20180404', '17.54', '0.4666')]
        '''
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
                    ratio = (SseDataSource.szzsCode, date.replace("-", ""), peRatio, turnoverRate)
                    PERatio.append(ratio)
                    bakPERatio = peRatio
                    bakTORatio = turnoverRate
                    hasNoDataDateDelta = 0
        return PERatio


    def addCnSSEPERateTORateToDB(self, webData):
        '''
        将上证平均PE和换手率数据添加到数据库，添加之前首先判断是否有重复的数据，去重后添加，
        index_table_cn表中的数据可以以stock_code和time作为唯一标示
        :param retData:
        :return:
        '''

        ###### 1. 从数据库读取数据

        szzsData = self.dbTool.getCnIndexTableDataByStockCode(STOCK_INFO["szzs"]["code"])
        searchIndexData = {}  # 仅用来保存key
        modelDataList = []
        if szzsData:
            for data in szzsData:
                searchIndexData[data.time] = 0
        ###### 2. 遍历新数据，判断是否已经在数据库中存在，添加新数据
        for wdata in webData:
            if searchIndexData.has_key(wdata["time"]):
                continue  # 数据库中已经存在当前时间的记录
            else:
                model = IndexTableCnModel.IndexTableCnModel(index_name=wdata["index_name"],
                                                            stock_code=wdata["stock_code"],
                                                            time=wdata["time"], close=wdata["close"])
                modelDataList.append(model)
        ###### 3. 添加数据
        if len(modelDataList) > 0:
            for model in modelDataList:
                xld_db.session.add(model)
            xld_db.session.commit()


if __name__ == "__main__":
    sse = SseDataSource()
    sse.getSSEPERatio(beginDate="2018-02-03", toDate="2018-04-04")

    # st = SeleniumTool(SseDataSource.peRatioCaptureRootUrl)
    # d = st.getDriver()
    # d.find_element_by_id(SseDataSource.sseDatePickerId)
    #
