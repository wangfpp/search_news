# -*- coding: utf-8 -*-
# @Author: wangfpp 
# @Date: 2018-05-31 17:39:18 
# @Last Modified by:   wangfpp 
# @Last Modified time: 2018-05-31 17:39:18 
import os
#产生文件列表文件
os.system("find /home/wang/nas/ocr/OCR_samples/downloadppt/ -name '*.rar' >> ./file_list.txt")
#读取file_list 然后解压
with open('./file_list.txt') as f:
    files = f.read().split('\n')
    for item in files:
        if item:
            new_path = os.path.split(item)[0]+'/'
            cmd = 'unrar  x {} -o -y {}'.format(item,new_path)
            print cmd
            os.system(cmd)