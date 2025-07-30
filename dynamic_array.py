# Course: CS261 - Data Structures
# Assignment: 2
# Description: This file implements the DynamicArray data structure where the data structure's size is adjustable and
# dynamic. It includes additional functions chunk and find_mode to complement DynamicArray. chunk sorts input
# DynamicArray into individual DynamicArrays with values of non-descending order. find_mode returns the mode or modes
# of input DynamicArray along with its frequency.


from static_array import StaticArray


class DynamicArrayException(Exception):
    """
    Custom exception class to be used by Dynamic Array
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class DynamicArray:
    def __init__(self, start_array=None):
        """
        Initialize new dynamic array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._size = 0
        self._capacity = 4
        self._data = StaticArray(self._capacity)

        # populate dynamic array with initial values (if provided)
        # before using this feature, implement append() method
        if start_array is not None:
            for value in start_array:
                self.append(value)

    def __str__(self) -> str:
        """
        Return content of dynamic array in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = "DYN_ARR Size/Cap: "
        out += str(self._size) + "/" + str(self._capacity) + ' ['
        out += ', '.join([str(self._data[_]) for _ in range(self._size)])
        return out + ']'

    def __iter__(self):
        """
        Create iterator for loop
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._index = 0
        return self

    def __next__(self):
        """
        Obtain next value and advance iterator
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        try:
            value = self[self._index]
        except DynamicArrayException:
            raise StopIteration

        self._index += 1
        return value

    def get_at_index(self, index: int) -> object:
        """
        Return value from given index position
        Invalid index raises DynamicArrayException
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if index < 0 or index >= self._size:
            raise DynamicArrayException
        return self._data[index]

    def set_at_index(self, index: int, value: object) -> None:
        """
        Store value at given index in the array
        Invalid index raises DynamicArrayException
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if index < 0 or index >= self._size:
            raise DynamicArrayException
        self._data[index] = value

    def __getitem__(self, index) -> object:
        """
        Same functionality as get_at_index() method above,
        but called using array[index] syntax
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self.get_at_index(index)

    def __setitem__(self, index, value) -> None:
        """
        Same functionality as set_at_index() method above,
        but called using array[index] syntax
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.set_at_index(index, value)

    def is_empty(self) -> bool:
        """
        Return True is array is empty / False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size == 0

    def length(self) -> int:
        """
        Return number of elements stored in array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return the capacity of the array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    def print_da_variables(self) -> None:
        """
        Print information contained in the dynamic array.
        Used for testing purposes.
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        print(f"Length: {self._size}, Capacity: {self._capacity}, {self._data}")

    # -----------------------------------------------------------------------

    def resize(self, new_capacity: int) -> None:
        """
        Resizes the capacity of the data structure of the DynamicArray object.

        Input: int

        Output: None
        """

        if new_capacity > 0 and new_capacity >= self._size:
            new_arr = StaticArray(new_capacity)
            if self._size > 0:
                for i in range(self._size):
                    new_arr[i] = self._data[i]
            self._capacity = new_capacity
            self._data = new_arr

    def append(self, value: object) -> None:
        """
        This function adds a value object to the end of the DynamicArray object.

        Input: object

        Output: None
        """

        if self._size == self._capacity:
            self.resize(self._capacity * 2)
        self._data[self._size] = value
        self._size += 1

    def insert_at_index(self, index: int, value: object) -> None:
        """
        This function adds a value object at the input index of the DynamicArray object.
        Raises a DynamicArrayException if index < 0 or index > size of DynamicArray object.

        Input: index int, object

        Output: None
        """

        if index < 0 or index > self._size:
            raise DynamicArrayException

        if self._size == self._capacity:
            self.resize(self._capacity * 2)

        # Edge case where value to be added is at the end of the array.
        if index == self._size:
            self._data[index] = value
            self._size += 1
        else:
            curr = self._data[index]
            self._data[index] = value
            self._size += 1
            for i in range(index + 1, self._size):
                temp = self._data[i]
                self._data[i] = curr
                curr = temp

    def remove_at_index(self, index: int) -> None:
        """
        This function removes a value object at input index.
        Raises a DynamicArrayException if index < 0 or index >= size of DynamicArray object.

        Input: index int

        Output: None
        """

        if index < 0 or index >= self._size:
            raise DynamicArrayException

        # Resizes DynamicArray capacity if size of DynamicArray is strictly less than 1/4 of its capacity.
        if self._size * 4 < self._capacity:
            # Condition to prevent resizing if capacity of DynamicArray is 10 or less.
            if self._capacity > 10:
                # Resizes the capacity of DynamicArray to twice its size.
                if self._size * 2 > 10:
                    self.resize(self._size * 2)
                # Resizes DynamicArray capacity to limit at 10 if size * 2 is less than 10.
                else:
                    self.resize(10)

        # Edge case where value to be removed is at the end of DynamicArray.
        if index == self._size - 1:
            self._size -= 1
        else:
            for i in range(index, self._size - 1):
                self._data[i] = self._data[i + 1]
            self._size -= 1

    def slice(self, start_index: int, size: int) -> "DynamicArray":
        """
        This function returns a new DynamicArray object of input size with values starting at input start_index.
        Raises a DynamicArrayException if start_index < 0, or start_index >= size of DynamicArray, or input size < 0,
        or there are not enough values between start_index and end of DynamicArray to return a new DynamicArray
        object of given input size.

        Input: start_index int, size int

        Output: DynamicArray object
        """

        if start_index < 0 or start_index >= self._size or size < 0 or self._size - start_index < size:
            raise DynamicArrayException

        # Edge case where sliced DynamicArray size is 0
        if size == 0:
            return DynamicArray()

        new_dyn_arr = DynamicArray()
        for i in range(start_index, start_index + size):
            new_dyn_arr.append(self._data[i])

        return new_dyn_arr

    def map(self, map_func) -> "DynamicArray":
        """
        This function returns a new DynamicArray object whose values are subjected to the input function
        map_function of the corresponding value in the input DynamicArray.

        Input: map_func function

        Output: DynamicArray object
        """

        new_dyn_arr = DynamicArray()
        for i in range(self._size):
            new_dyn_arr.append(map_func(self._data[i]))

        return new_dyn_arr

    def filter(self, filter_func) -> "DynamicArray":
        """
        This function returns a new DynamicArray object with included values that return True when subjected to
        input function filter_func of the corresponding value in the input DynamicArray.

        Input: filter_func function

        Output: DynamicArray object
        """

        new_dyn_arr = DynamicArray()
        for i in range(self._size):
            if filter_func(self._data[i]):
                new_dyn_arr.append(self._data[i])

        return new_dyn_arr

    def reduce(self, reduce_func, initializer=None) -> object:
        """
        This function returns an object derived from the input function reduce_func where all values from input
        DynamicArray is subjected to the input function reduce_func. input initializer is added to the beginning of
        function calculation if not None, returns initializer if input DynamicArray is empty.

        Input: Input function reduce_func, initializer object

        Output: object
        """

        if self._size == 0:
            return initializer
        # Edge case where size of DynamicArray is 1
        elif self._size == 1:
            if initializer is None:
                return self._data[0]
            else:
                return reduce_func(initializer, self._data[0])
        # Applies function reduce_func to all values in DynamicArray and the total calculation is tracked.
        else:
            if initializer is not None:
                total = reduce_func(initializer, self._data[0])
                for i in range(1, self._size):
                    total = reduce_func(total, self._data[i])
            else:
                total = reduce_func(self._data[0], self._data[1])
                for i in range(2, self._size):
                    total = reduce_func(total, self._data[i])
            return total


