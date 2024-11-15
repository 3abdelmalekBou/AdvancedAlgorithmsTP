from complexity import time_and_space_profiler
from tqdm import tqdm
import numpy as np
import pandas as pd

# Initialize the test cases
np.random.seed(42)
tests = []

# Define the array sizes and number of tests per size
lengths = np.array(range(1000, 100000, 20000))
tests_per_length = 5

for length in lengths:
    for _ in range(tests_per_length):
        val = np.random.randint(1, 4 * length, size=length)
        test = (length, val)
        tests.append(test)


# Sorting algorithm definitions with time and space profiling

@time_and_space_profiler
def selection_sort(arr):
    comparisons = 0
    n = len(arr)

    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            comparisons += 1
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]  # Swap operation

    return comparisons


@time_and_space_profiler
def bubble_sort(arr):
    comparisons = 0
    n = len(arr)

    for i in range(n):
        for j in range(0, n - i - 1):
            comparisons += 1
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]  # Swap operation

    return comparisons


@time_and_space_profiler
def insertion_sort_by_exchange(arr):
    comparisons = 0
    n = len(arr)

    for i in range(1, n):
        j = i
        while j > 0 and arr[j] < arr[j - 1]:
            comparisons += 1
            arr[j], arr[j - 1] = arr[j - 1], arr[j]  # Swap operation
            j -= 1
        comparisons += 1  # For the final failed comparison in while loop

    return comparisons


@time_and_space_profiler
def insertion_sort_by_shifting(arr):
    comparisons = 0
    n = len(arr)

    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            comparisons += 1
            arr[j + 1] = arr[j]  # Shift operation
            j -= 1
        arr[j + 1] = key
        comparisons += 1  # For the final failed comparison in while loop

    return comparisons


# Define the sorting algorithms to be tested
sorting_algorithms = [
    ("Selection Sort", selection_sort),
    ("Bubble Sort", bubble_sort),
    ("Insertion Sort (Exchange)", insertion_sort_by_exchange),
    ("Insertion Sort (Shift)", insertion_sort_by_shifting)
]

# Run tests and store results
results = []
for i, (length, original_array) in tqdm(enumerate(tests), total=len(tests), desc="Testing Sort Algorithms"):
    for algo_name, algo_func in sorting_algorithms:
        # Make a copy of the array to avoid in-place sorting issues
        array_copy = np.copy(original_array)

        # Execute sorting with profiler
        func_name, comparisons, elapsed_time, space_used = algo_func(array_copy)

        # Store results
        results.append({
            "Test ID": i,
            "Algorithm": func_name,
            "Array Length": length,
            "Comparisons": comparisons,
            "Time (s)": elapsed_time,
            "Space (MiB)": space_used
        })

# Convert results to DataFrame and save to CSV
df = pd.DataFrame(results)
print(df)
df.to_csv("sorting_results_with_profiler.csv", index=False)
