# -*- coding: UTF-8 -*-
from myapp.tools.seleniumTool import SeleniumTool
from myapp.tools.commonTool import CommonTool
from myapp.datacenter.db.dao.cnPeTurnoverRateDao import CnPeRurnoverRateDao
from myapp.datacenter.db.models.cnPERateTurnoverRateModel import CnPERateTurnoverRateModel
from selenium.webdriver.common.by import By
import logging, time
from myapp import xld_db
from myapp.settings import *

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
        self.cnPeTurnoverRateDao = CnPeRurnoverRateDao()
        pass

    def getSSEPERatio(self, beginDate, toDate=None):
        '''
        通过selenium工具获取上证指数指定时间段的平均市盈率，
        :param beginDate:
        :param toDate:
        :return:数组格式：（IndexCode, Date, PE市盈率， 市净率）
        :sample:[('000001', '20180402', '17.73', '0.5638'), ('000001', '20180403', '17.57', '0.4829'), ('000001', '20180404', '17.54', '0.4666')]
        '''
        if beginDate==None or beginDate > toDate:
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
        将web页面获取的数据，插入到数据库中，其中包括与数据库数据去重的逻辑，根据code和date作为唯一key

        :param webData: getSSEPERatio函数返回的页面数据，格式如下：list格式：[（IndexCode, Date, PE市盈率， 市净率）]
        :return:
        '''

        #### 从现有的数据库中读出已经存在的model记录，用于去重, DB数据字段：
        # stock_code
        # date
        # pe_ratee
        # turnover_ratee

        ###### 1. 从数据库读取数据
        existedModelRecords = self.cnPeTurnoverRateDao.getCnPeTurnoverRate()
        existedRecordKeyDict = {}
        for existedRecord in existedModelRecords:
            key =  "{}_{}".format(existedRecord.stock_code, existedRecord.date)
            existedRecordKeyDict[key] = None  # 仅保存key，用于去重

        modelList=[]
        ###### 2. 遍历新数据，判断是否已经在数据库中存在，添加新数据
        for data in webData:
            model = CnPERateTurnoverRateModel(data[0],  #code
                                              data[1],  #date
                                              data[2],  #pe rate
                                              data[3]   #turn over rate
                                              )
            key = "{}_{}".format(data[0], data[1])
            if existedRecordKeyDict.has_key(key):
                ## 记录已经存在，不需要重复添加
                continue
            else :
                modelList.append(model)

        ###### 3. 添加数据
        if len(modelList) > 0:
            for model in modelList:
                xld_db.session.add(model)
            xld_db.session.commit()

        return True


if __name__ == "__main__":
    sse = SseDataSource()
    sse.getSSEPERatio(beginDate="2018-02-03", toDate="2018-04-04")

    # st = SeleniumTool(SseDataSource.peRatioCaptureRootUrl)
    # d = st.getDriver()
    # d.find_element_by_id(SseDataSource.sseDatePickerId)
    #
