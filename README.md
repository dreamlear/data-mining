# data-mining
Some data mining algorithms and a data mining project.

## Contents
* [Algorithms](#algorithms)
    * [Apriori Algorithm](#apriori-algorithm)
* [Project](#project)

## Algorithms
Descriptions for these algorithms.
### Apriori Algorithm
#### The main idea:
    
    1.Set a minimum support as threshold.
    2.Scan the data table once to get all frequent itemsets of length l=1. 
      (Frequent Itemset: An itemset whose support is greater than or equal to a minimum support threshold)
    3.Repeat until there is no frequent itemsets of length l:
        a)Generate itemsets of length l+1 from the frequent itemsets of length l.
        b)Prune the new itemsets containing the subsets of lenngth l that are not frequent.
        c)Count the support for the new itemsets by scanning the data table.
        d)Prune the new itemsets that are not frequent by using the threshold.
        e)Let length l = l + 1. 
        
#### Advantages & Disadvantages
- Advantages:
- Disadvantages:
        
#### Implements


## Project
A project for data mining.

### Data
There are two data sets, one is data of Mobike from Mobike Big Data Challenge 2017, the other is data of Divvy bike data .

### To Do
The job is to predict the field to_station_id(predict destinations of bike share data).

### Task
#### Task 1 - Data Preprocessing and Statistics

#### Task 2 - Data Clustering

#### Task 3 - Simple Data Visualization

#### Task 4 - Frequent Pattern Mining 

#### Task 5 - Prediction

### Result