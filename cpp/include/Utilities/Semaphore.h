#pragma once
#ifndef UTILITIES_SEMAPHORE_H
#define UTILITIES_SEMAPHORE_H

// SYSTEM INCLUDES
#include <atomic>
#include <mutex>
#include <condition_variable>

// C++ PROJECT INCLUDES
#include "Utilities/LibraryExport.h"

namespace Utilities
{

    class UTILITIES_API Semaphore
    {
    public:

        Semaphore(int count);

        ~Semaphore();

        void Wait();

        void Signal();

        int GetCount();

    private:

        std::atomic<int>        _count;
        std::atomic<bool>       _trigger;
        std::condition_variable _cv;
        std::mutex              _mutex;

    };

} // end of namespace Utilities

#endif // end of UTILITIES_SEMAPHORE_H