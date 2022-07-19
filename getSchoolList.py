import requests
import json

# essential

# base url
BASE_URL = "https://open.neis.go.kr/hub/schoolInfo"

# data type
Type = 'json'

# api key
Key = '1475950391944d1c8831b761ade19ff6'

# 교육청 코드 (서울 교육청 코드)
ATPT_OFCDC_SC_CODE = 'B10'

# # pageNum
# pIndex = '1'

# # data per page
# pSize = '300'

SD_SCHUL_CODE_LIST = []


def getSchoolCode(i):
    # url
    url = "https://open.neis.go.kr/hub/schoolInfo?Type=json&ATPT_OFCDC_SC_CODE=B10&Key=1475950391944d1c8831b761ade19ff6&pIndex="+str(i)

    res = requests.get(url).json()

    schoolList = res["schoolInfo"][1]["row"]

    for school in schoolList:
        SD_SCHUL_CODE_LIST.append(school["SD_SCHUL_CODE"])


for i in range(1, 16):
    print(i)
    getSchoolCode(i)
# 학교 코드 리스트


print(len(list(set(SD_SCHUL_CODE_LIST))))



