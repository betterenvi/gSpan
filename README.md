# <div align = center>gSpan</div>

##### For Chinese readme, please go to [README-Chinese](https://github.com/betterenvi/gSpan/blob/master/README-Chinese.md). 

**gSpan** is an algorithm for mining frequent subgraphs.

This program implements gSpan with Python. The repository on GitHub is [https://github.com/betterenvi/gSpan](https://github.com/betterenvi/gSpan). This implementation borrows some ideas from [gboost](http://www.nowozin.net/sebastian/gboost/).

### Undirected Graphs
This program supports undirected graphs, and produces same results with gboost on the dataset [graphdata/graph.data](https://github.com/betterenvi/gSpan/blob/master/graphdata/graph.data). 

### Directed Graphs
So far(date: 2016-10-29), gboost does not support directed graphs. This program implements gSpan for directed graphs. More specific, this program can mine frequent directed subgraph that has at least one node that can reach other nodes in the subgraph. But correctness is not guaranteed since the author did not do enough testing. After running several times on datasets [graphdata/graph.data.directed.1](https://github.com/betterenvi/gSpan/blob/master/graphdata/graph.data.directed.1) and [graph.data.simple.5](https://github.com/betterenvi/gSpan/blob/master/graphdata/graph.data.simple.5), there is no fault.

### How to install

This program supports both **Python 2** and **Python 3**.

##### Method 1

Install this project using pip:
```sh
pip install gspan-mining
```

##### Method 2

First, clone the project:

```sh
git clone https://github.com/betterenvi/gSpan.git
cd gSpan
```

You can ***optionally*** install this project as a third-party library so that you can run it under ***any*** path.

```sh
python setup.py install
```

### How to run

The command is:

```sh
python -m gspan_mining [-s min_support] [-n num_graph] [-l min_num_vertices] [-u max_num_vertices] [-d True/False] [-v True/False] [-p True/False] [-w True/False] [-h] database_file_name 
```


##### Some examples

- Read graph data from ./graphdata/graph.data, and mine undirected subgraphs given min support is 5000
```
python -m gspan_mining -s 5000 ./graphdata/graph.data
```

- Read graph data from ./graphdata/graph.data, mine undirected subgraphs given min support is 5000, and visualize these frequent subgraphs(matplotlib and networkx are required)
```
python -m gspan_mining -s 5000 -p True ./graphdata/graph.data
```

- Read graph data from ./graphdata/graph.data, and mine directed subgraphs given min support is 5000
```
python -m gspan_mining -s 5000 -d True ./graphdata/graph.data
```

- Print help info
```
python -m gspan_mining -h
```

The author also wrote [example code](https://github.com/betterenvi/gSpan/blob/master/main.ipynb) using Jupyter Notebook. Mining results and visualizations are presented. For detail, please refer to [main.ipynb](https://github.com/betterenvi/gSpan/blob/master/main.ipynb).

### Running time

- Environment
    + OS: Windows 10
    + Python version: Python 2.7.12
    + Processor: Intel(R) Core(TM) i7-4790 CPU @ 3.60GHz 3.60 GHz
    + Ram: 8.00 GB


- Running time
On the dataset [./graphdata/graph.data](https://github.com/betterenvi/gSpan/blob/master/graphdata/graph.data), running time is listed below:


| Min support | Number of frequent subgraphs | Time |
| --- | --- | --- |
| 5000 | 26 | 51.48 s |
| 3000 | 52 | 69.07 s |
| 1000 | 455 | 3 m 49 s |
| 600 | 1235 | 7 m 29 s |
| 400 | 2710 | 12 m 53 s |



### Reference
- [Paper](http://www.cs.ucsb.edu/~xyan/papers/gSpan-short.pdf)

gSpan: Graph-Based Substructure Pattern Mining, by X. Yan and J. Han. 
Proc. 2002 of Int. Conf. on Data Mining (ICDM'02). 

- [gboost](http://www.nowozin.net/sebastian/gboost/)

One C++ implementation of gSpan.
