import pandas as pd
import random

scraped_censored = pd.read_csv('../revised_data/scraped_all_censored.csv')
scraped_uncensored = pd.read_csv('../revised_data/scraped_all_uncensored.csv')
scraped_sample_both = pd.read_csv('/Users/Kei/OneDrive/revised_data/weka/standardized/scraped_z_sample_both_classes.csv')
scraped_censored_survey = pd.read_csv('/Users/Kei/OneDrive/revised_data/survey/scraped_censored_survey.csv')
scraped_uncensored_survey = pd.read_csv('/Users/Kei/OneDrive/revised_data/survey/scraped_uncensored_survey.csv')

scraped_batch_8 = pd.read_csv('/Users/Kei/OneDrive/revised_data/survey/batches/batch_8.csv')

def extract_data():
    idx = []
    censored = []
    uncensored_sampled = []

    for index, data in scraped_sample_both.iterrows():
        if data['class'] == 'uncensored':
            idx.append(data['idx'])

    for index, data in scraped_uncensored.iterrows():
        if data['idx'] in idx:
            data['content'] = data['content'].replace(" ", "")
            uncensored_sampled.append(data)

    for index, data in scraped_censored.iterrows():
            data['content'] = data['content'].replace(" ", "")
            censored.append(data)

    random.shuffle(censored)
    censored_df = pd.DataFrame(censored).sample(400)
    censored_df.to_csv('../revised_data/survey/scraped_censored_survey.csv', index=False)
    random.shuffle(uncensored_sampled)
    uncensored_sampled_df = pd.DataFrame(uncensored_sampled).sample(400)
    uncensored_sampled_df.to_csv('../revised_data/survey/scraped_uncensored_survey.csv', index=False)

def create_batches():
    batch_1 = []
    batch_2 = []
    batch_3 = []
    batch_4 = []
    batch_5 = []
    batch_6 = []
    batch_7 = []
    batch_8 = []
    for index, data in scraped_censored_survey.iterrows():
        if index-1 <= 50:
            batch_1.append(data)
        elif index-1 <=100:
            batch_2.append(data)
        elif index-1 <=150:
            batch_3.append(data)
        elif index-1 <=200:
            batch_4.append(data)
        elif index-1 <=250:
            batch_5.append(data)
        elif index-1 <=300:
            batch_6.append(data)
        elif index-1 <=350:
            batch_7.append(data)
        elif index-1 <=400:
            batch_8.append(data)
        
    for index, data in scraped_uncensored_survey.iterrows():
        if index-1 <= 50:
            batch_1.append(data)
        elif index-1 <=100:
            batch_2.append(data)
        elif index-1 <=150:
            batch_3.append(data)
        elif index-1 <=200:
            batch_4.append(data)
        elif index-1 <=250:
            batch_5.append(data)
        elif index-1 <=300:
            batch_6.append(data)
        elif index-1 <=350:
            batch_7.append(data)
        elif index-1 <=400:
            batch_8.append(data)
    
    random.shuffle(batch_1)
    random.shuffle(batch_2)
    random.shuffle(batch_3)
    random.shuffle(batch_4)
    random.shuffle(batch_5)
    random.shuffle(batch_6)
    random.shuffle(batch_7)
    random.shuffle(batch_8)

    pd.DataFrame(batch_1).to_csv('/Users/Kei/OneDrive/revised_data/survey/batches/batch_1.csv', index=False)
    pd.DataFrame(batch_2).to_csv('/Users/Kei/OneDrive/revised_data/survey/batches/batch_2.csv', index=False)
    pd.DataFrame(batch_3).to_csv('/Users/Kei/OneDrive/revised_data/survey/batches/batch_3.csv', index=False)
    pd.DataFrame(batch_4).to_csv('/Users/Kei/OneDrive/revised_data/survey/batches/batch_4.csv', index=False)
    pd.DataFrame(batch_5).to_csv('/Users/Kei/OneDrive/revised_data/survey/batches/batch_5.csv', index=False)
    pd.DataFrame(batch_6).to_csv('/Users/Kei/OneDrive/revised_data/survey/batches/batch_6.csv', index=False)
    pd.DataFrame(batch_7).to_csv('/Users/Kei/OneDrive/revised_data/survey/batches/batch_7.csv', index=False)
    pd.DataFrame(batch_8).to_csv('/Users/Kei/OneDrive/revised_data/survey/batches/batch_8.csv', index=False)

def create_survey():
    with open('/Users/Kei/OneDrive/revised_data/survey/batches/batch_8.txt', 'w', encoding='utf-8') as output:
        for index, data in scraped_batch_8.iterrows():
            output.write("[[Block]]\n")
            output.write("{}. ".format(index+1))
            output.write(data['content'])
            output.write('\n\n')
            output.write('你认为此内容会被微博屏蔽吗？\n')
            output.write('你认为此微博内容会触发争论或骂战吗？\n')
            output.write('你认为此微博内容有触发集会、游行示威或暴动的可能吗？')
            output.write('\n\n')
            output.write('会\n')
            output.write('不会')
            output.write('\n\n\n')
            
        
# create_survey()
