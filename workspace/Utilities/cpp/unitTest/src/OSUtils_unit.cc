// SYSTEM INCLUDES
#include <gtest/gtest.h>

// C++ PROJECT INCLUDES
#include "Utilities/OSUtils.h"

namespace Utilities
{
namespace OS
{
namespace Tests
{

    TEST(Utilities_OS_Tests, GetCurrentDirectoryTest)
    {
        std::string emptyStr = "";
        EXPECT_EQ("", GetCurrentDirectory(emptyStr));

        // windows version
        std::string winDir = "C:\\Users\\foo\\dummy_file.txt";
        EXPECT_EQ("C:\\Users\\foo", GetCurrentDirectory(winDir));

        // unix version
        std::string unixDir = "/Users/foo/dummy_file.txt";
        EXPECT_EQ("/Users/foo", GetCurrentDirectory(unixDir));
    }

    TEST(Utilities_OS_Tests, GetPathSepTest)
    {
        std::string pathSep;
        #if defined _WIN32 || defined __CYGWIN__ || defined _WIN64
            pathSep = "\\";
        #else
            pathSep = "/";
        #endif
        EXPECT_EQ(pathSep, GetPathSep());
    }

    TEST(Utilities_OS_Tests, GetPathDelimiterTest)
    {
        std::string pathDelim;
        #if defined _WIN32 || defined __CYGWIN__ || defined _WIN64
            pathDelim = ";";
        #else
            pathDelim = ":";
        #endif
        EXPECT_EQ(pathDelim, GetPathDelimiter());
    }

} // end of namespace Tests
} // end of namespace OS
} // end of namespace Utilities
