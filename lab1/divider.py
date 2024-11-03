'''
pip install pandas jieba 
''' 
import pandas as pd
import re
import jieba

def clean_and_split_tags(tags):
    # 去除特殊字符和未转义字符
    tags = re.sub(r'[^a-zA-Z0-9\u4e00-\u9fa5，,]', '', tags)  # 保留中英文、数字和逗号
    # 中英分词：中文用jieba，英文用空格或逗号分隔
    words = []
    for tag in tags.split(','):
        if re.search(r'[\u4e00-\u9fa5]', tag):  # 判断是否包含中文
            words.extend(jieba.lcut(tag))  # 中文分词
        else:
            words.extend(tag.split())  # 英文分词
    return set(words)  # 去重

df = pd.read_csv("selected_book_top_1200_data_tag.csv")
df['Processed_Tags'] = df['Tags'].apply(clean_and_split_tags)
df.drop(columns=['Tags'], inplace=True)
df.to_csv("processed_selected_book_top_1200_data_tag.csv", index=False)