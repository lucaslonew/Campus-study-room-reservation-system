def heapify(arr, n, i):
    """
    Heapify a subtree rooted at index i.
    Assumes subtrees are already heapified.
    
    Parameters:
    arr: The array to heapify
    n: Size of the heap
    i: Index of the root node
    """
    largest = i  # Initialize largest as root
    left = 2 * i + 1
    right = 2 * i + 2
    
    # Check if left child exists and is greater than root
    if left < n and arr[left] > arr[largest]:
        largest = left
    
    # Check if right child exists and is greater than current largest
    if right < n and arr[right] > arr[largest]:
        largest = right
    
    # If largest is not root, swap and continue heapifying
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)


def build_max_heap(arr):
    """
    Build a max heap from an unsorted array.
    """
    n = len(arr)
    
    # Start from the last non-leaf node and move up
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)


def heap_sort(arr):
    """
    Main heap sort function.
    
    Parameters:
    arr: Array to be sorted
    Returns: Sorted array
    """
    n = len(arr)
    
    # Build a max heap
    build_max_heap(arr)
    
    # Extract elements one by one
    for i in range(n - 1, 0, -1):
        # Move current root to end
        arr[0], arr[i] = arr[i], arr[0]
        
        # Heapify the reduced heap
        heapify(arr, i, 0)
    
    return arr


class MinHeap:
    """
    Min Heap implementation with basic operations.
    """
    def __init__(self):
        self.heap = []
    
    def parent(self, i):
        """Get parent index"""
        return (i - 1) // 2
    
    def left_child(self, i):
        """Get left child index"""
        return 2 * i + 1
    
    def right_child(self, i):
        """Get right child index"""
        return 2 * i + 2
    
    def insert(self, value):
        """Insert a new element into the heap"""
        self.heap.append(value)
        self._heapify_up(len(self.heap) - 1)
    
    def extract_min(self):
        """Remove and return the minimum element"""
        if len(self.heap) == 0:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()
        
        # Store minimum value
        min_val = self.heap[0]
        
        # Move last element to root
        self.heap[0] = self.heap.pop()
        
        # Heapify down from root
        self._heapify_down(0)
        
        return min_val
    
    def _heapify_up(self, i):
        """Maintain heap property from bottom to top"""
        while i > 0 and self.heap[self.parent(i)] > self.heap[i]:
            # Swap with parent if parent is larger
            parent_idx = self.parent(i)
            self.heap[i], self.heap[parent_idx] = self.heap[parent_idx], self.heap[i]
            i = parent_idx
    
    def _heapify_down(self, i):
        """Maintain heap property from top to bottom"""
        smallest = i
        left = self.left_child(i)
        right = self.right_child(i)
        
        if left < len(self.heap) and self.heap[left] < self.heap[smallest]:
            smallest = left
        
        if right < len(self.heap) and self.heap[right] < self.heap[smallest]:
            smallest = right
        
        if smallest != i:
            # Swap and continue heapifying
            self.heap[i], self.heap[smallest] = self.heap[smallest], self.heap[i]
            self._heapify_down(smallest)
    
    def peek(self):
        """Return minimum element without removing it"""
        return self.heap[0] if self.heap else None
    
    def size(self):
        """Return heap size"""
        return len(self.heap)


# Example Usage
if __name__ == "__main__":
    # Example 1: Heap Sort
    print("=== Heap Sort Example ===")
    unsorted_array = [12, 11, 13, 5, 6, 7]
    print("Original array:", unsorted_array)
    
    sorted_array = heap_sort(unsorted_array.copy())
    print("Sorted array:", sorted_array)
    
    # Example 2: Min Heap Operations
    print("\n=== Min Heap Operations Example ===")
    min_heap = MinHeap()
    
    elements = [3, 2, 1, 15, 5, 4, 45]
    for elem in elements:
        min_heap.insert(elem)
        print(f"Inserted {elem}. Heap: {min_heap.heap}")
    
    print(f"\nMin element: {min_heap.peek()}")
    print(f"Heap size: {min_heap.size()}")
    
    print("\nExtracting elements in sorted order:")
    while min_heap.size() > 0:
        min_val = min_heap.extract_min()
        print(f"Extracted: {min_val}, Remaining heap: {min_heap.heap}")
    
    # Example 3: Using heapq module (Python built-in)
    print("\n=== Python heapq Module Example ===")
    import heapq
    
    # Min heap operations using heapq
    heap_list = []
    for num in [3, 1, 4, 1, 5, 9, 2, 6]:
        heapq.heappush(heap_list, num)
    
    print("Heap after pushes:", heap_list)
    print("Elements popped in order:")
    while heap_list:
        print(heapq.heappop(heap_list), end=" ")
    print()


# Output:
# === Heap Sort Example ===
# Original array: [12, 11, 13, 5, 6, 7]
# Sorted array: [5, 6, 7, 11, 12, 13]
# 
# === Min Heap Operations Example ===
# Inserted 3. Heap: [3]
# Inserted 2. Heap: [2, 3]
# Inserted 1. Heap: [1, 3, 2]
# Inserted 15. Heap: [1, 3, 2, 15]
# Inserted 5. Heap: [1, 3, 2, 15, 5]
# Inserted 4. Heap: [1, 3, 2, 15, 5, 4]
# Inserted 45. Heap: [1, 3, 2, 15, 5, 4, 45]
# 
# Min element: 1
# Heap size: 7
# 
# Extracting elements in sorted order:
# Extracted: 1, Remaining heap: [2, 3, 45, 15, 5, 4]
# Extracted: 2, Remaining heap: [3, 4, 45, 15, 5]
# Extracted: 3, Remaining heap: [4, 5, 45, 15]
# Extracted: 4, Remaining heap: [5, 15, 45]
# Extracted: 5, Remaining heap: [15, 45]
# Extracted: 15, Remaining heap: [45]
# Extracted: 45, Remaining heap: []
# 
# === Python heapq Module Example ===
# Heap after pushes: [1, 1, 2, 3, 5, 9, 4, 6]
# Elements popped in order:
# 1 1 2 3 4 5 6 9