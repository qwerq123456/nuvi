import requests
# import json
import re
# from multiprocessing import Pool
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
    deleteBracketString = re.sub(r'\([^)]*\)', '', menustring)
    deleteNumberString = re.sub(r'[0-9]+', '', deleteBracketString)
    # we can just delete special character with regex
    replaceSpecialCharacterString = deleteNumberString.replace('.', '').replace('@', '').replace(
        ' ', '').replace('<br/>', ', ').replace('^', '').replace('*', '').replace('-', '').replace('#', '')
    return replaceSpecialCharacterString


# error list has to re run
errorSchoolCodeList = []

# this list of school has no data
noDataSchoolCodeList = []


def getMealDataWithSchoolCode(SD_SCHUL_CODE, count):
    url = BASE_URL + MEAL_URL + OPTION + \
        '&pIndex=1&pSize=1000&SD_SCHUL_CODE=' + SD_SCHUL_CODE + \
        "&MLSV_FROM_YMD=" + MLSV_FROM_YMD + "&MLSV_TO_YMD=" + MLSV_TO_YMD

    try:
        res = requests.get(url).json()

    except:
        print('request error with schoolCode : ' + SD_SCHUL_CODE)
        errorSchoolCodeList.append(SD_SCHUL_CODE)
        return[]

    if "mealServiceDietInfo" not in res:
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
    print('school count : ' + str(count))
    print("schoolCode : " + SD_SCHUL_CODE + "success!")
    return mealDataList


def main():
    getSchoolCodeList()
    print('get school code list end')

    tempList = []
    count = 0
    for SD_SCHUL_CODE in SD_SCHUL_CODE_LIST:
        count += 1
        tempList.append(getMealDataWithSchoolCode(SD_SCHUL_CODE, count))
    
    # p = Pool(processes=10)
    # tempList = p.map(getMealDataWithSchoolCode, [SD_SCHUL_CODE for SD_SCHUL_CODE in SD_SCHUL_CODE_LIST])
    # p.close()
    # p.join()

    print('temp list end')

    result = list(itertools.chain(*tempList))

    print('list flatten end')

    resultDataFrame = pd.DataFrame(
        result, columns=['학교명', '날짜', '구분', '메뉴', '칼로리'])

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
