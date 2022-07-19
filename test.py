import itertools
import pandas as pd
my_list = [[['서울고', '중식', '밥,국'], ['평택고', '석식', '밥,국,찌개']],
           [['서울고', '중식', '밥,국'], ['평택고', '석식', '밥,국,찌개']]]

temp = list(itertools.chain(*my_list))
df = pd.DataFrame(temp, columns=['학교명', '구분', '메뉴'])
print(df)

file_name = './df.xlsx'
df.to_excel(file_name)

# 학교명, 날짜, 구분, 메뉴, 칼로리

