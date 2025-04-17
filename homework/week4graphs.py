from typing import List, Generator


def merge_sort(nums: List[int]) -> Generator[int, None, None]:
    if len(nums) <= 1:
        yield from nums
        return

    # Split and sort
    s = len(nums) // 2
    A = merge_sort(nums[:s])
    B = merge_sort(nums[s:])

    # We know there's at least 1 item in any recursed array, so this is always safe
    vA = next(A)
    vB = next(B)
    while True:
        if vA <= vB:
            yield vA
            try:
                vA = next(A)
            except StopIteration:
                yield vB
                yield from B
                return
        else:
            yield vB
            try:
                vB = next(B)
            except StopIteration:
                yield vA
                yield from A
                return


import time


def worst_case_test(n: int) -> float:
    array = list(range(n, 0, -1))
    start = time.time()
    list(merge_sort(array))
    end = time.time()
    return end - start


import matplotlib.pyplot as plt

Ns = [1, 10, 100, 500] + list(range(1000, 10000, 500))
Ts = [worst_case_test(n) for n in Ns]

plt.plot(Ns, Ts)
plt.xlabel("Array Size")
plt.ylabel("Runtime (seconds)")
plt.title("Performance")
plt.show()
