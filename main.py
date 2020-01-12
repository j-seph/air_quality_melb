import requests
import json
import os
import math

TOKEN = os.environ.get('aqicn_token')
LOCATION = {
    'australia/melbourne/melbourne-cbd': 'Melbourne CBD'
}
AQI_MAPPING = {
    'Good': (0, 50),
    'Moderate': (51, 100),
    'Unhealthy for Sensitive Groups': (101, 150),
    'Unhealthy': (151,200),
    'Very Unhealthy': (201, 300),
    'Hazardous': (301, math.inf) 
}

response = requests.get('https://api.waqi.info/feed/' + list(LOCATION.keys())[0] + '/?token=' + TOKEN)
response_json = response.json()

AQI = response_json['data']['aqi']
AQI_NAME = None
PM25 = response_json['data']['iaqi']['pm25']['v']

if AQI > 50:
    for level, ranges in AQI_MAPPING.items():
        if ranges[0] <= AQI <= ranges[1]:
            AQI_NAME = level
            break

    data = {
        'text': LOCATION['australia/melbourne/melbourne-cbd'] + '\nAQI: ' + str(AQI) + ' (' + AQI_NAME + ')' '\nPM2.5: ' + str(PM25)
    }

    webhook = os.environ.get('webhook_slack')
    requests.post(webhook, json.dumps(data))