import pandas as pd
import os
import pprint

pp = pprint.PrettyPrinter(indent=4)

print(os.getcwd())

# Navigate to the 'data' folder
os.chdir("/Users/annaolsen/Desktop/Speciale/DS_thesis/data")


def main():
    # Load original data sets
    df_bio = pd.read_csv("Tara_Biodiversity.csv")
    df_depth = pd.read_csv("Tara_Environmental_Depth.csv")
    df_meso = pd.read_csv("Tara_Environmental_Mesoscale.csv")
    df_meso_SL = pd.read_csv("Tara_Env_Meso_SampleLocation.csv")

    df_bio_u = pd.read_csv("Bio_Unique.csv")
    df_meso_u = pd.read_csv("Meso_Unique.csv")
    df_depth_u = pd.read_csv("Depth_Unique.csv")

    # Create dataframes with info about the data
    tara_bio_info_df = create_info_df(df_bio)
    tara_depth_info_df = create_info_df(df_depth)
    tara_meso_info_df = create_info_df(df_meso)
    meso_SL_info_df = create_info_df(df_meso_SL)

    bio_unique_df = create_info_df(df_bio_u)
    meso_unique_df = create_info_df(df_meso_u)
    depth_unique_df = create_info_df(df_depth_u)

    # Save info dataframes to CSV files
    tara_bio_info_df.to_csv("Tara_Bio_Info.csv", index=False)
    tara_depth_info_df.to_csv("Tara_Depth_Info.csv", index=False)
    tara_meso_info_df.to_csv("Tara_Meso_Info.csv", index=False)
    meso_SL_info_df.to_csv("Tara_Meso_SL_Info.csv", index=False)

    bio_unique_df.to_csv("Bio_Unique_Info.csv", index=False)
    meso_unique_df.to_csv("Meso_Unique_Info.csv", index=False)
    depth_unique_df.to_csv("Depth_Unique_Info.csv", index=False)

    # merged_info_df.to_csv("Tara_merged_info.csv", index=False)

    # Print info about dataframes
    count_elements(df_bio, "bio")
    count_elements(df_depth, "depth")
    count_elements(df_meso, "meso")
    count_elements(df_meso_SL, "meso (sample location)")

    count_elements(df_bio_u, "Bio (unique)")
    count_elements(df_meso_u, "Meso (unique)")
    count_elements(df_depth_u, "Depth (unique)")


def create_info_df(df):

    rows = []

    # Iterate through each column in the original dataframe
    for column in df.columns:

        # Count the number of NaN values in each column
        nan_count = df[column].isna().sum()

        # Count the number of non-NaN values in each column
        value_count = df[column].notna().sum()

        # Calculate NaN count percentage
        nan_percentage = round((nan_count / len(df)) * 100, 2)

        # Get data type of the column
        data_type = df[column].dtype

        # Create a dictionary containing column information
        row = {'Column Name': column, 'NaN Count': nan_count,
               'NaN Percentage': nan_percentage,
               'Value Count': value_count, 'Dtype': data_type}

        rows.append(row)

    info_df = pd.DataFrame(rows)

    return info_df


def count_elements(df, df_name):

    # Get the shape of the dataframe (rows, columns)
    total_rows, total_columns = df.shape

    # Calculate the total number of elements (rows * columns)
    total_elements = total_rows * total_columns

    # Calculate the total number of NaN values in the entire dataframe
    total_nan_count = df.isna().sum().sum()

    # Calculate the percentage of NaN values out of the total elements
    percentage_nan = (total_nan_count / total_elements) * 100

    # Print the results
    print(f"\n{df_name.upper()}:")
    print("Total number of rows:", total_rows)
    print("Total number of columns:", total_columns)
    print("Total number of elements (rows * columns):", total_elements)
    print("Total number of NaN values:", total_nan_count)
    print("Percentage of NaN values out of total elements: {:.2f}%".format(
        percentage_nan))


if __name__ == "__main__":
    main()
