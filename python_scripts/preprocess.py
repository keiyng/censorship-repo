import os
import re
import jieba
import pandas as pd
import numpy as np
import file_location

keywords_list = ['中国', '翻墙', '河蟹', '被河蟹', '五毛党', '五毛', '谷歌', '被和谐', '民主', '文革', '文化大革命', '茉莉花革命', '茉莉花', '示威', '抗议', '集会', '民众', '新闻自由', '言论自由', '宗教自由', '信仰自由', '台独', '藏独', '港独', '疆独', '新疆', '雾霾', '达赖喇嘛', '三聚氰胺', '地沟油', '毒奶粉', '雾霾', '豆腐渣', '薄熙来', 'bxl', '艾未未', '刘晓波', '晓波', 'lxb', '天安门', '六四', '知识产权', '山寨', '盗版', '三峡', '贫富', '洗脑', '人权', '维稳', '维权', '移民', '移居', '外资', '南海争议', '钓鱼岛', '钓鱼台', '女权', '爱国', '爱党', '奥巴马', '欧巴马', '共产党', '计划生育', '一孩政策', '红黄蓝', '三色幼儿园', '川普', '特朗普', '政改', '温家宝', '胡锦涛', 'wjb', 'hjt']

def add_topic_and_class_column(directory):
    for f in os.listdir(os.fsencode(directory)):
        if f.endswith(b'.csv'):
            file_name = f.decode('utf-8')
            df = pd.read_csv(directory + '/' + file_name)
            if f.endswith(b'_censored.csv') and f.startswith(b'jed'):          
                topic = file_name[4:-13]
                df['topic'] = topic
                df['class'] = 'censored'

            elif f.endswith(b'_uncensored.csv') and f.startswith(b'jed'):
                topic = file_name[4:-15]
                df['topic'] = topic
                df['class'] = 'uncensored' 

            df.to_csv(directory + '/' + file_name, index=False)   
            print('{}: {}'.format(file_name, df.shape))

def merge_csvs(directory):
    censored_df = []
    uncensored_df = []
    df_list = []
    for f in os.listdir(os.fsencode(directory)):
        if f.endswith(b'scrapped_sample_both_classes.csv'):
            file_name = f.decode('utf-8')
            df = pd.read_csv(directory + '/' + file_name)
            df.drop(columns=['followers_z', 'semantic_classes_z'], inplace=True)
            # print(df.columns.values)
            print(df.shape)
            df_list.append(df)
        elif f.endswith(b'old_both_classes.csv'):
            file_name = f.decode('utf-8')
            df = pd.read_csv(directory + '/' + file_name)
            print(df.shape)
            for name in df.columns.values:
                if name != 'topic' and name != 'class' and name != 'class_num':
                    df.rename(columns={name: name + '_z'}, inplace=True)
            for name in df.columns.values:
                if name == 'baiduai_pos_sent_z':
                    df.rename(columns={name: 'pos_sent_z'}, inplace=True)
                if name == 'baiduai_neg_sent_z':
                    df.rename(columns={name: 'neg_sent_z'}, inplace=True)
                if name == 'baiduai_sent_z':
                    df.rename(columns={name: 'sentiment_z'}, inplace=True)
                if name == 'char_freq_z':
                    df.rename(columns={name: 'charFreq_z'}, inplace=True)
                if name == 'word_freq_z':
                    df.rename(columns={name: 'wordFreq_z'}, inplace=True)
                if name == 'WC_over_semantic_groups_z':
                    df.rename(columns={name: 'wc_over_semantic_classes_z'}, inplace=True)
                
                        
            # print(df.columns.values)
            # print(df.shape)
            df_list.append(df)
            
    #         if f.endswith(b'_censored.csv'):
    #             censored_df.append(df)
    #         elif f.endswith(b'_uncensored.csv'):
    #             uncensored_df.append(df)   

    merged_df = pd.concat(df_list, sort=False)
    print(merged_df.columns.values)
    print(merged_df.shape)
    merged_df.to_csv(directory + '/' + 'old_and_scrapped_sample_both_classes.csv', index=False)

    # censored_merged_df = pd.concat(censored_df, sort=False)
    # uncensored_merged_df = pd.concat(uncensored_df, sort=False)

    # censored_merged_df.to_csv(directory + '/' + file_name[:3] + '_all_censored.csv', index=False)
    # uncensored_merged_df.to_csv(directory + '/' + file_name[:3] + '_all_uncensored.csv', index=False)

    # print(censored_merged_df.shape)
    # print(uncensored_merged_df.shape)

