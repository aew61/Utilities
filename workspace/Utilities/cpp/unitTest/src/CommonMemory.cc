// SYSTEM INCLUDES


// C++ PROJECT INCLUDES
#include "CommonMemory.h"

namespace Utilities
{
namespace Tests
{

    CommonMemory::CommonMemory(int semInit) : _sem(semInit)
    {
    }

    CommonMemory::~CommonMemory()
    {
    }

} // end of namespace Tests
} // end of namespace Utilities
