import pandas as pd
import jieba.posseg as pseg
import matplotlib.pyplot as plt
import os
import re
from collections import defaultdict

scraped_censored = pd.read_csv('/Users/Kei/OneDrive/revised_data/scrapped_all_censored.csv', usecols=['content'])
scraped_uncensored = pd.read_csv('/Users/Kei/OneDrive/revised_data/scraped_sample_uncensored_content.csv', usecols=['content'])
jed_censored = pd.read_csv('/Users/Kei/OneDrive/jed_data/jed_censored_content_topics.csv', usecols=['content'])
jed_uncensored = pd.read_csv('/Users/Kei/OneDrive/jed_data/jed_sample_uncensored_content_topics.csv', usecols=['content'])
df_list = {'scraped censored': scraped_censored, 'scraped uncensored': scraped_uncensored, 'jed censored': jed_censored, 'jed uncensored': jed_uncensored}

sem_dict_path = '/Users/Kei/OneDrive/censorship-research/semantics/sem_dict.txt'

verbs_dict = {}
verbs_category = ["F", "G", "H", "I", "J"]

def create_verbs_dict():
    with open(sem_dict_path, encoding="utf-8") as source:
        for line in source:
            line = line.split()
            if (line[0][0] in verbs_category):
                if (not line[0][:2] in verbs_dict.keys()):
                    verbs_dict[line[0][:2]] = []
                verbs_dict[line[0][:2]] = verbs_dict[line[0][:2]] + line[1:]

    return verbs_dict

verbs_dict = create_verbs_dict()


def extract_verbs_from_df(df):
    verbs_per_row = []
    all_verbs = []
    no_of_words = 0
    temp = []

    for index, data in df.iterrows():
        tagged_data = pseg.cut(data['content'])
        for word, flag in tagged_data:
            if flag is not 'x':
                no_of_words += 1
            if flag is 'v':
                temp.append(word)
                all_verbs.append(word)
        verbs_per_row.append(temp)
        temp = []
    print("no. of instances: {}".format(len(verbs_per_row)))

    no_of_verbs = len(all_verbs)
    print("no. of words: {}".format(no_of_words))
    print("no. of verbs: {}".format(no_of_verbs))
    
    return verbs_per_row, all_verbs, no_of_verbs, no_of_words


def extract_verb_category(all_verbs, df_name):
    verb_categories = []
    for key, values in verbs_dict.items():
        for value in values:
            for verb in all_verbs:
                if verb == value:
                    verb_categories.append((key, value))

    with open('{}_verbs_categories.txt'.format(df_name), 'w', encoding='utf-8') as output:
        for v in verb_categories:
            output.write(str(v))
            output.write('\n')
    return verb_categories



def generate_freq_dist(verb_categories):
    freq_dist = {}
    for item in verb_categories:
        if item[0] not in freq_dist.keys():
            freq_dist[item[0]] = 1
        else:
            freq_dist[item[0]] += 1
    return freq_dist

def get_percent_dist(freq_dist, df):
    percent_dist = {}
    verbs_total = 0
    for value in freq_dist.values():
        verbs_total += value
    for key, value in freq_dist.items():
        value = round((value / verbs_total) * 100, 2)
        percent_dist[key] = value
    print("total no. of verbs across sbucat: {}".format(verbs_total))
    print(percent_dist)
    return percent_dist

def generate_graph(percent_dist, df_name):
    plt.plot(percent_dist.keys(), percent_dist.values())



    # plt.bar(percent_dist.keys(), percent_dist.values())
    # plt.xlabel('categories')
    # plt.ylabel('percentage')
    # plt.title(df_name)
    # plt.show()

count = 0
for df_name, df in df_list.items():
    verbs_per_row, all_verbs, no_of_verbs, no_of_words = extract_verbs_from_df(df)
    verb_categories = extract_verb_category(all_verbs, df_name)
    freq_dist = generate_freq_dist(verb_categories)
    percent_dist = get_percent_dist(freq_dist, df)
    generate_graph(percent_dist, df_name)
    # break


    print("{} finished".format(df_name))

plt.legend(list(df_list.keys()), loc='upper left')
plt.xlabel('categories')
plt.ylabel('percentage')
plt.show()