# merge_csvs(file_location.scrapped_features)

def remove_duplicates(directory):
    for f in os.listdir(os.fsencode(directory)):
        if f.endswith(b'.csv'):
            file_name = f.decode('utf-8')
            if 'all' in file_name:
                df = pd.read_csv(directory + '/' + file_name)
                print('{} before: {}'.format(file_name, df.shape))
                ## look at the duplicates if necessary
                # duplicates = pd.concat(dup for _, dup in df.groupby('content') if len(dup) > 1)
                df_dropped = df.drop_duplicates(subset='content')
                print('{} after: {}'.format(file_name, df_dropped.shape))
                df_dropped.to_csv(directory + '/' + file_name, index=False)


def clean_data(directory):
    for f in os.listdir(os.fsencode(directory)):
        if f.endswith(b'.csv'):
            cleaned = []
            file_name = f.decode('utf-8')
            df = pd.read_csv(directory + '/' + file_name)

            for index, data in df.iterrows():
                data['content'] = re.sub(r'\n+', ' ', data['content']) ## newline
                data['content'] = re.sub(r'\r', ' ', data['content']) ## linebreak
                data['content'] = re.sub(r'收起全文d', '', data['content']) ## collapse
                data['content'] = re.sub(r'(//)', '', data['content']) ## slashes
                data['content'] = re.sub(r'(@.+?)[:：;]+', ' ', data['content']) ## tagged user reply
                data['content'] = re.sub(r'(@.+?)\s+', ' ', data['content']) ## tagged user
                data['content'] = re.sub(r'(@.+?)$', ' ', data['content']) ## end of text
                data['content'] = re.sub(r'(转发微博)', '', data['content']) ## retweet
                data['content'] = re.sub(r'(转：)', '', data['content']) ## reblog
                data['content'] = re.sub(r'#', ' ', data['content']) ## hashtag
                data['content'] = re.sub(r'(→_→)', '', data['content']) ## arrows
                data['content'] = re.sub(r'(回复)', '', data['content']) ## reply
                data['content'] = re.sub(r'(网页链接)', '', data['content']) ## link
                data['content'] = re.sub(r'\[.+?\]', '', data['content']) ## emoticon text
                data['content'] = re.sub(r'', ' ', data['content']) ## special symbol
                data['content'] = data['content'].strip()
                
                cleaned.append(data)

            df_cleaned = pd.DataFrame(cleaned)
            df_cleaned.to_csv(directory + '/' + file_name, index=False)


def remove_nan_and_short_rows(directory):
    for f in os.listdir(os.fsencode(directory)):
        if f.endswith(b'.csv'):
            file_name = f.decode('utf-8')
            df = pd.read_csv(directory + '/' + file_name)
            print('before {}'.format(df.shape))
            for index, data in df.iterrows():
                if type(data['content']) is not str or len(data['content']) <= 5 or '好声音' in data['content'] or '中国移动' in data['content'] or '音乐' in data['content'] or '一善' in data['content']:
                    df.drop(index, inplace=True)
            print('after {}'.format(df.shape))
            df.to_csv(directory + '/' + file_name, index=False)


def sort_by_content(directory):
    for f in os.listdir(os.fsencode(directory)):
        if f.endswith(b'.csv'):
            file_name = f.decode('utf-8')
            df = pd.read_csv(directory + '/' + file_name)
            df.sort_values(by=['content']).to_csv(directory + '/' + file_name, index=False)


