#include <iostream>
#include <omp.h>

alignas(64) volatile int shared_counter = 0;

int main()
{
#pragma omp parallel num_threads(4)
    {
        int id = omp_get_thread_num();

        for (int i = 0; i < 1000000; i++)
        {
#pragma omp atomic
            shared_counter++;
        }

#pragma omp critical
        std::cout << "Thread " << id << " finished\n";
    }

    std::cout << "Counter = " << shared_counter << std::endl;

    return 0;
}
