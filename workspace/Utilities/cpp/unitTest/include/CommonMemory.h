#pragma once
#ifndef UTILITIES_TESTS_COMMONMEMORY_H
#define UTILITIES_TESTS_COMMONMEMORY_H


// SYSTEM INCLUDES


// C++ PROJECT INCLUDES
#include "Utilities/Semaphore.h"

namespace Utilities
{
namespace Tests
{

    struct CommonMemory
    {
        Semaphore _sem;

        CommonMemory(int semInit);

        ~CommonMemory();
    };

} // end of namespace Tests
} // end of namespace Utilities

#endif // end of UTILITIES_TEST_COMMONMEMORY_H
