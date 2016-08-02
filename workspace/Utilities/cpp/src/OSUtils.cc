// SYSTEM INCLUDES


// C++ PROJECT INCLUDES
#include "Utilities/OSUtils.h"

namespace Utilities
{
namespace OS
{

    std::string GetCurrentDirectory(const std::string pathToFile)
    {
        int indexOfLastPath = -1;
        for(int i = pathToFile.length() - 1; i > -1 && indexOfLastPath == -1; --i)
        {
            if(pathToFile.at(i) == '\\' || pathToFile.at(i) == '/')
            {
                indexOfLastPath = i;
            }
        }
        return pathToFile.substr(0, indexOfLastPath);
    }

    const std::string GetPathSep()
    {
        #if defined _WIN32 || defined __CYGWIN__ || defined _WIN64
            return "\\";
        #else
            return "/";
        #endif
    }

    const std::string GetPathDelimiter()
    {
        #if defined _WIN32 || defined __CYGWIN__ || defined _WIN64
            return ";";
        #else
            return ":";
        #endif
    }

} // end of namespace OS
} // end of namespace Utilities
