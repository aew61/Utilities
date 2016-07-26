// SYSTEM INCLUDES
#include <gtest/gtest.h>

// C++ PROJECT INCLUDES
#include "Utilities/AddInts.h"

namespace Utilities
{
namespace UnitTest
{

    TEST(SimpleUtilitiesTest, TestAddInts)
    {
        EXPECT_EQ(8, AddInts(5, 3));
    }

} // end of namespace UnitTest
} // end of namespace Utilities
