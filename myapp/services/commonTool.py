# -*- coding: UTF-8 -*-

import urllib, urllib2


def _convertParamPairToStr(params):
    paramStr = "";
    for k,v in params:
        paramStr = "{paramStr}&{key}={value}".format(paramStr,k, v);
    return paramStr


class CommonTool:

    @staticmethod
    def doPost( url, headers, values):
        # url = 'http://www.someserver.com/cgi-bin/register.cgi'
        # user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'  # 将user_agent写入头信息
        # values = {'name': 'who', 'password': '123456'}
        # headers = {'User-Agent': user_agent}
        data = urllib.urlencode(values)
        req = urllib2.Request(url, data, headers)
        response = urllib2.urlopen(req)
        the_page = response.read()


    @staticmethod
    def doGet( url, params=None, encodeFlag=False):
        '''
        发送GET请求并返回结果，支持urlencode
        :param self:
        :param url:
        :param params: python Dict类型的数据可以不提供
        :param encodeFlag: False代表不需要对后面的参数urlencode
        :return:
        '''
        # values = {'name': 'who', 'password': '123456'}

        if params:
            if(encodeFlag) :
                data = urllib.urlencode(params)
            else :
                data = _convertParamPairToStr(params)
            url = "{url}?{data}".format(url=url, data=data);

        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        result = response.read()
        return result