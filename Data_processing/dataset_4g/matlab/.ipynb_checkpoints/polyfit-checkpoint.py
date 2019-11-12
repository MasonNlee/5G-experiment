import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
from pandas import DataFrame
import pandas as pd
from scipy.stats import norm
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn import linear_model

with open('rate.txt', 'r') as f:
    file_context = f.read()
    item = file_context.split(" ")
y = np.array(item, dtype = float)

with open('csq_grid.txt','r') as f2:
    file_context2 = f2.read()
    item2 = file_context2.split(" ")
x = np.array(item2, dtype = float)

s1=pd.Series(x)
s2=pd.Series(y)
df=pd.DataFrame({"rate":s2,"csq":s1})
df = df.sort_values(by = 'csq',axis = 0,ascending = True)
x=df['csq'].values
y = df['rate'].values

''' 数据生成 '''
# x = np.arange(0, 1, 0.002)
# y = norm.rvs(0, size=500, scale=0.1)
# y = y + x**2

# x = np.array([-80.26553270449976, -82.99856983950421, -84.35407022693914,-82.0875160875161, -82.08664029603165, -78.94028172739898,-74.15506468362229, -73.1912049593181, -76.00496004408929, -83.85266136801542, -80.53025553843702,-81.33855722410901,-78.66545266927676, -75.71690669526582,-70.99150620541789,-67.09737964022044,-70.06941904015329, -75.22512368031825, -78.57584675477554, -79.48196232252361, -76.08182562051095, -74.18004974807067, -71.9403856599674, -67.71405930132735,-60.873951080164254])
# y = np.array([0.027833616823875057, 0.03178134435086604, 0.045162018742237776, 0.13942513942513943, 0.11483986219216537, 0.11242642682362278, 0.07040394262078677, 0.04520211804210254, 0.02361925756800378, 0.006021194605009634,0.058439143600913776, 0.03682638405826752, 0.024279947798112236, 0.019151218017465912, 0.016492805013812725, 0.0, 0.008710042679209128, 0.010200438618860611, 0.02140296431055701, 0.06629467985194189,0.06364214928629876,0.04464570444543657, 0.006789788158609451,0.0,0.008926977325477592])
''' 均方误差根 '''
def rmse(y_test, y):
    return sp.sqrt(sp.mean((y_test - y) ** 2))
 
''' 与均值相比的优秀程度，介于[0~1]。0表示不如均值。1表示完美预测.这个版本的实现是参考scikit-learn官网文档  '''
def R2(y_test, y_true):
    return 1 - ((y_test - y_true)**2).sum() / ((y_true - y_true.mean())**2).sum()
 
 
''' 这是Conway&White《机器学习使用案例解析》里的版本 '''
def R22(y_test, y_true):
    y_mean = np.array(y_true)
    y_mean[:] = y_mean.mean()
    return 1 - rmse(y_test, y_true) / rmse(y_mean, y_true)
 
 
plt.scatter(x, y,s=5,c='r')
degree = [1]
y_test = []
y_test = np.array(y_test)
 
 
for d in degree:
    clf = Pipeline([('poly', PolynomialFeatures(degree=d)),
                    ('linear', linear_model.Ridge ())])
    clf.fit(x[:400, np.newaxis], y[:400])
    y_test = clf.predict(x[:, np.newaxis])
 
    print(clf.named_steps['linear'].coef_)
    print('rmse=%.2f, R2=%.2f, R22=%.2f, clf.score=%.2f' %
      (rmse(y_test, y),
       R2(y_test, y),
       R22(y_test, y),
       clf.score(x[:, np.newaxis], y)))    
    
    plt.plot(x, y_test, linewidth=2.5)
    
# plt.legend(['3'], loc='upper left')
plt.rcParams['figure.figsize'] = (11.0, 4.0)
plt.ylim((-0.005, 0.12))
plt.xlabel('RSRP(dBm)')
plt.ylabel('PLR(%)')
plt.text(-70,0.08,r'$\left|\rho\right| = 0.5$',fontsize=18)
plt.savefig("polyfit.pdf")
plt.show()