def chunk(arr: DynamicArray) -> "DynamicArray":
    """
    This function inputs a DynamicArray object and returns a new DynamicArray object whose values are individual
    DynamicArray objects whose values are non-descending values from the input DynamicArray.

    Input: DynamicArray object

    Output: DynamicArray object
    """

    # Edge case where input DynamicArray has no values.
    if arr.length() == 0:
        return arr

    new_arr = DynamicArray()

    # divisions is the number of divided individual DynamicArrays to be created. Calculated by number of times
    # value is in descending order. 1 added to divisions to account for last divided individual DynamicArray.
    divisions = 0
    for i in range(arr.length() - 1):
        if arr[i] > arr[i + 1]:
            divisions += 1
    divisions += 1

    # Adds number of divided individual DynamicArrays to new DynamicArray object.
    for i in range(divisions):
        new_arr.append(DynamicArray())

    # count keeps track of divided individual DynamicArray to be added to.
    count = 0
    for i in range(arr.length() - 1):
        new_arr[count].append(arr[i])
        if arr[i] > arr[i + 1]:
            count += 1
    # Edge case to add last input value to last divided individual DynamicArray
    new_arr[count].append(arr[arr.length() - 1])

    return new_arr


def find_mode(arr: DynamicArray) -> tuple[DynamicArray, int]:
    """
    This function returns a tuple with a DynamicArray that includes the most recurring value or values in a sorted
    input DynamicArray object along with its frequency.

    Input: DynamicArray object

    Output: tuple with DynamicArray object with modes of input DynamicArray and its frequency
    """

    # Edge case where there is only 1 value in input DynamicArray
    if arr.length() == 1:
        return (arr, 1)

    # New DynamicArray object to include mode or modes of input DynamicArray
    return_arr = DynamicArray()

    # Handles edge case of first 2 values in input DynamicArray
    return_arr.append(arr[0])
    current_frequency = 1
    max_frequency = 1
    if arr[0] == arr[1]:
        current_frequency += 1
        max_frequency += 1
    # If first 2 values are unique, both values are appended to new DynamicArray and current_frequency is reset.
    else:
        return_arr.append(arr[1])
        current_frequency = 1

    # Compares adjacent values in input DynamicArray and tracks frequency of current value and max frequency.
    # If adjacent values are equal, current_frequency is incremented, else, current_frequency is reset to 1.
    for i in range(2, arr.length()):
        if arr[i - 1] == arr[i]:
            current_frequency += 1
            # Case where there is more than 1 mode.
            if current_frequency == max_frequency:
                return_arr.append(arr[i])
            elif current_frequency > max_frequency:
                # Erases past included values in new DynamicArray by replacing with a new DynamicArray
                return_arr = DynamicArray()
                return_arr.append(arr[i])
                max_frequency = current_frequency
        else:
            current_frequency = 1
            # Case where there is more than 1 mode.
            if max_frequency == 1:
                return_arr.append(arr[i])

    return (return_arr, max_frequency)


