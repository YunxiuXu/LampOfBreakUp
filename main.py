# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.keys import Keys
import time,threading
from UI import ui
from lxml import etree
import requests

#加载UI用户界面
list_var=[]                           #list_var用于接收从UI界面中输入框里获取的内容
test=False                            #test用于作为检测是否可以执行thread_two()方法的条件。如果test为True则会被t3线程检测到，从而
                                      #执行thread_two()方法。为False则会不做处理。
list_var1=[]                          #list_var1
def thread_one():
        gc = ui()                     #创建UI文件里的ui类的实例对象gc
        root = ui.loading(gc)         #调用ui类的loading()方法并传入实例对象，返回得到主界面对象root
        global list_var1              #在thread_one()方法中对其声明使用全局成员列表list_var1
        text = ui.Text(gc, root)      #调用ui类的Text()方法传入实例对象gc与主界面对象root，并返回得到文本框控件对象text
        list_var1.append(text)        #将文本框控件对象text添加到列表list_var1中，方便之后使用这个对象
        ui.ButtoN(gc, root, text)     #使用ui类的ButtoN的方法(),并传入实例对象gc、主界面对象root、文本框控件对象text
        t4.start()                    #启动t4线程
        ui.show(gc, root)             #调用ui类的show()方法，并传入实例对象gc、主界面对象root


