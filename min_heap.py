# Name: Fariss Khairy
# OSU Email: khairyf@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 5
# Due Date: 05/28/24
# Description:


from dynamic_array import *


class MinHeapException(Exception):
    """
    Custom exception to be used by MinHeap class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class MinHeap:
    def __init__(self, start_heap=None):
        """
        Initialize a new MinHeap
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._heap = DynamicArray()

        # populate MinHeap with initial values (if provided)
        # before using this feature, implement add() method
        if start_heap:
            for node in start_heap:
                self.add(node)

    def __str__(self) -> str:
        """
        Return MinHeap content in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        heap_data = [self._heap[i] for i in range(self._heap.length())]
        return "HEAP " + str(heap_data)

    def add(self, node: object) -> None:
        """
        TODO: Write this implementation
        """
        self._heap.append(node)

        current_index = self._heap.length() - 1

        while current_index > 0 and self._heap[(current_index - 1) // 2] > self._heap[current_index]:
            temp = self._heap[current_index]
            self._heap[current_index] = self._heap[(current_index - 1) // 2]
            self._heap[(current_index - 1) // 2] = temp
            current_index = (current_index - 1) // 2


    def is_empty(self) -> bool:
        """
        TODO: Write this implementation
        """
        return self._heap.is_empty()

    def get_min(self) -> object:
        """
        TODO: Write this implementation
        """
        if self._heap.is_empty():
            raise MinHeapException
        else:
            return self._heap[0]

    def remove_min(self) -> object:
        """
        TODO: Write this implementation
        """
        if self._heap.is_empty():
            raise MinHeapException

        temp_value = self._heap[0]
        self._heap[0] = self._heap[self._heap.length() - 1]
        self._heap.remove_at_index(self._heap.length() - 1)
        _percolate_down(self._heap, 0, self._heap.length())

        return temp_value

    def build_heap(self, da: DynamicArray) -> None:
        """
        TODO: Write this implementation
        """
        self._heap = DynamicArray()
        for i in range(da.length()):
            self._heap.append(da[i])

        for i in range((self._heap.length()) // 2 - 1, -1, -1):
            _percolate_down(self._heap, i, self._heap.length())

    def size(self) -> int:
        """
        TODO: Write this implementation
        """
        return self._heap.length()

    def clear(self) -> None:
        """
        TODO: Write this implementation
        """
        self._heap = DynamicArray()


def heapsort(da: DynamicArray) -> None:
    """
    TODO: Write this implementation
    """
    for i in range((da.length()) // 2 - 1, -1, -1):
        _percolate_down(da, i, da.length())

    for i in range(da.length() - 1, -1, -1):
        temp = da[i]
        da[i] = da[0]
        da[0] = temp

        _percolate_down(da, 0, i)

# It's highly recommended that you implement the following optional          #
# helper function for percolating elements down the MinHeap. You can call    #
# this from inside the MinHeap class. You may edit the function definition.  #


def _percolate_down(da: DynamicArray, parent: int, stop) -> None:
    """
    TODO: Write your implementation
    """
    child_1_index = 2 * parent + 1
    child_2_index = 2 * parent + 2

    while (child_1_index < stop and da[parent] > da[child_1_index]) or (child_2_index < stop and da[parent] > da[child_2_index]):
        if child_2_index < stop:
            if da[child_1_index] <= da[child_2_index] and da[parent] > da[child_1_index]:
                temp = da[parent]
                da[parent] = da[child_1_index]
                da[child_1_index] = temp
                parent = child_1_index
            else:
                temp = da[parent]
                da[parent] = da[child_2_index]
                da[child_2_index] = temp
                parent = child_2_index
        else:
            temp = da[parent]
            da[parent] = da[child_1_index]
            da[child_1_index] = temp
            parent = child_1_index
        child_1_index = 2 * parent + 1
        child_2_index = 2 * parent + 2


# ------------------- BASIC TESTING -----------------------------------------


if __name__ == '__main__':

    print("\nPDF - add example 1")
    print("-------------------")
    h = MinHeap()
    print(h, h.is_empty())
    for value in range(300, 200, -15):
        h.add(value)
        print(h)

    print("\nPDF - add example 2")
    print("-------------------")
    h = MinHeap(['fish', 'bird'])
    print(h)
    for value in ['monkey', 'zebra', 'elephant', 'horse', 'bear']:
        h.add(value)
        print(h)

    print("\nPDF - is_empty example 1")
    print("-------------------")
    h = MinHeap([2, 4, 12, 56, 8, 34, 67])
    print(h.is_empty())

    print("\nPDF - is_empty example 2")
    print("-------------------")
    h = MinHeap()
    print(h.is_empty())

    print("\nPDF - get_min example 1")
    print("-----------------------")
    h = MinHeap(['fish', 'bird'])
    print(h)
    print(h.get_min(), h.get_min())

    print("\nPDF - remove_min example 1")
    print("--------------------------")
    h = MinHeap([1, 10, 2, 9, 3, 8, 4, 7, 5, 6])
    while not h.is_empty() and h.is_empty() is not None:
        print(h, end=' ')
        print(h.remove_min())

    print("\nPDF - build_heap example 1")
    print("--------------------------")
    da = DynamicArray([100, 20, 6, 200, 90, 150, 300])
    h = MinHeap(['zebra', 'apple'])
    print(h)
    h.build_heap(da)
    print(h)

    print("--------------------------")
    print("Inserting 500 into input DA:")
    da[0] = 500
    print(da)

    print("Your MinHeap:")
    print(h)
    if h.get_min() == 500:
        print("Error: input array and heap's underlying DA reference same object in memory")

    print("\nPDF - size example 1")
    print("--------------------")
    h = MinHeap([100, 20, 6, 200, 90, 150, 300])
    print(h.size())

    print("\nPDF - size example 2")
    print("--------------------")
    h = MinHeap([])
    print(h.size())

    print("\nPDF - clear example 1")
    print("---------------------")
    h = MinHeap(['monkey', 'zebra', 'elephant', 'horse', 'bear'])
    print(h)
    print(h.clear())
    print(h)

    print("\nPDF - heapsort example 1")
    print("------------------------")
    da = DynamicArray([100, 20, 6, 200, 90, 150, 300])
    print(f"Before: {da}")
    heapsort(da)
    print(f"After:  {da}")

    print("\nPDF - heapsort example 2")
    print("------------------------")
    da = DynamicArray(['monkey', 'zebra', 'elephant', 'horse', 'bear'])
    print(f"Before: {da}")
    heapsort(da)
    print(f"After:  {da}")
