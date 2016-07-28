
# SYSTEM IMPORTS
import os
import pymongo
import sys


currentDir = os.path.dirname(os.path.realpath(__file__))
buildScriptsDir = os.path.join(currentDir, "build", "scripts")


def urljoin(url, *urls):
    urlList = [url]
    urlList.extend([urlPart for urlPart in urls])
    unrefinedUrl = '/'.join(urlList).strip()
    unrefinedUrl = unrefinedUrl.replace("//", "/")
    return unrefinedUrl.replace("http:/", "http://")


def downloadBuildScripts():
    import requests
    import tarfile

    downloadedBuildScriptsPath = os.path.join(buildScriptsDir, "downloads")
    if not os.path.exists(downloadedBuildScriptsPath):
        os.makedirs(downloadedBuildScriptsPath)
    client = pymongo.MongoClient(os.environ["MONGODB_URI"])
    db = client["BuildScripts"]
    coll = db["src"]
    mostRecentBuildScriptsRecord = [x for x in coll.find(
        {
            "config": "src"
        }
    ).sort("build_num")][-1]
    filePath = os.path.join(downloadedBuildScriptsPath,
                            mostRecentBuildScriptsRecord["fileName"] + mostRecentBuildScriptsRecord["filetype"])
    response = requests.get(urljoin(os.environ["FILESERVER_URI"], "BuildScripts/",
                                    mostRecentBuildScriptsRecord["fileName"] + mostRecentBuildScriptsRecord["filetype"]),
                            stream=True,
                            auth=requests.auth.HTTPBasicAuth(os.environ["DBFILESERVER_USERNAME"],
                                                             os.environ["DBFILESERVER_PASSWORD"]))

    numBytes = len(response.content)
    currentBytes = 0.0
    minPercentToPrint = 0
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


def updateBuildScripts():
    if not os.path.exists(buildScriptsDir):
        os.makedirs(buildScriptsDir)
        return True
    # if this method is called, can safely assume build/scripts/ exists
    client = pymongo.MongoClient(os.environ["MONGODB_URI"])
    db = client["BuildScripts"]
    coll = db["src"]
    mostRecentBuildScriptsRecord = [x for x in coll.find(
        {
            "config": "src"
        }
    ).sort("build_num")][-1]
    mostRecentBuildNum = [mostRecentBuildScriptsRecord["major_version"],
                          mostRecentBuildScriptsRecord["minor_version"],
                          mostRecentBuildScriptsRecord["patch"],
                          mostRecentBuildScriptsRecord["build_num"]]
    print("Most recent BuildScripts version: %s" % mostRecentBuildNum)
    allVersions = os.listdir(os.path.join(buildScriptsDir, "downloads"))
    if len(allVersions) == 0:
        return True
    downloadedVersions = [[int(x) for x in version.split("_")[1].split(".")]
                          for version in allVersions]
    currentBuild = max(downloadedVersions)
    print("Currently have BuildScripts version: %s" % currentBuild)
    return mostRecentBuildNum > currentBuild
    

if updateBuildScripts():
    downloadBuildScripts()
sys.path.extend([currentDir, buildScriptsDir])  # now we can import modules from <currentDirectory>/scripts


# PYTHON PROJECT IMPORTS
import ProjectBuild
import Utilities
import FileSystem


class LocalBuild(ProjectBuild.ProjectBuild):
    def __init__(self):
        super(LocalBuild, self).__init__("Utilities")
        self._build_steps = [self.build,
                             self.runUnitTests,
                             self.package,
                             self.uploadPackagedVersion]
        self._tests_to_run = ["Utilities_unit"]

    # def generateConfig(self, asyncConfigPath=None, asyncConfigFileName=None):
    #     outIncludeDir = os.path.join(FileSystem.getDirectory(FileSystem.OUT_ROOT),
    #                                  "include")
    #     projectLogDir = FileSystem.getDirectory(FileSystem.LOG_DIR, self._config, self._project_name)
    #     asyncConfig = None
    #     if asyncConfigPath is None:
    #         asyncConfig = os.path.join(FileSystem.getDirectory(FileSystem.CLIENT_CONFIG),
    #                                    (asyncConfigFileName if asyncConfigFileName is not None else "AsyncConfig.xml"))
    #     else:
    #         asyncConfig = asyncConfigPath
    #     Utilities.mkdir(outIncludeDir)

    #     configArgs = []

    #     configArgs.append(['std::string', 'LOGGING_ROOT', 'dir', projectLogDir.replace("\\", "/")])
    #     if "Robos" in self._project_name:
    #         configArgs.append(['std::string', 'ASYNC_CONFIG_PATH', 'file', asyncConfig.replace("\\", "/")])

    #     (formattedConfigArgsHeader, formattedConfigArgsSrc) = self.checkConfigArgsAndFormat("\t", configArgs)

    #     if os.path.exists(projectLogDir):
    #         Utilities.rmTree(projectLogDir)
    #     Utilities.mkdir(projectLogDir)
    #     projNameUpper = self._project_name.upper()
    #     with open(os.path.join(outIncludeDir, self._project_name + "Config.hpp"), 'w') as file:
    #         file.write("#pragma once\n"
    #                    "#ifndef " + projNameUpper + "_CONFIG_" + projNameUpper + "CONFIG_HPP\n"
    #                    "#define " + projNameUpper + "_CONFIG_" + projNameUpper + "CONFIG_HPP\n\n"
    #                    "// SYSTEM INCLUDES\n"
    #                    "#include <string>\n\n"
    #                    "// C++ PROJECT INCLUDES\n\n"
    #                    "namespace " + self._project_name + "\n"
    #                    "{\n"
    #                    "namespace Config\n"
    #                    "{\n\n" +
    #                    formattedConfigArgsHeader +
    #                    "} // end of namespace Config\n"
    #                    "} // end of namespace " + self._project_name + "\n"
    #                    "#endif // end of " + projNameUpper + "_CONFIG_" + projNameUpper + "CONFIG_HPP\n")
    #     with open(os.path.join(outIncludeDir, self._project_name + "Config.cpp"), 'w') as file:
    #         file.write("// SYSTEM INCLUDES\n\n"
    #                    "// C++ PROJECT INCLUDES\n"
    #                    "#include \"" + self._project_name + "Config.hpp\"\n\n"
    #                    "namespace " + self._project_name + "\n"
    #                    "{\n"
    #                    "namespace Config\n"
    #                    "{\n\n" +
    #                    formattedConfigArgsSrc +
    #                    "} // end of namespace Config\n"
    #                    "} // end of namespace " + self._project_name + "\n")

    def customSetupWorkspace(self):
        print("Setting up workspaces for project [%s]" % self._project_name)
        self.cleanBuildWorkspace()
        Utilities.mkdir(FileSystem.getDirectory(FileSystem.WORKING, self._config, self._project_name))
        self.loadDependencies(self.parseDependencyFile())

    # def customPreBuild(self, asyncConfigPath=None, asyncConfigFileName=None):
    #     self.customSetupWorkspace()
    #     self.generateProjectVersion()
    #     self.generateConfig(asyncConfigPath, asyncConfigFileName)

    def help(self):
        super(LocalBuild, self).help()

if __name__ == "__main__":
    customCommands = Utilities.parseCommandLine(sys.argv[1:])
    print(customCommands)

    localBuild = LocalBuild()
    localBuild.run(customCommands)