#thread_two()是用于将UI界面的输入框中的内容拿出来拼接到微博输入框url上，再对其爬取内容。
def thread_two():
    txt=list_var.pop(0)               # 弹出list_var列表里关于在输入框中获取到的内容
    list_var.clear()                  #对list_var列表进行清空操作
    print("txt2:{}".format(txt))      #打印list_var列表弹出的内容，判断是否为输入框中输入的内容
    payload={                         #payload={}这个字典存放的是用来需要拼接到url上的内容
        "q":txt,
        "wvr":"6",
        "Refer":"SWeibo_box"
             }
                                      #headers={}里是请求头的一些参数
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36',
    }
                                      #requests.get()方法是将payload这个字典拼接到url上并且对其编码，再带着请求头去对url访问爬取
    r = requests.get('https://s.weibo.com/weibo?', headers=headers,params=payload)
    print("url:{}".format(r.url))     #打印拼接好的url
    etree.HTML(r.text)                #对返回的内容进行解码
    print(r.text)                     #打印返回的内容

    tree= etree.HTML(r.text)
    P_list=tree.xpath('//div[@class="card-wrap"]/div[@class="card"]/div[@class="card-feed"]/div[@class="content"]/p[@class="txt"]')
    time = tree.xpath(
        '//div[@class="card-wrap"]/div[@class="card"]/div[@class="card-feed"]/div[@class="content"]/p[@class="from"]')

    TimeNum = 0
    print(P_list)
    for p_single in P_list:
        print("****************START***************")
        print("博主：{}".format(p_single.xpath('./@nick-name')[0]))

        tt = time[TimeNum].xpath('./a/text()')
        print("ddfdsfgasgfdfafgasd", tt, TimeNum)
        TimeNum += 1

        paragraph=[]

        for rel_p in p_single:                             #p_single为p标签对象（列表），rel_p是p标签的文本或者是其下的子类标签
            appear_b=0
            if type(rel_p) == etree._Element:                                         #判断是否为p对象下的子类标签对象（列表）
                a_object=rel_p
                for rel_a in a_object:                                                #a级对象列表遍历出b级元素
                    if type(rel_a) == etree._Element:                                 #判断是否为a对象下的子类标签对象（列表）b级对象
                        b_object=rel_a
                        print("b级对象下的文本:{}".format(b_object.xpath('./text()')))  #输出b级元素文本（a下面不是b级对象均为b级元素文本）
                        appear_b+=1
                        paragraph.append(b_object.xpath('./text()'))
                print("a级对象下的文本:{}".format(a_object.xpath('./text()')))          #输出b级元素文本（a下面不是b级对象均为b级元素文本）
                paragraph.append(a_object.xpath('./text()'))
                continue
        print("paragraph1:{}".format(paragraph))
        print("P级对象下的文本:{}".format(p_single.xpath('./text()')))
        p_text_list=p_single.xpath('./text()')
        #p_text_list列表与paragraph穿插   paragraph作为父级，p_text_list作为子级
        #第一步：判断是否有b级对象
        #第二步：含有b级对象的穿插

        #对爬取下来的数据进行处理------start------   (对数据的顺序进行重新排序，该部分不需要掌握，这里采用了两种算法，可以参考try2.py文件)
        sub = []
        sum = 0
        for x in range(len(paragraph)):
            if len(paragraph[x]) >1:
                insert_obj = paragraph[x - 1]
                sub.append(x - 1)
                paragraph[x].insert(1, insert_obj)
        while len(sub) > 0:
            sub_ject = sub.pop(0)
            paragraph.pop(sub_ject - sum)
            sum += 1

        print("paragraph2:{}".format(paragraph))
        num=1
        y = 0
        list_max = []
        list_min = []
        if len(paragraph) < len(p_text_list):
            list_max = p_text_list
            list_min = paragraph
            y = len(list_max)
        else:
            list_max = paragraph
            list_min = p_text_list
            y = len(list_max)

        for x in range(y):
            # print("x:{}".format(x))
            # print("num:{}".format(num))
            if len(list_max) - 1 < x + num:
                break
            if len(list_min)-1<x:
                break
            list_max.insert(x + num, list_min[x])
            num += 1
            # print("list1:{}".format(paragraph))
            # print("y:{}".format(y))
        print("paragraph3:{}".format(list_max))



        var=''
        for z in list_max:
            if type(z)==list:
                if len(z) == 0:
                    continue
                if len(z)>1:
                    for x in z:
                        if type(x)==list:
                            var=var+x[0]
                        else:
                            var=var+x
                else:
                    var=var+z[0]
            else:
                var=var+z
        b = var.split()
        var = "".join(b)
        print("var:{}".format(var))
        # 对爬取下来的数据进行处理------end------

        #爬取评论数，点赞数
        div_3=p_single.xpath('..')              #由于无法连续的退回上一级，所以只能单个来进行，第一次跳转
        print("div_3:{}".format(div_3[0]))
        div_2=div_3[0].xpath('..')              #第二次跳转
        print("div_2:{}".format(div_2[0]))
        div=div_2[0].xpath('..')                #第三次跳转
        print("div:{}".format(div[0]))
        ul=div[0].xpath('./div[@class="card-act"]/ul[1]')            #得到所需的etree._Element对象
        print("ul:{}".format(ul[0]))
        Collection=ul[0].xpath('./li[1]/a/text()')                   #得到所需对象下需要的文本
        forward=ul[0].xpath('./li[2]/a/text()')                      #得到所需对象下需要的文本
        comment = ul[0].xpath('./li[3]/a/text()')                    #得到所需对象下需要的文本
        good_number = ul[0].xpath('./li[4]/a/em/text()')




        #得到所需对象下需要的文本
        print("收藏:{}".format(Collection))
        print("转发:{}".format(forward))
        print("评论:{}".format(comment))
        print("点赞:{}".format(good_number))



# t3线程
#检测UI界面输入
def thread_three():
    while True:
        global test
        if test == True:
            print("zhingxinle")
            thread_two()
            test=False

        else:
            # print("test不为True")
            pass

# t4线程
def thread_four():
    text=list_var1.pop()
    while True:
        if ui.test == True:
            txt = text.get()
            list_var.append(txt)
            print("txt:{}".format(txt))
            ui.test = False
            global test
            test = True

#程序入口
if __name__ == "__main__":
    t1=threading.Thread(target=thread_one)                 #  创建t1线程用于加载UI界面
    t1.start()                                             # 启动t1线程
    # t2=threading.Thread(target=thread_two)
    t3=threading.Thread(target=thread_three)               # 创建t3线程用于检测UI界面中的输入框是否有输入
    t3.start()                                             # 启动t3线程
    t4=threading.Thread(target=thread_four)                # 创建t4线程用于循环获取UI界面输入框中的内容


#解析网页并存入excel表里
