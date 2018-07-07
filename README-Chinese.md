# <div align = center>gSpan</div>

gSpan是一个频繁子图挖掘算法。

这个程序使用Python实现了gSpan算法，项目的GitHub地址为[https://github.com/betterenvi/gSpan](https://github.com/betterenvi/gSpan)。在实现时，参照了[gboost](http://www.nowozin.net/sebastian/gboost/)。

### 无向图频繁子图挖掘
在[graphdata/graph.data](https://github.com/betterenvi/gSpan/blob/master/graphdata/graph.data)数据上，在数次运行中，这个程序和gboost的输出结果一致。

### 有向图频繁子图挖掘
当前（时间：2016-10-29），gboost还不支持有向图的频繁子图挖掘。这个程序实现了面向有向图的频繁子图挖掘，可以挖掘那些至少有一个点能够到达其他任一点的频繁子图，**但是还没有全面测试过，正确性不敢保证**。程序的作者在[graphdata/graph.data.directed.1](https://github.com/betterenvi/gSpan/blob/master/graphdata/graph.data.directed.1)和[graph.data.simple.5](https://github.com/betterenvi/gSpan/blob/master/graphdata/graph.data.simple.5)两个数据集上，运行了数次，暂时还未发现错误。

### 如何安装

这个程序是支持**Python 2**和**Python 3**。

##### 方法 1
使用pip安装：
```sh
pip install gspan-mining
```

##### 方法 2
首先，克隆项目：
```sh
git clone https://github.com/betterenvi/gSpan.git
cd gSpan
```
你也可以选择安装这个项目，这样就可以在任意一个路径下运行：
```sh
python setup.py install
```


### 如何运行

命令：
```sh
python -m gspan_mining [-s min_support] [-n num_graph] [-l min_num_vertices] [-u max_num_vertices] [-d True/False] [-v True/False] [-p True/False] [-w True/False] [-h] database_file_name 
```

##### 一些例子

- 从./graphdata/graph.data中读取数据，挖掘支持度最少5000的频繁无向子图
```sh
python -m gspan_mining -s 5000 ./graphdata/graph.data
```

- 从./graphdata/graph.data中读取数据，挖掘支持度最少5000的频繁无向子图，并将频繁子图可视化（需要安装matplotlib和networkx）
```sh
python -m gspan_mining -s 5000 -p True ./graphdata/graph.data
```

- 从./graphdata/graph.data中读取数据，挖掘支持度最少5000的频繁有向子图
```sh
python -m gspan_mining -s 5000 -d True ./graphdata/graph.data
```

- 查看帮助，输出各个参数的含义
```sh
python -m gspan_mining -h
```

本程序的作者还写了基于Jupyter Notebook的[代码](https://github.com/betterenvi/gSpan/blob/master/main.ipynb)，展示了程序的输出，并对图进行了可视化。详见[main.ipynb](https://github.com/betterenvi/gSpan/blob/master/main.ipynb)。

### 运行时间

- 测试环境
    + 操作系统： Windows 10
    + Python版本： Python 2.7.12
    + 处理器： Intel(R) Core(TM) i7-4790 CPU @ 3.60GHz 3.60 GHz
    + 内存Ram: 8.00 GB


- 程序运行时间
在[./graphdata/graph.data](https://github.com/betterenvi/gSpan/blob/master/graphdata/graph.data)数据上，运行时间如下


| 最小支持度 | 频繁子图个数 | 时间 |
| --- | --- | --- |
| 5000 | 26 | 51.48 s |
| 3000 | 52 | 69.07 s |
| 1000 | 455 | 3 m 49 s |
| 600 | 1235 | 7 m 29 s |
| 400 | 2710 | 12 m 53 s |



### Reference
- [论文](http://www.cs.ucsb.edu/~xyan/papers/gSpan-short.pdf)

gSpan: Graph-Based Substructure Pattern Mining, by X. Yan and J. Han. 
Proc. 2002 of Int. Conf. on Data Mining (ICDM'02). 

- [gboost](http://www.nowozin.net/sebastian/gboost/)

gSpan的一个C++实现。
