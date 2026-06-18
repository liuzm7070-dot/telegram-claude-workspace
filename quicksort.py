"""
QuickSort implementation with multiple pivot strategies.
Includes Lomuto partition scheme and randomized pivot selection.
"""

import random
from typing import List, TypeVar

T = TypeVar('T')


def quicksort(arr: List[T], low: int = 0, high: int | None = None) -> List[T]:
    """
    In-place QuickSort using Lomuto partition with randomized pivot.

    Args:
        arr: The list to sort
        low: Start index (default 0)
        high: End index (default len(arr)-1)

    Returns:
        The sorted list (modified in-place)

    Time:  O(n log n) average, O(n²) worst case
    Space: O(log n) for recursion stack
    """
    if high is None:
        high = len(arr) - 1

    if low < high:
        pivot_idx = partition(arr, low, high)
        quicksort(arr, low, pivot_idx - 1)
        quicksort(arr, pivot_idx + 1, high)

    return arr


def partition(arr: List[T], low: int, high: int) -> int:
    """
    Lomuto partition: choose random pivot, place it at correct position,
    with all smaller elements to the left and larger to the right.
    """
    # Randomized pivot to avoid O(n²) on sorted arrays
    rand_idx = random.randint(low, high)
    arr[high], arr[rand_idx] = arr[rand_idx], arr[high]

    pivot = arr[high]
    i = low - 1  # index of smaller element

    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def mergesort(arr: List[T]) -> List[T]:
    """
    MergeSort — stable, guaranteed O(n log n).
    Returns a new sorted list (not in-place).
    """
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = mergesort(arr[:mid])
    right = mergesort(arr[mid:])

    return merge(left, right)


def merge(left: List[T], right: List[T]) -> List[T]:
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


if __name__ == '__main__':
    # Test QuickSort
    test_arr = [64, 34, 25, 12, 22, 11, 90]
    original = test_arr.copy()
    quicksort(test_arr)
    print(f"QuickSort: {original} → {test_arr}")
    assert test_arr == sorted(original), "QuickSort failed!"

    # Test MergeSort
    test_arr2 = [38, 27, 43, 3, 9, 82, 10]
    result = mergesort(test_arr2)
    print(f"MergeSort: {test_arr2} → {result}")
    assert result == sorted(test_arr2), "MergeSort failed!"

    print("✅ All sorting tests passed!")