def remove_similar(directory):
    for f in os.listdir(os.fsencode(directory)):
        if f.endswith(b'.csv'):
            file_name = f.decode('utf-8')
            df = pd.read_csv(directory + '/' + file_name)

            print(file_name + str(df.shape))

            ## group data by their first character
            groups = dict()
            for index, data in df.iterrows():
                if data['content'][0] in groups.keys():
                    continue
                else:
                    current = index
                    try:
                        while data['content'][0] == df.iloc[current+1]['content'][0]:
                            if data['content'][0] not in groups.keys():
                                groups[data['content'][0]] = [data]
                            groups[data['content'][0]].append(df.iloc[current+1])
                            current += 1
                    except:
                        print('end')
            
            print('no. of groups created: {}'.format(len(groups)))

            ## remove similar posts
            similar = []
            for key, value in groups.items():
                if len(value) > 1:
                    for i in range(len(value) - 1):
                        if len(value[i]['content']) > 15:
                            cutoff = int(len(value[i]['content']) / 2)
                            if value[i]['content'][:cutoff] in value[i+1]['content'][:cutoff]:
                                # print(value[i+1]['content'])
                                similar.append(value[i+1]['mid'])
            print('similar posts found: {}'.format(len(similar)))

            for index, data in df.iterrows():
                if data['mid'] in similar:
                    df.drop(index, inplace=True)
            print(df.shape)

            df.to_csv(directory + '/' + file_name, index=False)


def remove_irrelevant(directory):
    for f in os.listdir(os.fsencode(directory)):
        if f.endswith(b'.csv'):
            relevant = []
            file_name = f.decode('utf-8')
            df = pd.read_csv(directory + '/' + file_name)
            df_drop = pd.read_csv(directory + '/' + file_name)
            print(df.shape)
            
            for index, data in df.iterrows():
                if data['topic'] != 'everythingElse':
                    if not any(keyword in data['content'] for keyword in keywords_list):
                        df_drop.drop(index, inplace=True)
            print(df_drop.shape)


def segment(directory):
    for f in os.listdir(os.fsencode(directory)):
        if f.endswith(b'.csv'):
            file_name = f.decode('utf-8')
            df = pd.read_csv(directory + '/' + f.decode('utf-8'))
            print(df.shape)

            for word in keywords_list:
                jieba.add_word(word)
                jieba.suggest_freq(word, True)

            segmented_data = []
            for index, data in df.iterrows():
                data['content'] = jieba.cut(data['content'], cut_all=False, HMM=True)
                data['content'] = ' '.join(data['content'])
                data['content'] = re.sub(r'\s+', ' ', data['content'])
                segmented_data.append(data)

            print(pd.DataFrame(segmented_data).shape)

            pd.DataFrame(segmented_data).to_csv(directory + '/' + file_name, index=False)

