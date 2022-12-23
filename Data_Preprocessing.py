import pandas as pd
import numpy as np
import re
import sys
from sklearn import preprocessing

def preprocess_word(word):
    # Remove punctuation
    word = word.strip('\'"?!,.():;')
    word = word.replace('\\','')
    # Convert more than 2 letter repetitions to 2 letter
    # sooooo --> so
    word = re.sub(r'(.)\1+', r'\1\1', word)
    # Remove - & '
    word = re.sub(r'(-|\')', '', word)
    return word

def is_valid_word(word):
    # Check if word begins with an alphabet
    return (re.search(r'^[a-zA-Z][a-z0-9A-Z\._]*$', word) is not None)

def preprocess_rmp(comment):
    processed_rmp = []
    # Convert to lower case
    comment = comment.lower()
    # Replaces URLs with the word URL
    comment = re.sub(r'((www\.[\S]+)|(https?://[\S]+))', ' URL ', comment)
    # Replaces #hashtag with hashtag
    comment = re.sub(r'#(\S+)', r' \1 ', comment)
    # Replace 2+ dots with space
    comment = re.sub(r'\.{2,}', ' ', comment)
    # Strip space, " and ' from tweet
    comment = comment.strip(' "\'')
    # Replace multiple spaces with a single space
    comment = re.sub(r'\s+', ' ', comment)
    words = comment.split()

    for word in words:
        word = preprocess_word(word)
        processed_rmp.append(word)


    return ' '.join(processed_rmp)


def preprocess_csv(csv_file_name, processed_file_name):
    df = pd.read_csv(csv_file_name,sep=",")
    department_name = df.loc[:,"d_category"]
    state_name = df.loc[:,"s_category"]
    #Guassian Distribution Normalizaton for num_student
    num_student = df.loc[:,"num_student"]
    df['num_student'] = (df['num_student']-df['num_student'].mean())/df['num_student'].std()
    num_student = df.loc[:,"num_student"]
    normal_student = list(num_student)
    # label for sentiment analysis
    student_star = df.loc[:,"student_star"]
    values = df['student_star'].values
    sentiment = []
    for i in values:
        if i > 3.0:
                sentiment.append("1")
        else:
                sentiment.append("0")
    # Guassian Distribution Normalization for student_difficult
    student_difficult = df.loc[:,"student_difficult"]
    df['student_difficult'] = (df['student_difficult']-df['student_difficult'].mean())/df['student_difficult'].std()
    student_difficult = df.loc[:,"student_difficult"]
    normal_stu_diff = list(student_difficult)
    # Guassian Distribution Normalization for words count
    word_comment = df.loc[:,"word_comment"]
    df['word_comment'] = (df['word_comment']-df['word_comment'].mean())/df['word_comment'].std()
    word_comment = df.loc[:,"word_comment"]
    normal_word_cot = list(word_comment)
    # words cleaning for comments
    comments = df.loc[:,"comments"]
    df['comments'].replace(' ',np.nan, inplace = True)
    df['comments'].replace('No Comments',np.nan, inplace = True)
    df.dropna(subset=["comments"],inplace = True)
    comments = df.loc[:,"comments"]
    raw = list(comments)
    processed = []
    for line in raw:
        processed.append(preprocess_rmp(line))
    new_df = pd.DataFrame(list(zip(department_name,state_name,normal_student,sentiment,normal_stu_diff,normal_word_cot,processed)),columns=["department_name","state_name","num_student","label","student_difficult","word_comment","processed_comments"])
    new_df.dropna(how = "any",inplace = True)
    new_df.to_csv(processed_file_name)
    print('\n Saved processed comments to: %s' % processed_file_name)
    return processed_file_name

if __name__ == '__main__':
    if len(sys.argv) != 2:
            print ('Usage: python preprocess.py <raw-CSV>')
            exit()
    csv_file_name = sys.argv[1]
    processed_file_name = 'processed.csv'
    preprocess_csv(csv_file_name, processed_file_name)
