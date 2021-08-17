import requests
from math import sqrt

class invalidResponse(Exception):
    pass

def comparePlaces(place1,place2):
    """
        장소 두 곳을 비교해서(거리 : Column 3,가격대 : Column 1) 
        place1이 더 가격대,거리가 나으면 -1, place2가 낫거나 같으면 1를 리턴하는 함수   
    """
    distancePlace1,distancePlace2 = float(place1[3]),float(place2[3])
    if distancePlace1 < distancePlace2:
        return -1
    elif distancePlace1 > distancePlace2:
        return 1
    else:
        if place1[1] < place2[1]:
            return -1
        else:
            return 1
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

