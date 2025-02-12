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
def result():
    f=open("5-SPOT.OVERAL")
    lines=f.readlines()
    f.close()
    start=16

    step=int((len(lines)-start)/6)
    data=np.zeros([step,5])
    result={}

    accum=0
    for i in range(0,step):

        temp=lines[start].split(",")
        data[i,0]= float(temp[1])  #days
        data[i,1] = float(temp[4]) #Cumoil
        temp=lines[start+1].split(",")
        data[i,4]=float(temp[3])


        temp = lines[start+3].split(",")
        data[i,3] = float(temp[1])  #Oil Cut


        if i ==0:
            data[i, 2] = data[i, 1]
        else:
            accum =  (data[i,1]-data[i-1,1])/(1.05**(data[i,0]//365))+accum #discounted
            data[i,2]=accum

        start+=6

    result['OVERAL'] =data







    return result


if __name__ == "__main__":
     file_loc = r"D:\hotpolymerOptimization\99"
     os.chdir(file_loc)
     UTCHEMresult=result()








