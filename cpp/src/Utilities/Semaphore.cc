// SYSTEM INCLUDES


// C++ PROJECT INCLUDES
#include "Utilities/Semaphore.h"


namespace Utilities
{

    Semaphore::Semaphore(int count) : _count(count),
        _trigger(true), _cv(), _mutex()
    {
    }

    Semaphore::~Semaphore()
    {
    }

    void Semaphore::Wait()
    {
        std::unique_lock<std::mutex> mutexLock(this->_mutex);
        this->_count--;

        // std::condition_variable it notorious for having spurious wakeups.
        // this while loop prevents the semaphore from "signaling" due to
        // a spurious wakeup of the std::condition_variable. The _trigger
        // variable is necessary for this loop to work.
        while(this->_trigger && this->_count < 0)
        {
            this->_cv.wait(mutexLock);
        }

        // when thread/process is woken up..._trigger = false. We need
        // to set it back to true so that other threads/processes will not
        // be "signaled" by a spurious wakeup. This line has no effect
        // if a wait() call does not block.
        this->_trigger = true;
    }

    void Semaphore::Signal()
    {
        std::lock_guard<std::mutex> mutexLock(this->_mutex);
        if(++this->_count <= 0)
        {
            this->_trigger = false;
            this->_cv.notify_one();
        }
    }

    int Semaphore::GetCount()
    {
        std::lock_guard<std::mutex> mutexLock(this->_mutex);
        return this->_count;
    }

} // end of namespace Utilities
