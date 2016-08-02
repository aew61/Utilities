// SYSTEM INCLUDES
#include <chrono>
#include <gtest/gtest.h>
#include <thread>
#include <vector>

// C++ PROJECT INCLUDES
#include "Utilities/Semaphore.h"
#include "CommonMemory.h"
#include "Waiter.h"
#include "Signaler.h"

namespace Utilities
{
namespace Tests
{

    TEST(Utilities_Semaphore_Tests, SemaphoreConstructorTest)
    {
        Semaphore sem(3);

        EXPECT_NE(nullptr, &sem);
    }

    TEST(Utilities_Semaphore_Tests, SemaphoreGetCountTest)
    {
        Semaphore sem(3);
        EXPECT_EQ(3, sem.GetCount());

        Semaphore sem2(5);
        EXPECT_EQ(5, sem2.GetCount());
    }

    TEST(Utilities_Semaphore_Tests, LinearSemaphoreTest)
    {
        int numThreads = 12;
        int numSignalers = numThreads >> 1;
        int numWaiters = numThreads >> 1;

        CommonMemory* pCommon = new CommonMemory(0);
        EXPECT_EQ(0, pCommon->_sem.GetCount());

        std::vector<std::thread> threads(numSignalers + numWaiters);
        for(int i = 0; i < numWaiters; ++i)
        {
            threads[i] = std::thread(&Waiter, pCommon);
        }
        std::this_thread::sleep_for(std::chrono::seconds(1));

        EXPECT_EQ(-numWaiters, pCommon->_sem.GetCount());

        for(int i = 0; i < numSignalers; ++i)
        {
            threads[numWaiters + i] = std::thread(&Signaler, pCommon);
        }
        for(int i = 0; i < numSignalers + numWaiters; ++i)
        {
            if(threads[i].joinable())
            {
                threads[i].join();
            }
        }
        EXPECT_EQ(0, pCommon->_sem.GetCount());
        delete pCommon;
    }

    TEST(Utilities_Semaphore_Tests, InterleavedSemaphoreTest)
    {
        int numThreads = 12;
        CommonMemory* pCommon = new CommonMemory(0);
        int count = 0;
        EXPECT_EQ(count, pCommon->_sem.GetCount());

        std::vector<std::thread> threads(numThreads);
        std::thread additionalSignaler;
        for(int i = 0; i < numThreads; ++i)
        {
            if(i % 2 == 0)
            {
                threads[i] = std::thread(&Waiter, pCommon);
                std::this_thread::sleep_for(std::chrono::seconds(1));
                EXPECT_EQ(--count, pCommon->_sem.GetCount());
            }
            else
            {
                threads[i] = std::thread(&Signaler, pCommon);
                std::this_thread::sleep_for(std::chrono::seconds(1));
                EXPECT_EQ(++count, pCommon->_sem.GetCount());
            }
        }
        if(numThreads % 2 != 0)
        {
            additionalSignaler = std::thread(&Signaler, pCommon);
        }
        for(int i = 0; i < numThreads; ++i)
        {
            if(threads[i].joinable())
            {
                threads[i].join();
            }
        }
        if(additionalSignaler.joinable())
        {
            additionalSignaler.join();
        }
        EXPECT_EQ(0, count);
        EXPECT_EQ(count, pCommon->_sem.GetCount());
        delete pCommon;
    }

} // end of namespace UnitTest
} // end of namespace Utilities
