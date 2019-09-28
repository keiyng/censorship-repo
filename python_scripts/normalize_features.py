import os
import re
import pandas as pd
import numpy as np
import file_location

def compute_zscores(directory):
    # non_features = ['content', 'topic', 'class']
    non_features = ['Path', 'File_Name', 'class', 'class_num']

    for f in os.listdir(os.fsencode(directory)):
        if f.endswith(b'.csv') and b'normalized' in f and b'censored' in f:
            file_name = f.decode('utf-8')
            df = pd.read_csv(directory + '/' + file_name)
            print(df.shape)
            df_features = pd.DataFrame()

            cols = list(df.columns)

            for non_feature in non_features:
                cols.remove(non_feature)

            for col in cols:
                col_z =  col + '_z'
                df_features[col_z] = (df[col] - df[col].mean()) / df[col].std(ddof=0)

            for non_feature in non_features:
                df_features[non_feature] = df[non_feature]
           
            df_features.drop(columns=['Paragraphs_z', 'SVM readability prediction 2.0_z', 'Path'], inplace=True)

            print(df_features.shape)
            print(df_features.columns.values)

            df_features.to_csv(directory + '/' + file_name.replace('normalized', 'standardized'), index=False)
compute_zscores('/Users/Kei/Desktop/old/csv')


# df_cen = pd.read_csv(file_location.features + '/scrapped_all_censored.csv')
# df_uncen = pd.read_csv(file_location.features + '/scrapped_all_uncensored.csv')
# print(df_cen.describe())
# print(df_cen.mean())
# print(df_cen.sample())
# print(df_cen.corr())
# print(df_cen.shape)
# print(df_cen.columns.values)
# print(df_cen.tail())