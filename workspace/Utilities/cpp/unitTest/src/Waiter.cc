// SYSTEM INCLUDES

// C++ PROJECT INCLUDES
#include "Waiter.h"

namespace Utilities
{
namespace Tests
{

    void Waiter(CommonMemory* pCommon)
    {
        pCommon->_sem.Wait();
    }

} // end of namespace Tests
} // end of namespace Utilities
