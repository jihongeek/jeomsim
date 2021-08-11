import requests
from math import sqrt

class invalidResponse(Exception):
    pass

def getLocation(apiUrl,address):
    """
        VWorld Geocoder 2.0 Api를 이용하여 좌표를 가져오는 함수
    """
    apiResponse = requests.get(apiUrl+f"&address={address}").json()['response']
    if apiResponse['status'] == "OK":
        location = apiResponse['result']['point']
        location.update({'x': float(location['x']), 'y': float(location['y'])})
    else:
        raise invalidResponse
    
    return location

def getDistance(homeLocation,placeLocation):
    """
        homeLocation(기준인 장소의 좌표)와 placeLocation(비교 장소의 좌표) 간에 거리를 구하는 함수
    """
    return sqrt((homeLocation['x'] - placeLocation['x'])**2 + (homeLocation['y'] - placeLocation['y'])**2) 