# ------------------- BASIC TESTING -----------------------------------------


if __name__ == "__main__":

    print("\n# resize - example 1")
    da = DynamicArray()

    # print dynamic array's size, capacity and the contents
    # of the underlying static array (data)
    da.print_da_variables()
    da.resize(8)
    da.print_da_variables()
    da.resize(2)
    da.print_da_variables()
    da.resize(0)
    da.print_da_variables()

    print("\n# resize - example 2")
    da = DynamicArray([1, 2, 3, 4, 5, 6, 7, 8])
    print(da)
    da.resize(20)
    print(da)
    da.resize(4)
    print(da)

    print("\n# append - example 1")
    da = DynamicArray()
    da.print_da_variables()
    da.append(1)
    da.print_da_variables()
    print(da)

    print("\n# append - example 2")
    da = DynamicArray()
    for i in range(9):
        da.append(i + 101)
        print(da)

    print("\n# append - example 3")
    da = DynamicArray()
    for i in range(600):
        da.append(i)
    print(da.length())
    print(da.get_capacity())

    print("\n# insert_at_index - example 1")
    da = DynamicArray([100])
    print(da)
    da.insert_at_index(0, 200)
    da.insert_at_index(0, 300)
    da.insert_at_index(0, 400)
    print(da)
    da.insert_at_index(3, 500)
    print(da)
    da.insert_at_index(1, 600)
    print(da)

    print("\n# insert_at_index example 2")
    da = DynamicArray()
    try:
        da.insert_at_index(-1, 100)
    except Exception as e:
        print("Exception raised:", type(e))
    da.insert_at_index(0, 200)
    try:
        da.insert_at_index(2, 300)
    except Exception as e:
        print("Exception raised:", type(e))
    print(da)

    print("\n# insert at index example 3")
    da = DynamicArray()
    for i in range(1, 10):
        index, value = i - 4, i * 10
        try:
            da.insert_at_index(index, value)
        except Exception as e:
            print("Cannot insert value", value, "at index", index)
    print(da)

    print("\n# remove_at_index - example 1")
    da = DynamicArray([10, 20, 30, 40, 50, 60, 70, 80])
    print(da)
    da.remove_at_index(0)
    print(da)
    da.remove_at_index(6)
    print(da)
    da.remove_at_index(2)
    print(da)

    print("\n# remove_at_index - example 2")
    da = DynamicArray([1024])
    print(da)
    for i in range(17):
        da.insert_at_index(i, i)
    print(da.length(), da.get_capacity())
    for i in range(16, -1, -1):
        da.remove_at_index(0)
    print(da)

    print("\n# remove_at_index - example 3")
    da = DynamicArray()
    print(da.length(), da.get_capacity())
    [da.append(1) for i in range(100)]  # step 1 - add 100 elements
    print(da.length(), da.get_capacity())
    [da.remove_at_index(0) for i in range(68)]  # step 2 - remove 68 elements
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 3 - remove 1 element
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 4 - remove 1 element
    print(da.length(), da.get_capacity())
    [da.remove_at_index(0) for i in range(14)]  # step 5 - remove 14 elements
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 6 - remove 1 element
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 7 - remove 1 element
    print(da.length(), da.get_capacity())

    for i in range(14):
        print("Before remove_at_index(): ", da.length(), da.get_capacity(), end="")
        da.remove_at_index(0)
        print(" After remove_at_index(): ", da.length(), da.get_capacity())

    print("\n# remove at index - example 4")
    da = DynamicArray([1, 2, 3, 4, 5])
    print(da)
    for _ in range(5):
        da.remove_at_index(0)
        print(da)

    print("\n# slice example 1")
    da = DynamicArray([1, 2, 3, 4, 5, 6, 7, 8, 9])
    da_slice = da.slice(1, 3)
    print(da, da_slice, sep="\n")
    da_slice.remove_at_index(0)
    print(da, da_slice, sep="\n")

    print("\n# slice example 2")
    da = DynamicArray([10, 11, 12, 13, 14, 15, 16])
    print("SOURCE:", da)
    slices = [(0, 7), (-1, 7), (0, 8), (2, 3), (5, 0), (5, 3), (6, 1), (6, -1)]
    for i, cnt in slices:
        print("Slice", i, "/", cnt, end="")
        try:
            print(" --- OK: ", da.slice(i, cnt))
        except:
            print(" --- exception occurred.")

    print("\n# map example 1")
    da = DynamicArray([1, 5, 10, 15, 20, 25])
    print(da)
    print(da.map(lambda x: x ** 2))

    print("\n# map example 2")


    def double(value):
        return value * 2


    def square(value):
        return value ** 2


    def cube(value):
        return value ** 3


    def plus_one(value):
        return value + 1


    da = DynamicArray([plus_one, double, square, cube])
    for value in [1, 10, 20]:
        print(da.map(lambda x: x(value)))

    print("\n# filter example 1")


    def filter_a(e):
        return e > 10


    da = DynamicArray([1, 5, 10, 15, 20, 25])
    print(da)
    result = da.filter(filter_a)
    print(result)
    print(da.filter(lambda x: (10 <= x <= 20)))

    print("\n# filter example 2")


    def is_long_word(word, length):
        return len(word) > length


    da = DynamicArray("This is a sentence with some long words".split())
    print(da)
    for length in [3, 4, 7]:
        print(da.filter(lambda word: is_long_word(word, length)))

    print("\n# reduce example 1")
    values = [100, 5, 10, 15, 20, 25]
    da = DynamicArray(values)
    print(da)
    print(da.reduce(lambda x, y: (x // 5 + y ** 2)))
    print(da.reduce(lambda x, y: (x + y ** 2), -1))

    print("\n# reduce example 2")
    da = DynamicArray([100])
    print(da.reduce(lambda x, y: x + y ** 2))
    print(da.reduce(lambda x, y: x + y ** 2, -1))
    da.remove_at_index(0)
    print(da.reduce(lambda x, y: x + y ** 2))
    print(da.reduce(lambda x, y: x + y ** 2, -1))

    def print_chunked_da(arr: DynamicArray):
        if len(str(arr)) <= 100:
            print(arr)
        else:
            print(f"DYN_ARR Size/Cap: {arr.length()}/{arr.get_capacity()}")
            print('[\n' + ',\n'.join(f'\t{chunk}' for chunk in arr) + '\n]')

    print("\n# chunk example 1")
    test_cases = [
        [10, 20, 30, 30, 5, 10, 1, 2, 3, 4],
        ['App', 'Async', 'Cloud', 'Data', 'Deploy',
         'C', 'Java', 'Python', 'Git', 'GitHub',
         'Class', 'Method', 'Heap']
    ]

    for case in test_cases:
        da = DynamicArray(case)
        chunked_da = chunk(da)
        print(da)
        print_chunked_da(chunked_da)

    print("\n# chunk example 2")
    test_cases = [[], [261], [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]]

    for case in test_cases:
        da = DynamicArray(case)
        chunked_da = chunk(da)
        print(da)
        print_chunked_da(chunked_da)

    print("\n# find_mode - example 1")
    test_cases = (
        [1, 1, 2, 3, 3, 4],
        [1, 2, 3, 4, 5],
        ["Apple", "Banana", "Banana", "Carrot", "Carrot",
         "Date", "Date", "Date", "Eggplant", "Eggplant", "Eggplant",
         "Fig", "Fig", "Grape"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"{da}\nMode: {mode}, Frequency: {frequency}\n")

    case = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    da = DynamicArray()
    for x in range(len(case)):
        da.append(case[x])
        mode, frequency = find_mode(da)
        print(f"{da}\nMode: {mode}, Frequency: {frequency}")
