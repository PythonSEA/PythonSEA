import urllib.request
import re
import urllib.parse
import urllib
import sys
import os
import traceback
import string
#import chardet
import zlib

class CSpider:
    def __init__(self):
        self.cityurl = []
        self.items = []
        # 可能在抓取某个城市的过程中中断，设置一个变量来储存当前城市抓取的第几个页面产生失败
        #self.startpage = 1
        #初始化开始抓取页面的索引
        fileindex = open('../doc/recordindex.txt','r')
        line = fileindex.readlines()
        #页数索引
        self.pindex = line[0].strip('\n')
        #城市索引
        self.cindex = line[1].strip('\n')
        self.compstart = int(self.cindex)
        self.compend = 384
        
        fileindex.close()
        

    # get all city's home url
    def getAllCityUrl(self):
        url = 'http://www.58.com/ruanjiangong/changecity/'
        findcity = re.compile('<a\s*href=[\'\"](http://\w*.58\.com/\w*/)[\"\']\s*onclick=[\'\"]\w*.{1}[\'\"]\w*[\'\"].{1}[\'\"]>')
        home = urllib.request.Request(url)
        homepage = urllib.request.urlopen(home)
        homesource = homepage.read().decode('utf-8')
        #store all city's url
        self.cityurl = findcity.findall(homesource)
        print(self.cityurl)
        file = open('../doc/citiesurl.txt','w')
        for item in self.cityurl:
            file.write(item + '\n')
        file.close()
        
    #spide per city   
    def getCitiesPage(self):
        for url in self.cityurl:
            self.__getOneCityAllPages(url)
            
    def __getOneCityAllPages(self,urlpara ):
        #urlpara = "http://www.baidu.com/"
        print('现在正在抓取第 {0} 个城市 ， url :{1}'.format(self.compstart + 1,urlpara))
        find = re.compile("<span.*tag=[\'\"].*[\"\']\s*url=[\'\"](.*58\.com.*html)[\'\"]\s*name=[\'\"].*[\'\"]>.*</span>")
        self.items = []
        useragent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:37.0) Gecko/20100101 Firefox/37.0'
        accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        header = {'User-Agent':useragent}#,'Accept':accept}
        #页数从上次中断位置开始
        page = int(self.pindex)
        while page < 200:                                # 先设置大数量爬取，后期再去掉相同公司html，
            url = urlpara +'pn' + str(page) + '/'
            try:
                request = urllib.request.Request(url , headers = header)
                print('1. Request , OK')
                pages = urllib.request.urlopen(request)
                print('2. urlopen , OK')
            except:
                print('Have reach back')
                break
            decopage = pages.read().decode('utf-8')
            print('3. decode sourece , OK')
            try:
                found = find.findall(decopage)   # find all right url
                print('4. find url , OK')
            except:
                traceback.print_exc()
            print(found)
            if found:
                try:
                    self.items.extend(found)      # list.extend([a,b]) -> [...,a,b]
                    
                    #for option in found:
                    #    saveurl.write(option + '\n')
                    #self.__storeUrl(found)
                    print('5. save file successfully , OK')
                except:
                    return 0
            else:
                #获取此时真正的url ，若重定向到验证码页面，则保存当前城市索引 和 当前城市页数索引 ，并退出（然后乖乖的去输验证码）
                trueurl = pages.geturl()
                regurl = re.compile('(.*support.58.com/firewall/.*).*')
                result = regurl.findall(trueurl)
                
                if result:  #说明真的重定向了,保存page , self.compstart
                    filetmp = open('../doc/recordindex.txt','w')
                    filetmp.write(str(page)+'\n')
                    filetmp.write(str(self.compstart) + '\n')
                    filetmp.close()
                    print('-----------------------------------------------------------\n赶快用浏览器去刷新58页面，并输入一次验证码，再来爬取网页'\
                          + '\n当前抓取到第{0}个城市第{1}页时需要验证码，剩余{2}个城市等待抓取\n--------------------------------------------------------------'\
                          .format(self.compstart + 1, page , 384 - self.compstart - 1))
                    exit(0)
                    
                #否则，只是本城市无招聘信息/该城市所有的公司已爬完，故跳过此城市，搜索下一城市,页数索引为1，故函数直接返回
                self.pindex = '1'
                break
                

            page += 1
            
        self.__storeUrl(self.items)
        print('6. Store this city\'s page, OK')
        
    def __storeUrl(self,found):
        #before store , assure the url is unique
        found = list(set(found))
        file = open('../doc/compsurl.txt','a')
        for item in found:
            file.write(item + '\n')
        file.close()


    #################  spide lowly
    def downloadPages(self):
        file = open('../doc/citiesurl.txt','r')
        lines = file.readlines()
        ls = lines
        lines = lines[self.compstart:self.compend]
        
        for line1 in lines:
            self.__getOneCityAllPages(line1.strip('\n'))   #去掉尾部恐怖的'\n' T-T
            self.compstart += 1
         
        print('All pages have been downloaded')
    ########################## 以上是抓取每个公司url（并保存到citiesurl.txt）的代码




    
    
    
    
            
