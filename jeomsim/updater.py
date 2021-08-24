import gspread
import sys,os
from oauth2client.service_account import ServiceAccountCredentials
from place import * 
try:
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive',
    ]
    # 인증 관련 설정
    authDict = {  
      "type": os.getenv("GAUTH_TYPE"), 
      "project_id": os.getenv("GAUTH_PROJECT_ID"), 
      "private_key_id": os.getenv("GAUTH_PRIVATE_KEY_ID"), 
      "private_key": os.getenv("GAUTH_PRAIVATE_KEY").replace('\\n', '\n'),
      "client_email": os.getenv("GAUTH_CLIENT_EMAIL"),
      "client_id": os.getenv("GAUTH_CLINET_ID"),
      "auth_uri": "https://accounts.google.com/o/oauth2/auth",
      "token_uri": "https://oauth2.googleapis.com/token",
      "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
      "client_x509_cert_url": os.getenv("GAUTH_CLIENT_X509_CERT_URL")
    }
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(authDict,scope)

    # credentials을 통해 구글Api에 로그인하고 스프레드시트 가져오기
    spreadsheetURL = os.getenv('SHEET_URL')
    spreadsheet = gspread.authorize(credentials).open_by_url(spreadsheetURL)

    # 워크시트 선택하기
    addedWorksheet = spreadsheet.worksheet('added')
    stableWorksheet = spreadsheet.worksheet('stable')

    # VWorld Geocoder 2.0 Api 관련 설정
    apiKey = os.getenv("VWORLD_API_KEY")
    apiUrl = f"http://api.vworld.kr/req/address?service=address&request=getCoord&version=2.0&key={apiKey}&crs=EPSG:5179&refine=true&simple=true&format=json&type=road"
    
    # 기준 장소 설리
    homeAddress = os.getenv("HOME_ADDRESS")
    homeLocation = getLocation(apiUrl,homeAddress)
    
    # 중복된 장소를 확인하기 위해서 stable 워크시트의 네이버링크 가져와서 set으로 만들기
    setOfStableNaverLinks = set(stableWorksheet.col_values(5)[1:])
    # 마찬가지로 added 워크시트의 네이버링크를 저장할 set을 만든다.
    setOfAddedNaverLinks = set()
    
    # 추가 할 장소 골라내고 stable에 알맞은 row 형태로 만들기
    addedPlaces =  addedWorksheet.get_values()[1:]
    placesAddedToStable = []   
    for addedPlace in addedPlaces:
        if addedPlace[4] not in setOfStableNaverLinks and addedPlace[4] not in setOfAddedNaverLinks:
           placeLocation = getLocation(apiUrl,addedPlace[3]) 
           placesAddedToStable.append([addedPlace[1], addedPlace[2][0], addedPlace[3], getDistance(homeLocation,placeLocation), addedPlace[4]])
           setOfAddedNaverLinks.add(addedPlace[4]) 
    
    # stable 워크시트에 추가하기 
    stableWorksheet.append_rows(placesAddedToStable)
    # added 워크시트에 있던 장소 삭제
    addedWorksheet.delete_rows(2,2+len(addedPlaces)-1)

except invalidResponse:
    print("Geocoder 2.0 Api 응답에 문제가 발생했습니다.")
    sys.exit(1)