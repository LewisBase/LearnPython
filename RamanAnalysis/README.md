### 题记

一个处理皮肤拉曼数据的小程序，借用模型$S=\alpha_a S_a+\alpha_b S_b+B_0+B_1\Lambda+B_2\Lambda^2+B_3\Lambda^3+B_4\Lambda^4+B_5\Lambda^5$使用最小二乘法拟合得到不同组分对总拉曼谱的贡献$\alpha_a,\alpha_b$。

对原始数据首先进行了到[0,1]范围内的归一化，采用$\frac{y-y_{min}}{y_{max}-y_{min}}$的方法

为保证各个数据的数组长度统一，对原始数据进行了`interpolate.interp1d`的插值方法将数组长度统一为1000

进行最小二乘法计算，得到最终结果