def convert_punctuations(directory):

    comma = re.compile(r'，')
    period = re.compile(r'。')
    comma_chi = re.compile(r'、')
    semi_colon = re.compile(r'；')
    colon = re.compile(r'：')
    open_quote = re.compile(r'「')
    close_quote = re.compile(r'」')
    open_quote_2 = re.compile(r'『')
    close_quote_2 = re.compile(r'』')
    open_paren = re.compile(r'（')
    close_paren = re.compile(r'）')
    open_bracket = re.compile(r'【')
    close_bracket = re.compile(r'】')
    question_mark = re.compile(r'？')
    exclamation_mark = re.compile(r'！')
    dash = re.compile(r'──')
    elipses = re.compile(r'……')
    elipses_2 = re.compile(r'⋯')
    dash_short = re.compile(r'—')
    pound = re.compile(r'＃')
    dollar = re.compile(r'＄')
    percent = re.compile(r'％')
    ampersand = re.compile(r'＆')
    asterisk = re.compile(r'＊')
    plus = re.compile(r'＋')
    forward_slash = re.compile(r'／')
    less_than = re.compile(r'＜')
    more_than = re.compile(r'＞')
    equal = re.compile(r'＝')
    trail = re.compile(r'～')

    for f in os.listdir(os.fsencode(directory)):
        if f.endswith(b'.csv'):
            file_name = f.decode('utf-8')
            df = pd.read_csv(directory + '/' + f.decode('utf-8'))
            converted = []

            for index, data in df.iterrows():
                data['content'] = re.sub(comma, ',', data['content'])
                data['content'] = re.sub(period, '.', data['content'])
                data['content'] = re.sub(comma_chi, ',', data['content'])
                data['content'] = re.sub(semi_colon, ';', data['content'])
                data['content'] = re.sub(colon, ':', data['content'])
                data['content'] = re.sub(open_quote, '"', data['content'])
                data['content'] = re.sub(close_quote, '"', data['content'])
                data['content'] = re.sub(open_quote_2, '"', data['content'])
                data['content'] = re.sub(close_quote_2, '"', data['content'])
                data['content'] = re.sub(open_paren, '(', data['content'])
                data['content'] = re.sub(close_paren, ')', data['content'])
                data['content'] = re.sub(open_bracket, '[', data['content'])
                data['content'] = re.sub(close_bracket, ']', data['content'])
                data['content'] = re.sub(question_mark, '?', data['content'])
                data['content'] = re.sub(exclamation_mark, '!', data['content'])
                data['content'] = re.sub(dash, '_', data['content'])
                data['content'] = re.sub(elipses, '…', data['content'])
                data['content'] = re.sub(elipses_2, '…', data['content'])
                data['content'] = re.sub(dash_short, '-', data['content'])
                data['content'] = re.sub(pound, '#', data['content'])
                data['content'] = re.sub(dollar, '$', data['content'])
                data['content'] = re.sub(percent, '%', data['content'])
                data['content'] = re.sub(ampersand, '&', data['content'])
                data['content'] = re.sub(asterisk, '*', data['content'])
                data['content'] = re.sub(plus, '+', data['content'])
                data['content'] = re.sub(forward_slash, '/', data['content'])
                data['content'] = re.sub(less_than, '<', data['content'])
                data['content'] = re.sub(more_than, '>', data['content'])
                data['content'] = re.sub(equal, '=', data['content'])
                data['content'] = re.sub(trail, '~', data['content'])
                data['content'] = data['content'].lstrip()
                data['content'] = data['content'].rstrip()

                converted.append(data)
     
            print(pd.DataFrame(converted).shape)
            pd.DataFrame(converted).to_csv(directory + '/punc_' + file_name, index=False)

def rename_and_drop_columns(directory):
    for f in os.listdir(os.fsencode(directory)):
        if f.endswith(b'.csv'):
            file_name = f.decode('utf-8')
            df = pd.read_csv(directory + '/' + file_name)

            if 'uncensored' in file_name:
                df.rename(columns={'A': 'content', 'C': 'followers', 'H': 'topic', 'I': 'class'}, inplace=True)
                df.drop(columns=['B', 'D', 'E', 'F', 'G'], inplace=True)
            else:
                df.rename(columns={'Source (A)': 'content', 'Source (C)': 'followers', 'Source (H)': 'topic', 'Source (I)': 'class'}, inplace=True)
                df.drop(columns=['Source (B)', 'Source (D)', 'Source (E)', 'Source (F)', 'Source (G)'], inplace=True)

            df.to_csv(directory + '/' + file_name, index=False)


def extract_content_to_txt(directory):
    for f in os.listdir(os.fsencode(directory)):
        if f.endswith(b'.csv') and b'old' in f:
            file_name = f.decode('utf-8')
            df = pd.read_csv(directory + '/' + file_name)
            np.savetxt(directory + '/' + file_name.replace('csv', 'txt'), df['Data'], fmt='%s' , newline='\n')

# extract_content_to_txt('/Users/Kei/Desktop')

def rearrange_crie(directory):
    for f in os.listdir(os.fsencode(directory)):
        if f.endswith(b'.xls') and b'crie' in f:
            file_name = f.decode('utf-8')
            df = pd.read_excel(directory + '/' + file_name)
            print(file_name)
            print(df.shape)
            
            adjusted = []
            for index, data in df.iterrows():
                data['File_Name'] = data['File_Name'].replace('.txt', '')
                data['File_Name'] = int(data['File_Name'])
                adjusted.append(data)

            pd.DataFrame(adjusted).to_csv(directory + '/csv/' + file_name.replace('.xls', '.csv'), index=False)

