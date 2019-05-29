### 题记

该项目是对刘老师的polymerDFT程序输出文件进行处理时衍生的python练习项目。最初的目的只是完成对densmap数据的作图，后来因为有师弟需要根据densmap求取团簇的表面积，就顺便将程序完善了一下，把两个功能放置在一起。

师弟的输出数据源自TDDFT程序，输出的density数据上具有帧标签。所以就将每帧视为一个对象，建立了一个具有绘图，计算表面积等几种方法的类型。

在表面积的计算中，由于图形是完全轴对称的，便取了四分之一的边界曲线。在极坐标下积分求得，积分方程为：
$SurfaceArea=2\pi\int_a^bf(x)\sqrt{1+f'(x)^2}dx$。最终的表面积应当再乘以2。

简便起见，获取图形边界时采用了插值方法，计算过程的求导与积分直接对两个数组用数值的方法求得。

### 说明

该程序使用到了numpy，matplotlib，scipy模块，如为安装请先安装这些模块：
    pip install numpy,matplotlib,scipy

example.py文件为一个实例。

`ReadDenFile(filename,type='multi')`函数用于读取文件数据，并对每一帧构建一个DensityFrame对象。传入文件名与类型，默认为多帧密度文件。如果需要读入单帧文件，设置type为single。

`TransformData(X,Y,DENSITY)`函数用于转换数据类型，将一维的X，Y，DENSITY转换为二维距阵，方便作图。内置在`ReadDenFile()`中使用。

`DensityFrame`类用于构建密度帧的对象
* `__init__(self,X,Y,DENSITY,TIME=0.0)`构造函数，传入X，Y，DENSITY与时间TIME，配合`ReadDenFile()`进行构建；
* `DensMap(self,bar='bar',savepicture='no')`colormap彩图绘制函数，设置bar为任意其他字符则不显示colorbar，设置savepicture为其他字符则保存以该字符为名称的图片；
* `HighcontrastDensmap(self,bar='nobar',savepicture='no')`高对比度黑白图绘制函数，设置bar为'bar'则显示colorbar，设置savepicture为其他字符则保存以该字符为名称的图片；
* `SurfaceArea(self)`表面积计算函数，计算团簇的表面积并输出；

`Der(X,Y)`函数用于计算Y的导数，输入为两个同长度的数组。

`Int(X,Y)`函数用于计算Y-Ymin在X区间内的积分，输入为两个同长度的数组。

`Surface(X,Y)`函数计算对称曲面的表面积，输入为两个同长度的数组。

### 更新

#### 2019.05.29

更新了对边界的拟合方法，用numpy的polyfit()函数对边界进行了多项式拟合。
