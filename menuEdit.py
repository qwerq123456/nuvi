import re
menuBefore = "혼합잡곡밥  <br/>북어무국  (1.5.6.13.14.16.18.)<br/>꽃만두찜  (1.5.6.10.13.16.18.)<br/>골뱅이무침&소면  (5.6.13.17.18.)<br/>소불고기파채볶음  (5.6.10.13.14.16.18.)<br/>배추김치  (9.13.)"

p = re.compile('\([^)]*\)')

temp = re.sub('\([^)]*\)', '', menuBefore)
temp = temp.replace('  <br/>', ', ')
print(temp)
# print(menuList)
# 1. space 제거
# 2. 괄호 안 문자 제거
# 3. <br/>제거


# import re

# html_source = '<p>정규 표현식이라는 문구는 일치하는 텍스트가 준수해야 하는 "패턴"을 표현하기 위해..</p><p>문자열1</p><p>문자열2</p><p>문자열3</p>'
# p = re.compile('(?<=\<p>)(.*?)(?=<\/p>)')
# p_tag_list = p.findall(html_source)

# print(p_tag_list)