# rearrange_crie('/Users/Kei/Desktop/old')


def merge_and_sort_crie(directory):
    df_censored_list = []
    df_uncensored_list = []
    for f in os.listdir(os.fsencode(directory)):
        if f.endswith(b'.csv'):
            file_name = f.decode('utf-8')
            df = pd.read_csv(directory + '/' + file_name)
            df.sort_values(by=['File_Name'], inplace=True)
            df.to_csv(directory + '/' + file_name, index=False)
            # if '_censored' in file_name:
                # df['class'] = 'censored'
                # df['class_num'] = 1
                # df_censored_list.append(df)
                # df.sort_values(by=['File_Name'], inplace=True)
            # elif 'uncensored' in file_name and 'missed' in file_name:
            #     df['class'] = 'uncensored'
            #     df['class_num'] = 0
            #     df_uncensored_list.append(df)
                
    
    # merged_censored_df = pd.concat(df_censored_list, sort=False)
    # merged_uncensored_df = pd.concat(df_uncensored_list, sort=False)
    # print(merged_censored_df.shape)
    # print(merged_uncensored_df.shape)

    # merged_censored_df.sort_values(by=['File_Name'], inplace=True)
    # merged_uncensored_df.sort_values(by=['File_Name'], inplace=True)

    # merged_censored_df.to_csv(directory + '/' + 'jed_all_censored_crie.csv', index=False)
    # merged_uncensored_df.to_csv(directory + '/' + 'jed_all_uncensored_crie.csv', index=False)


