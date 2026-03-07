**Python Heap Data Structure and Heap Sort Algorithm**

**Heap Data Structure**

A **heap**​ is a specialized tree-based data structure that satisfies the heap property:

*   **Max Heap**: Each parent node is greater than or equal to its children (A\[parent(i)\] ≥ A\[i\])
*   **Min Heap**: Each parent node is less than or equal to its children (A\[parent(i)\] ≤ A\[i\])

**Key Characteristics**

*   **Complete Binary Tree**: All levels except possibly the last are completely filled, and nodes are as left as possible
*   **Array Representation**: Typically implemented as an array where:
    *   Parent index: parent(i) = (i-1)//2
    *   Left child: left(i) = 2\*i + 1
    *   Right child: right(i) = 2\*i + 2

**Operations Complexity**

*   Build Heap: O(n)
*   Insert: O(log n)
*   Extract Max/Min: O(log n)
*   Heapify: O(log n)

**Heap Sort Algorithm**

Heap Sort is a comparison-based sorting algorithm that uses a binary heap data structure. It has O(n log n) time complexity and is an in-place algorithm (O(1) space).

**Algorithm Steps**

1.  **Build Max Heap**: Build a max heap from the input array
2.  **Sort**:
    *   Swap the root (maximum element) with the last element
    *   Reduce heap size by 1
    *   Heapify the root
    *   Repeat until the heap is empty