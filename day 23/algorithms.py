# 1. Linear Search - O(n) Time | O(1) Space
def linear_search(items: list, target) -> int:
    """Scans every single element sequentially."""
    for index, item in enumerate(items):
        if item == target:
            return index
    return -1


# 2. Binary Search - O(log n) Time | O(1) Space
def binary_search(sorted_items: list, target) -> int:
    """Divide and conquer by splitting a sorted array in half."""
    low, high = 0, len(sorted_items) - 1

    while low <= high:
        mid = (low + high) // 2
        guess = sorted_items[mid]
        
        if guess == target:
            return mid
        if guess > target:
            high = mid - 1
        else:
            low = mid + 1
            
    return -1


if __name__ == "__main__":
    data = [10, 20, 30, 40, 50, 60, 70, 80, 90]
    print(f"Testing Binary Search for 70: Index found at {binary_search(data, 70)}")

    # 3. Bubble Sort - O(n²) Time | O(1) Space
def bubble_sort(arr: list) -> list:
    """Repeatedly steps through the list, compares adjacent elements, and swaps."""
    n = len(arr)
    # Copy to avoid modifying the original list in-place if we want to preserve it
    res = arr.copy()
    for i in range(n):
        for j in range(0, n - i - 1):
            if res[j] > res[j + 1]:
                res[j], res[j + 1] = res[j + 1], res[j]
    return res


# 4. Merge Sort - O(n log n) Time | O(n) Space
def merge_sort(arr: list) -> list:
    """Divide and conquer stable sorting algorithm."""
    if len(arr) <= 1:
        return arr
        
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    return merge(left, right)

def merge(left: list, right: list) -> list:
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


# 5. Quick Sort - O(n log n) Avg Time | O(log n) Space
def quick_sort(arr: list) -> list:
    """Partitions data around a pivot element."""
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)


# Let's update our test block at the bottom
if __name__ == "__main__":
    # Previous search test
    search_data = [10, 20, 30, 40, 50, 60, 70, 80, 90]
    print(f"Binary Search Test for 70: Index {binary_search(search_data, 70)}")
    
    # New sort tests
    unsorted_data = [64, 34, 25, 12, 22, 11, 90]
    print(f"\nOriginal Unsorted List: {unsorted_data}")
    print(f"Bubble Sorted: {bubble_sort(unsorted_data)}")
    print(f"Merge Sorted:  {merge_sort(unsorted_data)}")
    print(f"Quick Sorted:  {quick_sort(unsorted_data)}")

# 6. Recursion Example: Factorial with Call Stack safety check
def recursive_factorial(n: int) -> int:
    """
    Calculates factorial using recursion.
    Base Case: n <= 1
    Recursive Case: n * structural breakdown of (n-1)
    """
    if n < 0:
        raise ValueError("Sorry, factorial does not exist for negative numbers.")
    if n <= 1:  # Base Case (The emergency brake)
        return 1
    return n * recursive_factorial(n - 1)  # Recursive Case


# 7. Two Pointers Technique - O(n) Time | O(1) Space
def has_target_pair(sorted_arr: list[int], target_sum: int) -> bool:
    """
    Finds if two numbers in a sorted array add up to a target sum.
    Eliminates the need for a slow O(n²) nested loop.
    """
    left = 0
    right = len(sorted_arr) - 1
    
    while left < right:
        current_sum = sorted_arr[left] + sorted_arr[right]
        if current_sum == target_sum:
            return True
        elif current_sum < target_sum:
            left += 1  # Sum is too small, move left pointer up
        else:
            right -= 1 # Sum is too big, move right pointer down
    return False


# 8. Sliding Window (Fixed) - O(n) Time | O(1) Space
def max_sum_subarray(arr: list[int], window_size: int) -> int:
    """
    Finds the maximum sum of any contiguous subarray of size K.
    Perfect analog for stream analytics or rate limit windows.
    """
    n = len(arr)
    if n < window_size:
        return -1
        
    # Sum of the very first window
    window_sum = sum(arr[:window_size])
    max_sum = window_sum
    
    # Slide the window across the rest of the array
    for i in range(n - window_size):
        # Subtract the element leaving the window, add the element entering
        window_sum = window_sum - arr[i] + arr[i + window_size]
        max_sum = max(max_sum, window_sum)
        
    return max_sum

# Append these checks into your existing __main__ execution block:
    print("\n--- Testing Advanced Patterns ---")
    print(f"Recursion (Factorial of 5): {recursive_factorial(5)}")
    
    sorted_pairs = [1, 2, 4, 6, 8, 11, 15]
    print(f"Two Pointers (Find sum 14 in {sorted_pairs}): {has_target_pair(sorted_pairs, 14)}")
    
    stream_data = [2, 1, 5, 1, 3, 2, 1, 1]
    print(f"Sliding Window (Max sum of 3 contiguous elements): {max_sum_subarray(stream_data, 3)}")

from collections import deque

# 9. Breadth-First Search (BFS) - O(V + E) Time | O(V) Space
def bfs_shortest_path(graph: dict[str, list], start: str, target: str) -> list[str] | None:
    """
    Explores the graph layer by layer using a Queue.
    Perfect for finding the shortest path or connection hops in a backend.
    """
    queue = deque([[start]])
    visited = set([start])

    while queue:
        path = queue.popleft()
        node = path[-1]

        if node == target:
            return path

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)
    return None


# 10. Depth-First Search (DFS) - O(V + E) Time | O(V) Space
def dfs_all_reachable(graph: dict[str, list], start: str, visited=None) -> set[str]:
    """
    Dives deep down a branch before backtracking using a Stack (via recursion).
    Perfect for tracking hierarchical file systems or cascading deletes.
    """
    if visited is None:
        visited = set()
    
    visited.add(start)
    for neighbor in graph.get(start, []):
        if neighbor not in visited:
            dfs_all_reachable(graph, neighbor, visited)
            
    return visited

    print("\n--- Testing Graph Algorithms ---")
    # Network graph mimicking user connections
    # Shashi -> Hemang -> Shubham, etc.
    user_network = {
        "Shashi": ["Hemang", "Aman"],
        "Hemang": ["Shashi", "Shubham", "Nitin"],
        "Aman": ["Shashi", "Nitin"],
        "Shubham": ["Hemang"],
        "Nitin": ["Hemang", "Aman"]
    }
    
    shortest_hop = bfs_shortest_path(user_network, "Shashi", "Shubham")
    print(f"BFS Shortest Connection Path from Shashi to Shubham: {shortest_hop}")
    
    all_connections = dfs_all_reachable(user_network, "Shashi")
    print(f"DFS All Reachable Users from Shashi's cluster: {all_connections}")

import time

# 8.2 Sliding Window Rate Limiter Class for Backend Integration
class SlidingWindowRateLimiter:
    """
    Tracks API request timestamps within a sliding window.
    Perfect for dropping incoming spam requests or handling rate limits.
    """
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.request_history = []  # Holds active request timestamps

    def is_allowed(self) -> bool:
        current_time = time.time()
        
        # Keep only the timestamps that fall within the valid time window
        self.request_history = [
            t for t in self.request_history 
            if current_time - t < self.window_seconds
        ]
        
        # Check if we have remaining capacity
        if len(self.request_history) < self.max_requests:
            self.request_history.append(current_time)
            return True
            
        return False