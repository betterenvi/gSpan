# gSpan
gSpan是一个频繁子图挖掘算法。

这个程序使用Python实现了gSpan算法。在实现时，参照了[gboost](http://www.nowozin.net/sebastian/gboost/)。

### 无向图
在[graphdata/graph.data](./graphdata/graph.data)数据上，在数次运行中，本程序和gboost的输出结果一致。

### 有向图
当前（时间：2016-10-29），gboost还不支持有向图的频繁子图挖掘。本程序实现了面向有向图的频繁子图挖掘，**但是还没有全面测试过，正确性不敢保证**。本程序的作者在[graphdata/graph.data.directed.1](./graphdata/graph.data.directed.1)和[graph.data.simple.5](./graphdata/graph.data.simple.5)两个数据集上，运行了数次，暂时还未发现错误。


### 如何运行
```
$ python main.py [-s min_support] [-n num_graph] [-l min_num_vertices] [-u max_num_vertices] [-d] [-v] [-h] [-p] [-w] database_file_name 
```

##### 一些例子

- 从./graphdata/graph.data中读取数据，挖掘支持度最少5000的频繁无向子图
```
$ python main.py -s 5000 ./graphdata/graph.data
```

- 从./graphdata/graph.data中读取数据，挖掘支持度最少5000的频繁无向子图，并将频繁子图可视化（需要安装matplotlib和networkx）
```
$ python main.py -s 5000 -p ./graphdata/graph.data
```

- 从./graphdata/graph.data中读取数据，挖掘支持度最少5000的频繁有向子图
```
$ python main.py -s 5000 -d ./graphdata/graph.data
```

- 查看帮助，输出各个参数的含义
```
$ python main.py -h
```

本程序的作者还写了基于Jupyter Notebook的[代码](./main.ipynb)，展示了程序的输出，并对图进行了可视化。详见[main.ipynb](./main.ipynb)。

## Refercence
- [论文](http://www.cs.ucsb.edu/~xyan/papers/gSpan-short.pdf)

gSpan: Graph-Based Substructure Pattern Mining, by X. Yan and J. Han. 
Proc. 2002 of Int. Conf. on Data Mining (ICDM'02). 

- [gboost](http://www.nowozin.net/sebastian/gboost/)

gSpan的一个C++实现。
