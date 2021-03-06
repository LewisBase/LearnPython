### 题记

一个处理皮肤拉曼数据的小程序，借用模型$S=\alpha_a S_a+\alpha_b S_b+B_0+B_1\Lambda+B_2\Lambda^2+B_3\Lambda^3+B_4\Lambda^4+B_5\Lambda^5$使用最小二乘法拟合得到不同组分对总拉曼谱的贡献$\alpha_a,\alpha_b$。

对原始数据首先进行了到[0,1]范围内的归一化，采用$\frac{y-y_{min}}{y_{max}-y_{min}}$的方法

为保证各个数据的数组长度统一，对原始数据进行了`interpolate.interp1d`的插值方法将数组长度统一为1000

进行最小二乘法计算，得到最终结果

### 更新

2019.06.18

优化了计算方法，支持三元组合体系的计算。增加了版本号与说明选项(--option, --help)，文件输入顺序改为先输入综合拉曼数据，再输入单组份的拉曼数据。

2019.06.20

将拟合方程中的组分系数固定为正值，增加了对原始数据的平均与平滑处理，支持了四元体系的计算。文件输入不再需要后缀名，对于需要求平均值的分谱数据应以xxx-1.txt,xxx-2.txt,xxx-3.txt的形式命名，输入xxx即可。总谱数据不需要平均处理，省略后缀输入即可。

例：

    python Raman.py 2sample-30min-6um1 2skin-0um yao 1-kongbairuye

2019.07.08

新增了一个批量处理数据的程序Autorun.py，实现了简单的手动输入文件名自动计算并制表的功能。