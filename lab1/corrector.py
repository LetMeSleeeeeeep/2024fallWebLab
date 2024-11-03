from pycorrector import Corrector
from pycorrector import EnSpellCorrector
import pandas as pd
m = Corrector()
df = pd.read_csv('/home/cherubim02/pytest/selected_book_top_1200_data_tag.csv')
temp = df.loc[0, 'Tags'].strip('}{').split(',')
new = []
for strings in temp:
    new.append(m.correct(strings)['target'])
print(new)
print(m.correct('一本不象话的小说'))