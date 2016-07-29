// SYSTEM INCLUDES
#include <gtest/gtest.h>

// C++ PROJECT INCLUDES
#include "Utilities/Semaphore.h"

namespace Utilities
{
namespace UnitTest
{

    TEST(UtilitiesTest, SimpleSemaphoreTest)
    {
        Semaphore sem(3);

        EXPECT_EQ(sem.GetCount(), 3) << "sem was initalized with a count of 3";
    }

} // end of namespace UnitTest
} // end of namespace Utilities
