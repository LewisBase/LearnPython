# -*- coding: utf-8 -*- 
import numpy as np 
import pandas as pd 
from random import randint

abj=["狗屎般的","幸运的","苦逼的","辛苦的","自由的","一路挂科的","光辉灿烂的","无上荣光的"]
gender_male=np.array(["男","公","雄","male","boy","man","son"])
gender_female=np.array(["女","母","雌","female","girl","woman","madam"])

# information of doom mates

matesid=[randint(1000000,1009999)]
while len(matesid)<5:
    j = randint(1000000,1009999)
    if j not in matesid:
        matesid.append(j)

mates={'姓名':["王朝","马汉","张龙","赵虎"],'性别':["男","男","男","男"],
        '年龄':["18","19","17","20"]}
matealternate=pd.DataFrame({'姓名':"蔡徐坤",'性别':"不男不女",'年龄':"28"},index=[matesid[-1]])
dfdoommates=pd.DataFrame(mates,columns=["姓名","性别","年龄"],index=matesid[:-1])




def main():
    pass

if __name__ == '__mian__':
    main()


