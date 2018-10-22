

# 資料探勘 -- Project1 Report

* 實作 Apriori 和 FP-growth 兩種方法來挑出 Best Rules
* Dataset 使用 Kaggle dataset 和 IBM quest data
* 建立 Dataset 的 arff檔
* 將結果與 SPMF ( an open-source data  mining library ) 作比較

## 目錄

* [Dataset](#Dataset)
* [Setup](#Setup)
* [Run Process](#Run-Process)
    * [Apriori](#Apriori)
    * [FP-growth](#FP-growth)
    * [產生 Kaggle dataset 的 arff 檔](#產生-Kaggle-dataset-的-arff-檔)
* [比較＆結論：](#比較＆結論：)
    * [[比較1] 在同個演算法下](#[比較1]-在同個演算法下h)
    * [[比較2] 在同個 dataSet 下](#[比較2]-在同個-dataSet-下)
    * [[比較3] 在不同min_support / confidence下](#[比較3]-在不-min_support-/-confidence下)

## Dataset
#### Kaggle dataset: [mushrooms](https://www.kaggle.com/uciml/mushroom-classification)
```
data/mushrooms.csv  
```

####  IBM quest data:
```
data/pat.ntrans_5.tlen_10.nitems_0.02
```

## Setup

#### 語言 : python3
#### 需安裝套件: liac-arff
```
 pip install liac-arff
```

## Run Process
### Apriori: 
```
python3 apriori.py [data_type] [min_support] [min_confidence]
```
* [data_type] = 0 --> 使用 Kaggle dataset
    [data_type] = 1 --> 使用 IBM quest data
* [min_support] 和 [min_confidence] 的值都介於0~1

#### 執行結果：
1. 使用自己的演算法套用在kaggle dataset

    ![](https://i.imgur.com/JtW9bZM.png)


2. 使用spmf，套用在kaggle dataset

    ![](https://i.imgur.com/hYVoOCe.png)

3. 使用spmf，套用在IBM dataset 

    ![](https://i.imgur.com/GkpXYJw.png)


---

### FP-growth: 
```
python3 fp_growth.py [data_type] [min_support] [min_confidence]
```
* [data_type] = 0 --> 使用 Kaggle dataset
    [data_type] = 1 --> 使用 IBM quest data
* [min_support] 和 [min_confidence] 的值都介於0~1

#### 執行結果：

1. 使用自己的演算法套用在kaggle dataset (fp-growth)

    ![](https://i.imgur.com/d1WbHso.png)

2. 使用spmf，套用在kaggle dataset

    ![](https://i.imgur.com/thlvB9b.png)

3. 使用spmf，套用在IBM dataset (fp-growth)

    ![](https://i.imgur.com/FkwpN9V.png)


---
### 產生 Kaggle dataset 的 arff 檔:
```
python3 mushroom_to_arff.py
```

## 比較＆結論：




|m=0.95 c=0.9| Apriori (spmf) | Apriori (自己) | FP-Growth (spmf)|FP-Growth (自己) |
| -------- | -------- | -------- | -------- | -------- |
| Kaggle    | 0.02s    |  0.38s  | 0.06s |   0.23s |
| IBM   |   0.01s    | 0.10s         |  0.01s  |  0.11s  |

|m=0.1 c=0.3| Apriori (spmf) | Apriori (自己) | FP-Growth (spmf)|FP-Growth (自己) |
| -------- | -------- | -------- | -------- | -------- |
| Kaggle    | 10min		  | 	> 1hr  | 6min |   > 1hr |
| IBM   |   0.1s    | 0.23s         |  0.01s  |  > 1hr  |

### [比較1] 在同個演算法下
* 在同個演算法之下，不論是 Apriori 還是 FP-Growth ，都可以看出IBM的資料會比 Kaggle 來的快，我想這應該是因為:
    1. IBM有3600多筆data，並且平均transactions長度只有10，而kaggle則有8000多筆的資料，以及長度為23的transaction。
    2. IBM的資料分布比較稀疏，比較不會有長度較長的frequent itemSet，所以在這塊IBM的資料刪減的會比較快。

### [比較2] 在同個 dataSet 下
* 除了很明顯地可以看出由套件跑出的速度會比我自己所寫的來的快以外，還可以看出，在 min_support 以及 confidence 高的時候，fp-growth 並不會比 Apriori 來的快，但是在資料是稀疏以及min_support 小的時候，fp-growth 的效率會比Apriori高上許多。

### [比較3] 在不同min_support / confidence下
* 可以看出在 IBM 的資料下所花得時間其實不會差太多，但在 kaggle 的資料就會差上許多，我想這是同樣是因為IBM的資料是稀疏的，刪減後所保留的 dataSet 會下降得很快，而 kaggle 的則相反，由於 min_support太低，刪減後大多數的 itemSet 會繼續保留下來，因此整個時間大幅度的上升。
