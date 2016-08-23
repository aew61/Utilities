import os
import requests
import sys

currentDir = os.path.dirname(os.path.realpath(__file__))
buildScriptsDir = os.path.join(currentDir, "build", "scripts")


def parseValue(stringValue):
        if "u'" in stringValue:
            return stringValue[2:-1]
        elif "." in stringValue:
            return float(stringValue)
        else:
            return int(stringValue)

def parseDict(dictData, keysToKeep, keysToIgnore):
    returnDict = {}
    dictPairs = dictData.strip().split(",")
    for pair in dictPairs:
        key, value = pair.strip().split(":")
        key = key[2:-1]  # all keys are strings so they have u'<key>'. Get rid of the u''
        if (key in keysToKeep and len(keysToKeep) > 0) or\
           (key not in keysToIgnore and len(keysToIgnore) > 0) or\
           (key == "relativeUrl" or key == "fileName" or key == "filetype") and key != "_id":
            returnDict[key] = parseValue(value.strip())

    return returnDict

def parseQueryData(marshalledQueryData, keysToKeep=[], keysToIgnore=[]):
    parsedQueryData = []
    marshalledQueryData = marshalledQueryData.replace("[", "").replace("]", "")
    splitDictData = marshalledQueryData.split("},")
    splitDictData[-1] = splitDictData[-1][:-1]
    for dictData in splitDictData:
        parsedQueryData.append(parseDict(dictData.strip()[1:], keysToKeep, keysToIgnore))

    return parsedQueryData

def urljoin(url, *urls):
    urlList = [url]
    urlList.extend([urlPart for urlPart in urls])
    unrefinedUrl = '/'.join(urlList).strip()
    unrefinedUrl = unrefinedUrl.replace("//", "/")
    return unrefinedUrl.replace("http:/", "http://")


def downloadRBuild():
    import tarfile

    downloadedBuildScriptsPath = os.path.join(buildScriptsDir, "downloads")
    if not os.path.exists(downloadedBuildScriptsPath):
        os.makedirs(downloadedBuildScriptsPath)
    # client = pymongo.MongoClient(os.environ["MONGODB_URI"])
    # db = client["rbuild"]
    # coll = db["src"]
    # mostRecentBuildScriptsRecord = [x for x in coll.find(
    #     {
    #         "config": "src"
    #     }
    # ).sort("build_num")][-1]
    dbParams = {
        "dbkey_config": "src",
        "collectionName": "src",
        "dbName": "rbuild"
    }
    auth = requests.auth.HTTPBasicAuth(os.environ["DBFILESERVER_USERNAME"],
                                       os.environ["DBFILESERVER_PASSWORD"])
    response = requests.request("QUERY", os.environ["FILESERVER_URI"], data=dbParams, auth=auth)
    mostRecentRecord = sorted(parseQueryData(response.content, keysToKeep=["major_version", "minor_version",
                                                                           "patch", "build_num"]),
                              key=lambda record: [int(record["major_version"]),
                                                  int(record["minor_version"]),
                                                  int(record["patch"]), int(record["build_num"])])[-1]
    filePath = os.path.join(downloadedBuildScriptsPath,
                            mostRecentRecord["fileName"] + mostRecentRecord["filetype"])
    response = requests.get(urljoin(os.environ["FILESERVER_URI"], "rbuild/",
                                    mostRecentRecord["fileName"] + mostRecentRecord["filetype"]),
                            stream=True, auth=auth)

    numBytes = len(response.content)
    currentBytes = 0.0
    minPercentToPrint = 0
    print("Downloading rbuild_%s.%s.%s.%s" % (mostRecentRecord["major_version"], mostRecentRecord["minor_version"],
                                              mostRecentRecord["patch"], mostRecentRecord["build_num"]))
    print("Starting download (%s bytes):" % numBytes)
    with open(filePath, "wb") as f:
        for chunk in response.iter_content(numBytes / 10):
            if currentBytes/numBytes >= minPercentToPrint:
                print("[%s%%]" % int(currentBytes/numBytes * 100)),
                minPercentToPrint += 0.1
            f.write(chunk)
            currentBytes += len(chunk)
    print("Download done")
    with tarfile.open(filePath, "r:gz") as tarFile:
        # extract out scripts and config dirs and move it to currentDir/build
        tarFile.extractall(path=os.path.join(currentDir, "build"),
                           members=[x for x in tarFile.getmembers() if "license" not in x.name.lower()\
                                    and "readme" not in x.name.lower()])


def updateRBuild():
    if not os.path.exists(buildScriptsDir):
        os.makedirs(buildScriptsDir)
        return True
    # if this method is called, can safely assume build/scripts/ exists
    # client = pymongo.MongoClient(os.environ["MONGODB_URI"])
    # db = client["BuildScripts"]
    # coll = db["src"]
    # mostRecentBuildScriptsRecord = [x for x in coll.find(
    #     {
    #         "config": "src"
    #     }
    # ).sort("build_num")][-1]
    dbParams = {
        "dbkey_config": "src",
        "collectionName": "src",
        "dbName": "rbuild"
    }
    auth = requests.auth.HTTPBasicAuth(os.environ["DBFILESERVER_USERNAME"],
                                       os.environ["DBFILESERVER_PASSWORD"])
    response = requests.request("QUERY", os.environ["FILESERVER_URI"], data=dbParams, auth=auth)
    mostRecentRecord = sorted(parseQueryData(response.content, keysToKeep=["major_version", "minor_version",
                                                                           "patch", "build_num"]),
                              key=lambda record: [int(record["major_version"]),
                                                  int(record["minor_version"]),
                                                  int(record["patch"]), int(record["build_num"])])[-1]
    mostRecentBuildNum = [int(mostRecentRecord["major_version"]),
                          int(mostRecentRecord["minor_version"]),
                          int(mostRecentRecord["patch"]),
                          int(mostRecentRecord["build_num"])]
    print("Most recent BuildScripts version: %s" % mostRecentBuildNum)
    allVersions = os.listdir(os.path.join(buildScriptsDir, "downloads"))
    if len(allVersions) == 0:
        return True
    downloadedVersions = [[int(x) for x in version.split("_")[1].split(".")]
                          for version in allVersions]
    currentBuild = max(downloadedVersions)
    print("Currently have BuildScripts version: %s" % currentBuild)
    return mostRecentBuildNum > currentBuild
    

def checkRBuildVersion():
    if updateRBuild():
        downloadRBuild()
