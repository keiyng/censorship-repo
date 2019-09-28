# censorship-repo

## jed_data
Zhu et al's data. The files and directories names describe the what features and info expected to be found in the file. 

## revised_data
All data obtained by web scrpaing. The files and directories names describe the what features and info expected to be found in the file. 
Files with "sample" in the file name indicates uncensored data that are randomly sampled to match the number of censored data

## surveys
batch_*.txt - the content of surveys used to obtain human baseline, in batches.
batch*_classes.csv - each question of surveys lined up with its ground truth class, topic etc.
batch*_class_cc.csv - each question of surveys lined up with its average controvery and cap scores.

## semantics
chinese_thesaurus - the chinese thesauraus reference for etracting sematic classes.
classes - the english description of each semantic class
Other chinese resources that description the thesaurus 

## LIWC
Contains glossory of LIWC categories and the LIWC built-in simplified/traditional Chinese dictionaries

## sentiment-analysis
Contains the BaiduAI package and scripts used to run sentiment analysis

## word2vec
word2vec.py - the script used to generate word2vec data

## frequency
The character list and word list used to obtain character and word frequncies 

## python_scripts
Contains all the Python scripts that have been used to preprocess, extract, and manipulate data.