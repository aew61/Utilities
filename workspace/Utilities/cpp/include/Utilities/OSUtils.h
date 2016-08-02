#pragma once
#ifndef UTILITIES_OSUTILS_H
#define UTILITIES_OSUTILS_H


// SYSTEM INCLUDES
#include <string>

// C++ PROJECT INCLUDES
#include "Utilities/LibraryExport.h"

namespace Utilities
{
namespace OS
{

    UTILITIES_API std::string GetCurrentDirectory(const std::string pathToFile);

    UTILITIES_API const std::string GetPathSep();

    UTILITIES_API const std::string GetPathDelimiter();

} // end of namespace OS
} // end of namespace Utilities

#endif // end of UTILITIES_OSUTILS_H
