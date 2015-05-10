import threading
import sys
import re
import urllib.request
#import chardet
import os



class CGetCompsInfo():
	def __init__(self):
		self.threadlist = []
		self.webindex = []
		self.urls = []
		#全局ip标志，用于线程通信
		self.ipindex = 0
		self.iplist = []
        #设置锁
		self.lock = threading.Lock()
        
        #50个线程，每个线程约处理1000条记录
		for i in range(0,50):
			t = threading.Thread(target = self.getCompInfo , name = "ChildThread {0}".format(i))
			self.threadlist.append(t)
        
        #初始化各个线程开始抓取的网页，和各个线程已抓取的网页数量 
		with open("../doc/currentindex.txt",'r') as file:
			lines = file.readlines()
			if not lines:
				for i in range(0,50):
					l = [i*1000,0]
					self.webindex.append(l)
			else:
				for line in lines[0:50]:
					line = line.strip('\n')
					li = line.split(' ')
					self.webindex.append([int(li[0]) , int(li[1])])
                    
        #清空文件
		with open("../doc/currentindex.txt",'w') as file:
			file.write('')
                    
        #载入每个公司的url
		with open('../doc/compsurl.txt','r') as file:
			self.urls = file.readlines()
    
		#载入代理IP
		with open("../doc/ip.txt",'r') as file:
			self.iplist = file.readlines()
         
	def getCompInfo(self):
		#为各个线程分配验证码标志，
		isnextip = 0
		
        #为每个线程分配urls
		name = threading.currentThread().getName()
        
		name = name.strip('\n').split(' ')
		namenum = int(name[1])
        
		self.lock.acquire()
		
		try:
			if self.webindex[namenum][0] >= 49000:
				threadownurls = self.urls[49*1000 + self.webindex[namenum][1]:]
                
			else:
				threadownurls = self.urls[self.webindex[namenum][0] + self.webindex[namenum][1] : self.webindex[namenum][0] + 1000]
                
			counter = self.webindex[namenum][1]
		finally:
			self.lock.release()
        #为50个线程各自创建文件夹
		regfind1 = re.compile("<div class=\"posMsg borb\">(.*?)<div class=\"Job requirements\">" , re.S)  #确定位置
		regfind2 = re.compile("<[^>]*>")                                                              #去掉<>标签
		regfind3 = re.compile("&[^&;]*;")                                                              #去掉实体字符
		regfind4 = re.compile("(\w+\.\w+\.\w*|[0-9]{1,2}\.|\n|[Qq][Qq]|[Ii][Tt])")                       #去掉网址等
		regfind5 = re.compile(".*?([A-Za-z]+[0-9]?[\' \']?[\.]?[A-Za-z]+|[cC][#]?[\+]{0,2}|[\.][NnEeTt]{3}).*?")    #选取内容       

		for url in threadownurls:
			url = url.strip('\n')
            #print("From {0} url:{1}".format(self.webindex[namenum][0] + counter ,url))
			try:
				request = urllib.request.Request(url)
				print('1. Request from ----> [{0}], OK'.format(threading.currentThread().getName()))
				data = urllib.request.urlopen(request)
				print('2. Urlopen from ----> [{0}], OK'.format(threading.currentThread().getName()))
			except:
				self.lock.acquire()
				
				try:
					#self.__storeIndexExcept(self.webindex[namenum][0] , counter)
					self.webindex[namenum][1] = counter
				finally:
					self.lock.release()
					return 0
            #data = zlib.decompress(data, 16+zlib.MAX_WBITS)
            
            #有可能是重定向网页的内容
			try:
				pages = data.read().decode('utf-8')
				print('2. decode from ----> [{0}], OK'.format(threading.currentThread().getName()))
				found = regfind1.findall(pages)
			except:
				self.lock.acquire()
				
				try:
					#self.__storeIndexExcept(self.webindex[namenum][0] , counter)
					self.webindex[namenum][1] = counter
				finally:
					self.lock.release()
					return 0				
            #print(pages[0:50])
			if found:
                #print(found)
                #if found:
                #print("ifif")
				found = regfind2.sub('\t',found[0]) 
				found = regfind3.sub('\t',found)
				found = regfind4.sub('\t',found)
				found2 = regfind5.findall(found)
				try:
					print("Found :{0}".format(found2))
				except:
					self.lock.acquire()
					try:
						#self.__storeIndexExcept(self.webindex[namenum][0] , counter)
						self.webindex[namenum][1] = counter
					finally:
						self.lock.release()	
						return 0
                #转成大写，并除掉相同元素
				loadlist = []
				for f in found2:
					loadlist.append(f.upper())
				loadlist = list(set(loadlist))
                #写入文件
				try:
					file = open('../doc/Children{0}vInfo.txt'.format(namenum) , 'a')
					for f in loadlist: 
						file.write(f + '\t')
					file.write('\n')
				finally:
					file.close()
                #pages=""
				print("if")
            #判断网页是否重定向
			else:
				try:
					trueurl = data.geturl()
					regurl = re.compile('(.*support\.58\.com/firewall/.*)')
					result = regurl.findall(trueurl)
				except:
					self.lock.acquire()
					try:
						#self.__storeIndexExcept(self.webindex[namenum][0] , counter)
						self.webindex[namenum][1] = counter
					finally:
						self.lock.release()
						return 0
				if result:
                    #是否找新的代理ip
					self.lock.acquire()
					try:
						if isnextip == self.ipindex and self.ipindex < len(self.iplist):
							proxy = urllib.request.ProxyHandler({'http':self.iplist[self.ipindex].strip('\n')})
							opener = urllib.request.build_opener(proxy);  
							urllib.request.install_opener(opener)
							self.ipindex = self.ipindex + 1
							print("-------------------------------------------------\n更新了代理IP，来自 ----> [{0}]\n------------------------------------------------------\n"\
							.format(threading.currentThread().getName()))
					except:
						self.webindex[namenum][1] = counter
						return 0
					finally:
						self.lock.release()
					isnextip = isnextip + 1
					
					#获取当前需要验证码的url的索引，然后再索引加1处插入复制值继续进行爬取
					index = threadownurls.index(url)
					threadownurls.insert(index + 1 , url)
					continue

			counter = counter + 1
		#线程完成了所有网址的抓取
		self.lock.acquire()
		try:
			self.webindex[namenum][1] = counter
		finally:
			self.lock.release()
			
	def startThread(self):
		for i in range(0,50):
			try:
				self.threadlist[i].setDaemon(1)
				self.threadlist[i].start()
			except:
                
				print(self.threadlist[i].getName())
            
		for i in range(0,50):
			print('{0}'.format(threading.currentThread().getName()))
			self.threadlist[i].join()
			
	def storeWebIndex(self):
		file = open("../doc/currentindex.txt",'w')
		for line in self.webindex:
			file.write(str(line[0]) + ' ' + str(line[1]) + '\n')
		file.close()
		
	
		

	

