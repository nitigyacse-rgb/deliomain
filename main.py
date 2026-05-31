import json
import unittest
import datetime

# Use the open function to open and read the three json files
with open("./data-1.json", "r" , encoding="utf-8") as f:
    jsonData1 = json.load(f)
with open("./data-2.json", "r", encoding="utf-8") as f:
    jsonData2 = json.load(f)
with open("./data-result.json", "r", encoding="utf-8") as f:
    jsonExpectedResult = json.load(f)

def convertFromFormat1(jsonObject):
    # Split the location string by "/"
    locationParts = jsonObject['location'].split('/')
    
    result = {
        'deviceID': jsonObject['deviceID'],
        'deviceType': jsonObject['deviceType'],
        'timestamp': jsonObject['timestamp'],
        'location': {
            'country': locationParts[0],
            'city': locationParts[1],
            'area': locationParts[2],
            'factory': locationParts[3],
            'section': locationParts[4]
        },
        'data': {
            'status': jsonObject['operationStatus'],
            'temperature': jsonObject['temp']
        }
    }
    return result

def convertFromFormat2(jsonObject):
    # Format 2 timestamp string: "2021-06-23T10:57:17.783Z"
    # Replace 'Z' with standard UTC offset form '+00:00' for reliable parsing
    iso_string = jsonObject['timestamp'].replace('Z', '+00:00')
    dt = datetime.datetime.fromisoformat(iso_string)
    
    # Target requires milliseconds since epoch as an integer
    timestamp_ms = int(dt.timestamp() * 1000)
    
    result = {
        'deviceID': jsonObject['device']['id'],
        'deviceType': jsonObject['device']['type'],
        'timestamp': timestamp_ms,
        'location': {
            'country': jsonObject['country'],
            'city': jsonObject['city'],
            'area': jsonObject['area'],
            'factory': jsonObject['factory'],
            'section': jsonObject['section']
        },
        'data': {
            'status': jsonObject['data']['status'],
            'temperature': jsonObject['data']['temperature']
        }
    }
    return result

def main(jsonObject):
    # Direct routing based on structural signature
    if 'device' in jsonObject:
        return convertFromFormat2(jsonObject)
    else:
        return convertFromFormat1(jsonObject)

# Test cases using unittest module
class TestSolution(unittest.TestCase):
    
    def test_sanity(self):
        result = json.loads(json.dumps(jsonExpectedResult))
        self.assertEqual(result, jsonExpectedResult)
        
    def test_dataType1(self):
        result = main(jsonData1)
        self.assertEqual(result, jsonExpectedResult, 'Converting from Type 1 failed')
        
    def test_dataType2(self):
        result = main(jsonData2)
        self.assertEqual(result, jsonExpectedResult, 'Converting from Type 2 failed')

if __name__ == '__main__':
    unittest.main()