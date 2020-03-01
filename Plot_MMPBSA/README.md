学习使用GROMACS已经很久了，但是一直停留在很初级的应用上面，对高级技巧并不了解。就连做生物体系几乎必做的MMPBSA分析都没有尝试过。乘着这个假期了解了一下MMPBSA，才知道这个计算方法不仅仅是用于蛋白质-配体体系的结合自由能计算，对于任何一个二聚体都是可以的。另外，Jerkwin老师已经发展出了比之前常用的GMXMMPBSA与g_mmpbsa两种脚本/程序更加简单易用的计算脚本——gmx_mmpbsa。gmx_mmpbsa不但没有GROMACS与APBS程序的版本要求，还可以一步运行获得所有结果，大大降低了MMPBSA的学习成本。

Jerkwin老师的[博客](https://jerkwin.github.io/2019/07/31/gmx_mmpbsa%E4%BD%BF%E7%94%A8%E8%AF%B4%E6%98%8E/)中有详尽的使用说明以及与其他两种方法计算结果的比对，另外，gmx_mmpbsa脚本的最新版本也在可以他的[github](https://github.com/Jerkwin/gmxtool/tree/master/gmx_mmpbsa)库中找到。

gmx_mmpbsa使用前需安装GRMOMACS与APBS，脚本会自动调用这两个程序进行计算。Ubuntu环境下APBS可以使用`sudo apt install apbs`直接进行安装。在修改脚本内的变量内容时，如果GROMACS与APBS都已添加进了环境变量，则可简写为：`gmx='gmx'`以及`apbs='apbs'`。

脚本运行过程中如果出现某些`awk`函数未定义的错误，那么还需要安装一下`gawk`，使用`sudo apt install gawk`即可。

计算完成后会生成一系列不同结果的文档，这里编写了一个python脚本来进行绘图，顺便复习了一下Pandas与Matplotlib的使用方法。其中有关饼状图的修饰来自于Lemonbit的[知乎专栏文章](https://zhuanlan.zhihu.com/p/26812779)。

运行后会将MMPBSA的计算结果汇总为自由能的柱形图，以及各个残基自由能贡献的线状图与饼状图。数据太多时饼状图的标签会堆叠在一起，暂时还没想到很好的处理办法，图像展示如下：

![Bar](https://raw.githubusercontent.com/LewisBase/LearnPython/master/Plot_MMPBSA/MMPBSA_Results.png)

![Plots and Pie](https://raw.githubusercontent.com/LewisBase/LearnPython/master/Plot_MMPBSA/MMPBSA_Energy_Composition.png)

### 参考资料

[gmx_mmpbsa使用说明](https://jerkwin.github.io/2019/07/31/gmx_mmpbsa%E4%BD%BF%E7%94%A8%E8%AF%B4%E6%98%8E/)

[关于matplotlib，你要的饼图在这里](https://zhuanlan.zhihu.com/p/26812779)