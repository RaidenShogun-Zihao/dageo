 # -*- coding: utf-8 -*-
"""
Created on Sun May 29 14:14:23 2022

@author: Zihao
"""
#warning, start should be adjusted and also the total line number
#depends on the result file format
#The X1-X2 division number should also be adjusted
import numpy as np
import os

def result(fileadress):
    os.chdir(fileadress)
    f = open("2dtrac.HIST02")
    lines = f.readlines()
    f.close()
    start=19
    step=int((len(lines)-start)/6)

    data2=np.empty(step)
    data3=np.empty(step)
    data4=np.empty(step)

    for i in range(0,step):
        temp=lines[start+5].split(",")
        data2[i]=temp[0]
        start+=6
    f = open("2dtrac.HIST03")
    lines = f.readlines()
    f.close()
    start=19
    for i in range(0, step):
        temp = lines[start + 5].split(",")
        data3[i] = temp[0]
        start += 6
    f = open("2dtrac.HIST04")
    lines = f.readlines()
    f.close()
    start=19
    for i in range(0, step):
        temp = lines[start + 5].split(",")
        data4[i] = temp[0]
        start += 6

    #data=np.hstack((data2,data3,data4))
    data=data3
    return data


if __name__ == "__main__":
     file_loc = r"D:\IWTT\sample"
     UTCHEMresult=result(file_loc)








