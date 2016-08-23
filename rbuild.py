
# SYSTEM IMPORTS
import os
# import pymongo
import sys


currentDir = os.path.dirname(os.path.realpath(__file__))
buildScriptsDir = os.path.join(currentDir, "build", "scripts")
sys.path.extend([currentDir, buildScriptsDir])  # now we can import modules from <currentDirectory>/scripts


import getRBuild
getRBuild.checkRBuildVersion()


# PYTHON PROJECT IMPORTS
import ProjectBuild
import Utilities
import FileSystem


class LocalBuild(ProjectBuild.ProjectBuild):
    def __init__(self):
        super(LocalBuild, self).__init__("Utilities")
        self._cover = True
        self._build_steps = [self.build,
                             self.coverWithUnit,
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

    def customSetupWorkspace(self, node):
        print("Setting up workspaces for package [%s]" % node._name)
        self.cleanBuildWorkspace(node)
        Utilities.mkdir(FileSystem.getDirectory(FileSystem.WORKING, self._config, node._name))
        self.loadDependencies(node)

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
