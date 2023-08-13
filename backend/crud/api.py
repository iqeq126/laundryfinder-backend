from urllib.parse import urlencode, unquote, quote_plus
import requests

serviceKey = "RCRS2BYQrxm9Ughup5pUew%2BQJljutDtoR2FFUrfs8MxNosEYPRHmBqLEWifOLl7vi6jgSc45OWHSmfZySLoUiQ%3D%3D"
serviceKeyDecoded = unquote(serviceKey, 'UTF-8')

def check_air():
    url = "http://apis.data.go.kr//1471000/FoodNtrIrdntInfoService1/getFoodNtrItdntList1"
    returnType="json"
    numOfRows="3"
    pageNo="1"

    queryParams = '?' + urlencode({ quote_plus('ServiceKey=') : serviceKeyDecoded, quote_plus('&numOfRows=') : numOfRows, quote_plus('&pageNo=') : pageNo, quote_plus('&type=') : returnType })
    res = requests.get(url + queryParams)
    json = res.text
    return json