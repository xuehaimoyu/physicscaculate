import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
import time
import sys
from docx import Document
from docx.shared import Inches
class Interpolation:
    def __init__(self,x,y,model):
        if len(x)!=len(y):
            raise ValueError("Warning! length x is not eqal to length y")
        else:
            self.X=x
            self.y=y
            self.model=int(model)
    def Polynomial(self):#多项式插值
        n=len(self.X)
        X=np.array(self.X)
        X=np.vander(X,n,increasing=True)#建立范德蒙德行列式
        y=np.array(self.y)
        temp= lambda x:0
        y=y.T
        a=np.linalg.inv(X.T@X)@X.T@y#求解系数矩阵
        a=list(a)
        global count
        count=n
        def fun(t):
            global count
            count=count-1
            if count>=0:
                return a[count]*t**count+fun(t)#使用递归作为求解函数
            else:
                count=n
                return 0
                
        return fun
    def Neville(self):#内维尔插值
        n=len(self.X)
        x=self.X
        array=np.zeros((n,n))#生成n行n列矩阵用以存储数据进行计算
        for i in range(0,n):
            array[0][i]=self.y[i]#第一行设置初始值
        def fun(t):
            for i in range(1,n):
                for j in range(0,n-i):
                    array[i][j]=1/(x[j]-x[j+i])*((t-x[j+i])*array[i-1][j]-(t-x[j])*array[i-1][j+1])#从左到右，从上到下一层一层计算
            return array[n-1][0]
        return fun
    def Rational(self):#有理函数插值
        n=len(self.X)
        x=self.X
        array=np.zeros((n,n))#生成n行n列矩阵用以存储数据进行计算
        for i in range(0,n):
            array[0][i]=self.y[i]#第一行设置初始值
        def fun(t):#python中-1代表最后一列（行），没必要单独新加入一个维度
            for i in range(1,n):
                for j in range(0,n-i):
                    array[i][j]=array[i-1][j+1]+(array[i-1][j+1]-array[i-1][j])/(((t-x[j])/(t-x[i+j]))*(1-(array[i-1][j+1]-array[i-1][j])/(array[i-1][j+1]-array[i-2][j+1]))-1)
            return array[n-1][0]
        return fun
    def solve(self):
        if self.model==0:
            return self.Polynomial()
        elif self.model==1:
            return self.Neville()
        elif self.model==2:
            return self.Rational()
        
