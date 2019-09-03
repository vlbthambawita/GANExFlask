import json

def loadGans(jsonPath):
    ganArray = []
    with open(jsonPath) as f:
        ganDict = json.load(f)
        for key, value in ganDict.items():
            ganArray.append((key, value))
        f.close()

    return ganArray