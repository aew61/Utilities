// SYSTEM INCLUDES

// C++ PROJECT INCLUDES
#include "Signaler.h"

namespace Utilities
{
namespace Tests
{

    void Signaler(CommonMemory* pCommon)
    {
        pCommon->_sem.Signal();
    }

} // end of namespace Tests
} // end of namespace Utilities