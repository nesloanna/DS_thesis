import pandas as pd
from difflib import SequenceMatcher
import os
from itertools import chain
from collections import defaultdict
import pprint
pp = pprint.PrettyPrinter(indent=4)


os.chdir("/Users/annaolsen/Desktop/Speciale/DS_thesis/data")
print(os.getcwd())


df = pd.read_csv("Tara_merged_NEW_sorted.csv")

# df = df.T
# df = df[:500]


# for col, rows in df.iterrows():
#     print(rows[col])
#     break


# Dictionary to store column pairs with identical values along with their counts
identical_values = defaultdict(lambda: defaultdict(int))

# Iterate through rows
for index, row in df.iterrows():
    # Iterate through columns in the row
    for col1, value1 in row.items():
        # Check if the value is duplicated in other columns
        for col2, value2 in row.items():
            if col1 != col2 and value1 == value2:
                # Increment the count for this pair of columns and value
                identical_values[col1, col2][value1] += 1

# Filter out pairs with counts less than 2 (meaning no duplicates)
identical_values = {pair: count for pair,
                    count in identical_values.items() if sum(count.values()) > 1}

# Sort the identical_values dictionary based on the total count of matches for each column pair
sorted_identical_values = sorted(
    identical_values.items(), key=lambda x: sum(x[1].values()), reverse=True)

# Print the sorted dictionary containing column pairs with identical values and their total counts
for (col1, col2), counts in sorted_identical_values:
    total_count = sum(counts.values())
    print(
        f"Columns '{col1}' and '{col2}' have identical values {total_count} times")


# # Filter out pairs with counts less than 2 (meaning no duplicates)
# identical_values = {pair: counts for pair,
#                     counts in identical_values.items() if sum(counts.values()) > 1}


# # Sort the identical_values dictionary based on the total count of matches for each column pair
# sorted_identical_values = sorted(
#     identical_values.items(), key=lambda x: sum(x[1].values()), reverse=True)


# # Print the sorted dictionary containing column pairs with identical values and their counts
# for pair, counts in sorted_identical_values:
#     col1, col2 = pair
#     print(f"Columns '{col1}' and '{col2}' have identical values:")
#     for value, count in counts.items():
#         print(f"    Value '{value}' occurs {count} times")


# # Iterate through rows
# for index, row in df.iterrows():
#     print(f"Processing row {index}:")
#     # Iterate through values in the row
#     for col, value in row.items():
#         print(f"    Column '{col}': {value}")

# for col in df.columns:
#     print(df[col].duplicated())


# Dictionary to store whether each column contains duplicate values
# columns_with_duplicates = {}

# # Iterate over each column
# for col in df.columns:
#     # Store whether each value in the column is duplicated
#     columns_with_duplicates[col] = df[col].duplicated()

# Print the dictionary containing column names and their corresponding boolean Series indicating duplicate values
# for col, duplicates in columns_with_duplicates.items():
#     print(f'{col}:')
#     print(duplicates)
#     print()

# new = pd.DataFrame(columns_with_duplicates)
# new.to_csv("duplicates.csv")

# List to store column names with duplicate values
# columns_with_duplicates = []

dict_duplicates = {}

# # Iterate over each column
# for col, rows in df.iterrows():
#     print(col)
#     # print(rows.duplicated())
#     for row in rows:
#         print(col)
#         print(row)
#         break

# Check if any value in the column is duplicated
#     if df[col].duplicated().any():
#         # If duplicated, add the column name to the list
#         columns_with_duplicates.append(col)

# # Print the list of column names with duplicate values
# print(columns_with_duplicates)

# ------ Store and print column names in dict ------

# Initialize an empty dictionary to store column names as keys and duplicate values/rows as values
# duplicates_c_dict = defaultdict(list)

# #  Iterate over each column
# for col in df.columns:
#     # Initialize an empty dictionary to store values and corresponding row indices
#     seen = {}
#     for i, value in enumerate(df[col]):
#         if value in seen:
#             # If the value is already seen in this column, append the current column and the duplicate value to the list
#             duplicates_c_dict[value].append((seen[value], col))
#         else:
#             # If the value is seen for the first time in this column, store its row index
#             seen[value] = col

# # Filter out values without duplicates
# duplicates_c_dict = {
#     value: locations for value, locations in duplicates_c_dict.items() if len(locations) > 1}

# duplicates_c_dict = {value: set(locations)
#                      for value, locations in duplicates_c_dict.items()}
# # Print the dictionary containing values and their corresponding duplicate columns
# pp.pprint(duplicates_c_dict)

# Print length of dict
# length_dict = {key: len(value) for key, value in duplicates_c_dict.items()}
# pp.pprint(length_dict)


# ------ Store and print duplicate values in dict ------

# Initialize an empty dictionary to store column names as keys and duplicate values/rows as values
# duplicates_v_dict = defaultdict(list)

# # Iterate over each column
# for col in df.columns:
#     # Initialize an empty dictionary to store values and corresponding row indices
#     seen = {}
#     for i, value in enumerate(df[col]):
#         if value in seen:
#             # If the value is already seen in this column, append the current value and the duplicate value to the list
#             duplicates_v_dict[col].append((df.iloc[seen[value]][col], col))

#         else:
#             # If the value is seen for the first time in this column, store its row index
#             seen[value] = i

# # Filter out columns without duplicates
# duplicates_v_dict = {col: values for col,
#                      values in duplicates_v_dict.items() if len(values) > 0}

# # Print the dictionary containing column names and their corresponding duplicate values/rows
# pp.pprint(duplicates_v_dict)
