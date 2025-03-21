import os
import pandas as pd
import json


def read_csv_files(directory):
    # Reading CSV files from the given directory
    df_list = []
    for file in os.listdir(directory):
        if file.endswith(".csv"):
            df_list.append(pd.read_csv(os.path.join(directory, file), sep=';'))
    return pd.concat(df_list, ignore_index=True) if df_list else pd.DataFrame()


def read_json_files(directory):
    # Reading all JSON files from the given directory
    df_list = []
    for file in os.listdir(directory):
        if file.endswith(".json"):
            with open(os.path.join(directory, file), 'r') as f:
                data = [json.loads(line) for line in f]  # Read each JSON object separately
                df_list.append(pd.DataFrame(data))  # Convert JSON to DataFrame
    return pd.concat(df_list, ignore_index=True) if df_list else pd.DataFrame()


def process_player_data(df):
    # Processing the player data according to the given rules
    df = df.dropna(subset=['runs', 'wickets', 'age'])
    df = df[(df['age'] >= 15) & (df['age'] <= 50)]

    df['playerType'] = df.apply(
        lambda row: "All-Rounder" if row['runs'] > 500 and row['wickets'] > 50
        else "Batsman" if row['runs'] > 500
        else "Bowler",
        axis=1
    )

    df[['runs', 'wickets', 'age']] = df[['runs', 'wickets', 'age']].astype(int)

    return df


def validate_output(processed_df, output_directory):
    # Validate the processed data against the data available in output directory
    result_list = []

    for file in os.listdir(output_directory):
        if file.endswith(".csv"):
            output_df = pd.read_csv(os.path.join(output_directory, file), sep=';')
            event_type = file.split('.')[0].upper()  # Extract event type from filename
            expected_df = processed_df[processed_df['eventType'] == event_type]

            merged_df = expected_df.merge(output_df,
                                          on=['playerName', 'eventType', 'age', 'runs', 'wickets', 'playerType'],
                                          how='left', indicator=True)
            merged_df['Result'] = merged_df['_merge'].apply(lambda x: 'PASS' if x == 'both' else 'FAIL')
            result_list.append(merged_df.drop(columns=['_merge']))

    if result_list:
        final_result_df = pd.concat(result_list, ignore_index=True)
        final_result_df.to_csv('test_result.csv', index=False, sep=';')
        return final_result_df
    return pd.DataFrame()


def main():
    input_dir = "inputDataSet"
    output_dir = "outputDataSet"

    # Step 1: Read the CSV and JSON files
    csv_data = read_csv_files(input_dir)
    json_data = read_json_files(input_dir)

    # Step 2: Merge the data
    merged_data = pd.concat([csv_data, json_data], ignore_index=True)

    # Step 3: Create 'tempDataSet' directory if it does not exist
    temp_dir = "tempDataSet"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)  # Create the folder if it doesn't exist
        print(f"Directory '{temp_dir}' created.")
    else:
        print(f"Directory '{temp_dir}' already exists.")

    # Step 4: Process the player data
    processed_data = process_player_data(merged_data)
    processed_data_file_path = os.path.join(temp_dir, "processed_data.csv")
    processed_data.to_csv(processed_data_file_path, index=False, sep=';')
    print(f"Data has been merged and stored in: {processed_data_file_path}")

    # Step 5: Validate output considering given output data
    test_results = validate_output(processed_data, output_dir)


if __name__ == "__main__":
    main()
