# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.keys import Keys
import time,threading
import _thread
from UI import ui
from lxml import etree
import requests
import time
import re
import random
import serial



ContentLib = []#存放发过的ID 不显示同一ID多次发

def start():
    global queueNum

    payload={
        "q":txt,
        "wvr":"6",
        "Refer":"SWeibo_box"
             }
                                      #headers={}伪装成浏览器的 请求头header
    headers={
        'User-Agent':'Mozilla/6.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36',
    }

    r = requests.get('https://s.weibo.com/weibo?', headers=headers,params=payload) #爬取关键字的搜索结果网页
    print("url:{}".format(r.url))     #打印拼接好的url
    etree.HTML(r.text)                #对返回的内容进行解码
    #print(r.text)                     #打印返回的内容

    tree= etree.HTML(r.text)
    P_list=tree.xpath('//div[@class="card-wrap"]/div[@class="card"]')

    #print(P_list)
    for p_single in P_list:


        SendTime = p_single.xpath('./div[@class="card-feed"]/div[@class="content"]/p[@class="from"]/a/text()')
        timestr = str(SendTime[0])
        pattern = re.compile(r"\d*秒")
        resultSec = re.findall(pattern, timestr)

        patternMin = re.compile(r"\d*分")
        resultMin = re.findall(patternMin, timestr)
        if(len(resultSec) > 0 or len(resultMin) > 0):
            if(len(resultSec) > 0):
                resultMin = 999#让他失效 不然下面还要比较
                pattern2 = re.compile(r"\d*")
                resultSec = int(re.findall(pattern2, resultSec[0])[0])#这个就是秒数
            elif(len(resultMin) > 0):
                resultSec = 999
                pattern2 = re.compile(r"\d*")
                resultMin = int(re.findall(pattern2, resultMin[0])[0])  # 这个就是分钟数


            if(resultSec < 60 or resultMin < 5):#设置时间 n秒内发送的都有效  正则表达式

                ID = p_single.xpath('./div[@class="card-feed"]/div[@class="content"]/p[@class="txt"]/@nick-name')[0]
                content = p_single.xpath('./div[@class="card-feed"]/div[@class="content"]/p[@class="txt"]/text()')
                if(content not in ContentLib):
                    print("***************************")
                    ContentLib.append(content)#加入套餐
                    queueNum += 1
                    print(len(ContentLib))
                    print("博主：{}".format(ID))
                    print("时间：{}".format(SendTime))
                    print("内容：{}".format(content))
                    print("包含关键字：{}".format(p_single.xpath('./div[@class="card-feed"]/div[@class="content"]/p[@class="txt"]/em[@class="s-color-red"]/text()')))

                    Collection=p_single.xpath('./div[@class="card-act"]/ul/li[1]/a/text()')                   #得到所需对象下需要的文本
                    forward=p_single.xpath('./div[@class="card-act"]/ul/li[2]/a/text()')                      #得到所需对象下需要的文本
                    comment = p_single.xpath('./div[@class="card-act"]/ul/li[3]/a/text()')                    #得到所需对象下需要的文本
                    good_number = p_single.xpath('./div[@class="card-act"]/ul/li[4]/a/em/text()')
                    print("收藏:{}".format(Collection))
                    print("转发:{}".format(forward))
                    print("评论:{}".format(comment))
                    print("点赞:{}".format(good_number))



# 为线程定义一个函数
Intensity = 0#灯亮度 0~255
queueNum = 0#未亮灯的数量\
import numpy as np
import cv2


def print_time(threadName, delay):#亮灯的线程
    global queueNum, Intensity
    firstFlag = 0
    count = 0
    countSerial = 0
    while 1:
        if(countSerial > 30):
            if (Intensity > 255):
                Intensity = 255

            countSerial = 0
        countSerial += 1

        img = np.ones((500, 500)) / 255

        if(queueNum > 0 and count % 150 == 0):
            if(firstFlag == 0):
                firstFlag = 1
                queueNum = 5
            queueNum -= 1
            Intensity += 220#亮度改变
            #ser.write(chr(1).encode("ISO-8859-1"))
            count = 0




        Intensity -= 0.5#灯衰减速度
        if (Intensity < 0):
            Intensity = 0
        if (Intensity > 255):
            Intensity = 255

        count += 1
        time.sleep(delay)#灯光变化间隔
        img *= Intensity

        cv2.imshow("img", img)
        cv2.waitKey(1)

        #(Intensity)
        # for i in range(Intensity):
        #     print("*", end="")
        # print(" ")


# 创建两个线程
try:
   _thread.start_new_thread(print_time, ("Thread-1", 0.001))
except:
   print ("Error: 无法启动线程")


txt = "分手"
#ser=serial.Serial("com10",38400,timeout=0.5)#winsows系统使用com1口连接串行口
#程序入口
if __name__ == "__main__":
    while 1:
        start()
        #time.sleep(random.randint(500, 1000) / 1000)

        time.sleep(0.5)
