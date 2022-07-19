import requests
import json
import re
from multiprocessing import Pool
import itertools
import pandas as pd

# urls
BASE_URL = 'https://open.neis.go.kr/hub'
MEAL_URL = '/mealServiceDietInfo'
SCHOOL_URL = '/schoolInfo'

# default option
OPTION = '?Type=json&Key=1475950391944d1c8831b761ade19ff6&ATPT_OFCDC_SC_CODE=B10'

# start & end date
MLSV_FROM_YMD = '20210103'
MLSV_TO_YMD = '20210105'

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


def getMealDataWithSchoolCode(SD_SCHUL_CODE):
    url = BASE_URL + MEAL_URL + OPTION + \
        '&pIndex=1&pSize=1000&SD_SCHUL_CODE=' + SD_SCHUL_CODE

    res = requests.get(url).json()

    if "mealServiceDietInfo" not in res:
        print("no data with School Code : " + SD_SCHUL_CODE)
        return []

    mealResDataList = res["mealServiceDietInfo"][1]["row"]

    mealDataList = []

    for mealResData in mealResDataList:
        data = []
        data.append(mealResData["SCHUL_NM"])
        data.append(mealResData["MLSV_YMD"])
        data.append(mealResData["MMEAL_SC_NM"])
        data.append(re.sub('\([^)]*\)', '',
                    mealResData["DDISH_NM"]).replace('  <br/>', ', '))
        data.append(mealResData["CAL_INFO"])
        mealDataList.append(data)

    print("schoolCode : " + SD_SCHUL_CODE + "success!")
    return mealDataList


def main():
    getSchoolCodeList()

    p = Pool(processes=12)
    tempList = []
    for SD_SCHUL_CODE in SD_SCHUL_CODE_LIST:
        tempList.append(getMealDataWithSchoolCode(SD_SCHUL_CODE))
    # tempresult = p.map(getMealDataWithSchoolCode, SD_SCHUL_CODE_LIST)

    result = list(itertools.chain(*tempList))
    resultDataFrame = pd.DataFrame(result, columns=['학교명, 날짜, 구분, 메뉴, 칼로리'])

    file_name = './nuvi_schoolmeal.xlsx'
    resultDataFrame.to_excel(file_name)


if __name__ == "__main__":
    main()
