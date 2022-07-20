import requests
# import json
import re
from multiprocessing import Pool
import itertools
import pandas as pd
import os
# urls
BASE_URL = 'https://open.neis.go.kr/hub'
MEAL_URL = '/mealServiceDietInfo'
SCHOOL_URL = '/schoolInfo'

# default option
OPTION = '?Type=json&Key=b7b09678fd90486fb48d6cb42cdeb63e&ATPT_OFCDC_SC_CODE=B10'

# start & end date
MLSV_FROM_YMD = '20210101'
MLSV_TO_YMD = '20211231'

# school code list in seoul
SD_SCHUL_CODE_LIST = []


def getSchoolCodeByIndex(i):
    url = BASE_URL + SCHOOL_URL + OPTION + '&pIndex=' + str(i)

    res = requests.get(url).json()

    schoolList = res["schoolInfo"][1]["row"]

    for school in schoolList:
        SD_SCHUL_CODE_LIST.append(school["SD_SCHUL_CODE"])


def getSchoolCodeList():
    for i in range(1, 16):
        getSchoolCodeByIndex(i)

def makeMenuString(menustring):
    # todo : has to make replace list 
    # just delete all alphabet?
    temp = re.sub(r'\([^)]*\)', '', menustring)
    temp1 = re.sub(r'[0-9]+', '', temp)
    temp2 = temp1.replace('.', '')
    temp3 = temp2.replace('@', '')
    temp4 = temp3.replace(' ', '')
    temp5 = temp4.replace('<br/>', ', ').replace('^' , '').replace('*' , '').replace('-','').replace('#','')
    return temp5

errorSchoolCodeList = []
noDataSchoolCodeList = []  
def getMealDataWithSchoolCode(SD_SCHUL_CODE):
    # todo : make date and schoolcode option
    url = BASE_URL + MEAL_URL + OPTION + \
        '&pIndex=1&pSize=1000&SD_SCHUL_CODE=' + SD_SCHUL_CODE + "&MLSV_FROM_YMD=20210101&MLSV_TO_YMD=20211231"
    try:
        res = requests.get(url).json()
    except:
        print('request error with schoolCode : ' + SD_SCHUL_CODE)
        errorSchoolCodeList.append(SD_SCHUL_CODE)
        return[]
    if "mealServiceDietInfo" not in res:
        # print("no data with School Code : " + SD_SCHUL_CODE)
        noDataSchoolCodeList.append(SD_SCHUL_CODE)
        print(res)
        return []

    mealResDataList = res["mealServiceDietInfo"][1]["row"]

    mealDataList = []

    for mealResData in mealResDataList:
        data = []
        data.append(mealResData["SCHUL_NM"])
        data.append(mealResData["MLSV_YMD"])
        data.append(mealResData["MMEAL_SC_NM"])
        data.append(makeMenuString(mealResData["DDISH_NM"]))
        data.append(mealResData["CAL_INFO"])
        mealDataList.append(data)

    print('process id : ', os.getpid())
    # print('school count : ' + str(count))
    print("schoolCode : " + SD_SCHUL_CODE + "success!")
    return mealDataList

# 7011113
# SD_SCHUL_CODE_LIST = ["7011113","7010267","7010292"]
def main():
    getSchoolCodeList()
    print('get school code list end')
    p = Pool(processes=10)
    tempList = []
    # count = 0
    # for SD_SCHUL_CODE in SD_SCHUL_CODE_LIST:
    #     count += 1
    #     tempList.append(getMealDataWithSchoolCode(SD_SCHUL_CODE, count))
    tempList = p.map(getMealDataWithSchoolCode, [SD_SCHUL_CODE for SD_SCHUL_CODE in SD_SCHUL_CODE_LIST])
    p.close()
    p.join()
    print('temp list end')
    result = list(itertools.chain(*tempList))
    print('list flatten end')
    # print(result)
    resultDataFrame = pd.DataFrame(result, columns=['학교명', '날짜', '구분', '메뉴', '칼로리'])
    print('make dataframe end')
    file_name = './nuvi_schoolmeal.xlsx'
    resultDataFrame.to_excel(file_name)
    print('all ends')
    print('____error List____')
    print(errorSchoolCodeList)
    print('___no data List___')
    print(noDataSchoolCodeList)
if __name__ == "__main__":
    main()
