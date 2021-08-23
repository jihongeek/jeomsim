import requests,sys,random,os,gspread,datetime,json
from functools import cmp_to_key
from oauth2client.service_account import ServiceAccountCredentials
from place import comparePlaces

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
stableWorksheet = spreadsheet.worksheet('stable')
# 웹훅 Url 환경변수에서 가져오기
webhookUrl = os.getenv('WEBHOOK_URL') 

stablePlaces = stableWorksheet.get_values()[1:]
# 장소를 랜덤하게 섞은 다음 5개 뽑아서 정렬 
for _ in range(random.randint(1,100)):
    random.shuffle(stablePlaces)
pickedPlaces = sorted(stablePlaces[:5],key=cmp_to_key(comparePlaces))

# 시간 설정 : UTC + 9 
todayTime = datetime.datetime.now() + datetime.timedelta(seconds=32400)

# 디스코드 Embed Object
embedObject = {
    "title" : "오늘의 점심 식당 :rice_ball:  추천 리스트 :triangular_flag_on_post:",
    "description": f"{todayTime.year}년 {todayTime.month}월 {todayTime.day}일자 추천 리스트 입니다.",
    "color" : 15105570, # ORANGE
    "fields" : [],
    "footer" : {"text" : f"Jeomsim {todayTime.year}"}
} 
# Embed Object의 fields에 장소 넣기
for index,place in enumerate(pickedPlaces):
    embedObject['fields'].append({ "name" : f"__**{index+1}.**__ 상호명 : *{place[0]}*", "value" : f"가격대 : {place[1]}\n대략적 위치 : {place[2]}\n[네이버 지도 링크]({place[4]})"})

# http 헤더 설정
header = {"Content-Type" : "application/json"}

if requests.request("POST",webhookUrl,data=json.dumps({"content" : "", "embeds" : [embedObject]}),headers=header).ok:
    print("성공적으로 리스트를 웹훅으로 보냈습니다.")
else:
    print("리스트 보내기를 실패했습니다.")
    sys.exit(1)



