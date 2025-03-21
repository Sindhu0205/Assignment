import os
import pandas as pd
import pytest
from assignment import read_csv_files, read_json_files, process_player_data, validate_output

# Define test directories (Assume test data exists here)
TEST_INPUT_DIR = "inputDataSet"
TEST_OUTPUT_DIR = "outputDataSet"


TEMP_DIR = "tempDataSet"


@pytest.fixture
def sample_data():
    """Fixture to create a sample DataFrame for testing."""
    data = {
        "eventType": ["ODI", "Test", "Test"],
        "playerName": ["Player A", "Player B", "Player C"],
        "age": [25, 40, 17],
        "runs": [600, 450, 300],
        "wickets": [55, 10, 5]
    }
    return pd.DataFrame(data)


def test_read_csv_files():
    """Test if CSV files are read correctly."""
    df = read_csv_files(TEST_INPUT_DIR)
    assert isinstance(df, pd.DataFrame), "CSV data should be a DataFrame"
    assert not df.empty, "CSV data should not be empty"


def test_read_json_files():
    """Test if JSON files are read correctly."""
    df = read_json_files(TEST_INPUT_DIR)
    assert isinstance(df, pd.DataFrame), "JSON data should be a DataFrame"
    assert not df.empty, "JSON data should not be empty"


def test_process_player_data(sample_data):
    """Test player type classification and data filtering logic."""
    processed_df = process_player_data(sample_data)

    # Ensure 'playerType' column exists
    assert "playerType" in processed_df.columns, "Missing column: playerType"

    # Validate player type classification
    assert processed_df.loc[processed_df["playerName"] == "Player A", "playerType"].values[0] == "All-Rounder"
    assert processed_df.loc[processed_df["playerName"] == "Player B", "playerType"].values[0] == "Batsman"
    assert processed_df.loc[processed_df["playerName"] == "Player C", "playerType"].values[0] == "Bowler"


def test_schema_validation(sample_data):
    """Test if output schema matches expected structure."""
    processed_df = process_player_data(sample_data)

    expected_schema = {
        "eventType": "object",
        "playerName": "object",
        "age": "int64",
        "runs": "int64",
        "wickets": "int64",
        "playerType": "object"
    }

    for col, dtype in expected_schema.items():
        assert col in processed_df.columns, f"Missing column: {col}"
        assert processed_df[col].dtype == dtype, f"Incorrect data type for {col}, expected {dtype}"


def test_validate_output(sample_data):
    """Test the validation function against expected output."""
    processed_df = process_player_data(sample_data)

    # Assuming test_outputDataSet has correct expected outputs
    validation_df = validate_output(processed_df, TEST_OUTPUT_DIR)

    assert "Result" in validation_df.columns, "Missing column: Result"
    assert all(validation_df["Result"].isin(["PASS", "FAIL"])), "Invalid result values"


if __name__ == "__main__":
    pytest.main(["-v", "--html=report.html", "--self-contained-html"])  # Generates HTML report
