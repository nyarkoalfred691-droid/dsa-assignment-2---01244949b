"""
Part B: Arrays and the Two-Pointer Technique
ATU Library Book Management System
"""


def binary_search(arr, target):
    """
    Returns the index of target in sorted arr, or -1 if not found.
    Runs in O(log N) time.

    Best case: O(1) - target is the middle element on the first check.
    Worst case: O(log N) - target is at an extreme end or absent, and
    the search interval must be halved down to a single element.
    """
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1


def find_pair_with_sum(arr, target):
    """
    Two-pointer search on a SORTED array for two distinct values that
    sum to target. Returns a tuple (value_left, value_right) or None.
    Runs in O(N) time, O(1) additional space.
    """
    left, right = 0, len(arr) - 1
    while left < right:
        current_sum = arr[left] + arr[right]
        if current_sum == target:
            return (arr[left], arr[right])
        elif current_sum < target:
            left += 1
        else:
            right -= 1
    return None


def rotate_array(arr, k):
    """
    Rotates arr to the right by k positions, in place.
    Uses the triple-reversal technique: O(N) time, O(1) space.
    """
    n = len(arr)
    if n == 0:
        return arr
    k = k % n

    def reverse(a, i, j):
        while i < j:
            a[i], a[j] = a[j], a[i]
            i += 1
            j -= 1

    reverse(arr, 0, n - 1)      # reverse whole array
    reverse(arr, 0, k - 1)      # reverse first k elements
    reverse(arr, k, n - 1)      # reverse remaining elements
    return arr


if __name__ == "__main__":
    catalogue = [-8, -3, 0, 1, 4, 6, 9, 12, 15, 21]

    print("B1: binary_search")
    print("  search for 9  ->", binary_search(catalogue, 9))   # Output: 6
    print("  search for 5  ->", binary_search(catalogue, 5))   # Output: -1

    print("\nB2: find_pair_with_sum (target = 13)")
    print("  result ->", find_pair_with_sum(catalogue, 13))    # Output: (-8, 21)

    print("\nB3: rotate_array")
    sample = [1, 2, 3, 4, 5]
    print("  rotate [1,2,3,4,5] by 2 ->", rotate_array(sample, 2))  # Output: [4, 5, 1, 2, 3]
