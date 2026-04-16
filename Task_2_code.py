# Code of 2(a)
def sift_down(heap, idx, n):
    while True:
        left = 2 * idx + 1
        right = 2 * idx + 2
        smallest = idx

        if left < n and heap[left] < heap[smallest]:
            smallest = left
        if right < n and heap[right] < heap[smallest]:
            smallest = right

        if smallest == idx:
            break

        heap[idx], heap[smallest] = heap[smallest], heap[idx]
        idx = smallest

# Code of 2(b)
def sift_up(heap, idx):
    while idx > 0 and heap[idx] < heap[(idx - 1) // 2]:
        heap[idx], heap[(idx - 1) // 2] = heap[(idx - 1) // 2] , heap[idx]
        idx = (idx - 1) // 2

# Code of 2(c)
def build_heap(arr):
    n = len(arr)
    for i in range(n//2 - 1, -1, -1):
        sift_down(arr, i, n)

# Code of 2(d)
def heappop(heap):
    min_val = heap[0]
    last = heap.pop()
    if heap:
        heap[0] = last
        sift_down(heap, 0, len(heap))
    return min_val

# Code of Heap Sort
def heapify(arr, n, i):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2

    if l < n and arr[i] < arr[l]:
        largest = l

    if r < n and arr[largest] < arr[r]:
        largest = r

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)

def heapSort(arr):
    n = len(arr)

    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    for i in range(n-1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)

# Test for 2a
heap_test_2a = [4, 1, 3, 9, 5]
print("Before:", heap_test_2a)
sift_down(heap_test_2a, idx=0, n=5)
print("After:", heap_test_2a)

# Test for 2b
heap_test_2b = [1, 3, 2, 5, 4, 0]
print("Before", heap_test_2b)
sift_up(heap_test_2b, idx=5)
print("After", heap_test_2b)

# Test for 2c
heap_test_2c = [3, 1, 4, 1, 5, 9, 2, 6]
print("Before:", heap_test_2c)
build_heap(heap_test_2c)
print("After:", heap_test_2c)

# Test for 2d
heap_test_2d = [1, 3, 2, 5, 4, 9, 6]
print("Before:", heap_test_2d)
heappop(heap_test_2d)
print("After:", heap_test_2d)

# Test for Heap Sort
heap_sort_test = [1, 7, 6, 9, 11, 8, 5, 2, 3, 14, 12, 13, 4, 10]
print("Before:", heap_sort_test)
heapSort(heap_sort_test)
print("After:", heap_sort_test)