def normalize_crie(directory):
    for f in os.listdir(os.fsencode(directory)):
        normalized = []
        if f.endswith(b'.csv') and b'both' in f:
            file_name = f.decode('utf-8')
            df = pd.read_csv(directory + '/' + file_name)
            df.fillna(0, inplace=True)

            for index, data in df.iterrows():
                if int(data['Words']) == 0:
                    print("words " + str(index))
                    data['Words'] = 1
                if int(data['Characters']) == 0:
                    data['Characters'] = 1
                    print("chars " + str(index))
                if int(data['Sentences']) == 0:
                    data['Sentences'] = 1
                    print("sents " + str(index))

                try:
                    data['Adverbs'] = int(data['Adverbs']) / int(data['Words'])
                    data['Verbs'] = int(data['Verbs']) / int(data['Words'])
                    data['Difficult words'] = int(data['Difficult words']) / int(data['Words'])
                    data['Content words'] = int(data['Content words']) / int(data['Words'])
                    data['Negatives'] = int(data['Negatives']) / int(data['Words'])
                    data['Two-character words'] = int(data['Two-character words']) / int(data['Words'])
                    data['Three-character words'] = int(data['Three-character words']) / int(data['Words'])
                    data['Intentional words'] = int(data['Intentional words']) / int(data['Words'])
                    data['Number of Idioms'] = int(data['Number of Idioms']) / int(data['Words'])
                    data['Pronouns'] = int(data['Pronouns']) / int(data['Words'])
                    data['Personal pronouns'] = int(data['Personal pronouns']) / int(data['Words'])
                    data['First personal pronouns'] = int(data['First personal pronouns']) / int(data['Words'])
                    data['Third personal pronouns'] = int(data['Third personal pronouns']) / int(data['Words'])
                    data['conjunctions'] = int(data['conjunctions']) / int(data['Words'])
                    data['positive conjunctions'] = int(data['positive conjunctions']) / int(data['Words'])
                    data['negative conjunctions'] = int(data['negative conjunctions']) / int(data['Words'])
                    data['adversative conjunctions'] = int(data['adversative conjunctions']) / int(data['Words'])
                    data['causal conjunctions'] = int(data['causal conjunctions']) / int(data['Words'])
                    data['hypothesis conjunction'] = int(data['hypothesis conjunction']) / int(data['Words'])
                    data['condition conjunction'] = int(data['condition conjunction']) / int(data['Words'])
                    data['purpose conjunctions'] = int(data['purpose conjunctions']) / int(data['Words'])
                    data['Content word category'] = int(data['Content word category']) / int(data['Words'])

                    data['Low-stroke characters'] = int(data['Low-stroke characters']) / int(data['Characters'])
                    data['Intermediate-stroke characters'] = int(data['Intermediate-stroke characters']) / int(data['Characters'])        
                    data['High-stroke characters'] = int(data['High-stroke characters']) / int(data['Characters'])

                    data['Sentences with complex structure'] = int(data['Sentences with complex structure']) / int(data['Sentences'])
                    data['Parallelism'] = int(data['Parallelism']) / int(data['Sentences'])
                    data['Sentences with complex semantic categories'] = int(data['Sentences with complex semantic categories']) / int(data['Sentences'])
                    data['figure of speech (simile)'] = int(data['figure of speech (simile)']) / int(data['Sentences'])
                except ZeroDivisionError:
                    print("error" + str(index))
                    continue

            # for index, data in df.iterrows():
            #     data['副词数'] = int(data['副词数']) / int(data['词数'])
            #     data['动词数'] = int(data['动词数']) / int(data['词数'])
            #     data['难词数'] = int(data['难词数']) / int(data['词数'])
            #     data['实词数'] = int(data['实词数']) / int(data['词数'])
            #     data['否定词数'] = int(data['否定词数']) / int(data['词数'])
            #     data['二字词数'] = int(data['二字词数']) / int(data['词数'])
            #     data['三字词数'] = int(data['三字词数']) / int(data['词数'])
            #     data['意图性词汇数'] = int(data['意图性词汇数']) / int(data['词数'])
            #     data['成语数'] = int(data['成语数']) / int(data['词数'])
            #     data['代名词数'] = int(data['代名词数']) / int(data['词数'])
            #     data['人称代名词数'] = int(data['人称代名词数']) / int(data['词数'])
            #     data['第一人称代名词数'] = int(data['第一人称代名词数']) / int(data['词数'])
            #     data['第三人称代名词数'] = int(data['第三人称代名词数']) / int(data['词数'])
            #     data['连接词数'] = int(data['连接词数']) / int(data['词数'])
            #     data['正向连接词数'] = int(data['正向连接词数']) / int(data['词数'])
            #     data['负向连接词数'] = int(data['负向连接词数']) / int(data['词数'])
            #     data['转折连接词数'] = int(data['转折连接词数']) / int(data['词数'])
            #     data['因果连接词数'] = int(data['因果连接词数']) / int(data['词数'])
            #     data['假设连接词数'] = int(data['假设连接词数']) / int(data['词数'])
            #     data['条件连接词数'] = int(data['条件连接词数']) / int(data['词数'])
            #     data['目的连接词数'] = int(data['目的连接词数']) / int(data['词数'])
            #     data['实词种类数'] = int(data['实词种类数']) / int(data['词数'])

            #     data['低笔划字符数'] = int(data['低笔划字符数']) / int(data['字数'])
            #     data['中笔划字符数'] = int(data['中笔划字符数']) / int(data['字数'])        
            #     data['高笔划字符数'] = int(data['高笔划字符数']) / int(data['字数'])

            #     data['复杂结构句数'] = int(data['复杂结构句数']) / int(data['句数'])
            #     data['排比法句子数'] = int(data['排比法句子数']) / int(data['句数'])
            #     data['复杂语意类别句子数'] = int(data['复杂语意类别句子数']) / int(data['句数'])
            #     data['譬喻法句子数'] = int(data['譬喻法句子数']) / int(data['句数'])


                normalized.append(data)

            pd.DataFrame(normalized).to_csv(directory + '/' + file_name.replace('.csv', '_normalized.csv'), index=False)

# normalize_crie('/Users/Kei/OneDrive/old_data/crie/raw')

# f = pd.read_csv('/Users/Kei/OneDrive/revised_data/weka/crie/csv/scrapped_all_uncensored_crie_dropped.csv')
# print(f.shape)
# f.drop_duplicates(subset=['File_Name'], inplace=True)
# print(f.shape)
# f.to_csv('/Users/Kei/OneDrive/revised_data/weka/crie/csv/scrapped_all_uncensored_crie_dropped2.csv', index=False)




