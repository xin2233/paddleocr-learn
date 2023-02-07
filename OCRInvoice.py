#!/usr/bin/env python
# coding: utf-8

# In[18]:


import sys 
sys.path.append('/home/aistudio/external-libraries')
from paddleocr import PaddleOCR
import re
from PIL import Image

class OCRInvoice:
    def __init__(self):
        self.HorL='快速'

    def LowOrHigh(self):
        if self.HorL=='快速':
            self.ActOCR = PaddleOCR()
        else:
            self.ActOCR = PaddleOCR(use_angle_cls=True, lang="ch",rec_model_dir='./Models/rec',cls_model_dir='./Models/cls',det_model_dir='./Models/det')
    def RunOCR(self,path):
        result = self.ActOCR.ocr(path, cls=True)
        inform = []
        for line in result:
            inform.append(line[1][0])

        String2 = '【' + '】【'.join(inform) + '】'
        print("a:",String2)

        if '发' in String2 or '票' in String2:
            print('Success!')
        else:
            print('no')
            # image = cv2.imread(path)
            # print(image)
            # rotated = imutils.rotate(image, 180)
            # cv2.imwrite(path, rotated)
            im = Image.open(path)
            out = im.transpose(Image.ROTATE_180)
            out.save(path)
            result = self.ActOCR.ocr(path)
            inform = []
            for line in result:
                inform.append(line[1][0])

            String2 = '【' + '】【'.join(inform) + '】'



        #发票号码
        try:
            self.number = re.findall('【(发票号码：[0-9]{8})】', String2)[0]
        except:
            self.number=''

        # 将所有的字母（大小写）都替换为空。即删除。
        # invoice2 = re.sub('[a-zA-Z]', '', String2)
        # print("b:",invoice2)

        #发票代码
        try:
            self.daima = re.findall('【(发票代码：[\d]*)】', String2)[0]
        except:
            self.daima = ''

        #发票日期
        '''
        # 目前废弃，已编写新的code
        try:
            # .*?：
            # . 表示除\n 的所有字符，
            # * 表示0次或n次，
            # ?跟在*或者+后边用时，表示懒惰模式。也称非贪婪模式。就是匹配尽可能少的字符。
            patter = '([0-9]*[年|月|日].*?)】'
            dateo = re.findall(patter, String2)[0]
            print(dateo)
            year = ''.join(re.findall('(2019)|(2020)|(2021)|(2022)|(2023)|(2024)', dateo)[0])
            print(year)
            month = ''.join(re.findall('(01)|(02)|(03)|(04)|(05)|(06)|(07)|(08)|(09)|(10)|(11)|(12)', dateo)[1])
            date = dateo[-3:-1]
            self.ymd = year + month + date
        except:
            self.ymd =''
        '''
        # by zjx
        try:
            # .*?：
            # . 表示除\n 的所有字符，
            # * 表示0次或n次，
            # ?跟在*或者+后边用时，表示懒惰模式。也称非贪婪模式。就是匹配尽可能少的字符。
            patter = '【(开票日期：[0-9]*[年|月|日].*?)】'
            dateo = re.findall(patter, String2)[0]
            print(dateo)
            year = ''.join(re.findall('(2019)|(2020)|(2021)|(2022)|(2023)|(2024)', dateo)[0])
            # print(year)
            month = ''.join(re.findall('(01)|(02)|(03)|(04)|(05)|(06)|(07)|(08)|(09)|(10)|(11)|(12)', dateo)[1])
            date = dateo[-3:-1]
            self.ymd = year + month + date
        except:
            self.ymd =''

        #发票金额
        try:
            amounts = re.findall('(￥[0-9]*.*?)', String2)[0]
            # print("b:",amounts)
            # amounts =  amounts.replace(" ", "")
            # print()
            amounts = re.findall('([0-9]*.*?)', amounts)
            # print("c:",amounts)
            for p in amounts:
                if p.isdigit():
                    # print('3')
                    self.amount = p
                    break
                else:
                    # print('4')
                    self.amount = ''
                # print('p:',p)
            # amounts 是list
            # self.amount = amounts
        except:
            self.amount = ''

        self.OneInv = [path,self.daima, self.number, self.ymd, self.amount]
        print(self.OneInv)
        return self.OneInv


# In[19]:


if __name__ == '__main__':
    ocrAct = OCRInvoice()
    Invoicepath = './IMG/200/images_0.png'
    ocrAct.HorL=''
    ocrAct.LowOrHigh()
    ocrAct.RunOCR(Invoicepath)


# In[3]:


try:   
    get_ipython().system('jupyter nbconvert --to python file_name.ipynb')
    # python即转化为.py，script即转化为.html
    # file_name.ipynb即当前module的文件名
except:
    pass

