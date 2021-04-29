from tkinter import *


class ui(object):
    test = False
    txt = ''

    def loading(self):
        root = Tk()
        root.title("微博爬取器")
        root.geometry("600x400")
        # 创建文本框
        return root

    def Text(self, root):
        text = Entry(root, bd=0)
        text.place(x=200, y=180, width=175, height=40)
        return text

    # 第一种方法
    # @staticmethod
    # def fuc(text):
    #     # 获取用户输入
    #     txt = text.get()
    #     print(txt)

    # 第二种方法
    def fuc(self, text):
        # 获取用户输入
        # ui.txt = text.get()
        print("执行了")

        ui.test = True

    # 创建搜索按钮
    def ButtoN(self, root, text):
        button = Button(root, command=lambda: ui.fuc(self, text))
        button.place(x=390, y=180, width=40, height=40)

    def show(self, root):
        root.mainloop()
