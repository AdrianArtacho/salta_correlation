import gui.gui_browse_t as gui_browse
import pandas as pd

def extract_timepoints(file_path, time_column):
    """
    Extracts timepoints from a specified column in a CSV file and converts them to floats in seconds.

    Args:
        file_path (str): Path to the CSV file.
        time_column (str): Name of the column containing time values.

    Returns:
        list of float: Time values converted to seconds.
    """
    df = pd.read_csv(file_path)
    # Convert time values to seconds
    time_in_seconds = (
        df[time_column]
        .dropna()  # Remove any NaN values
        .apply(lambda x: sum(float(t) * 60**i for i, t in enumerate(reversed(x.split(":")))))
        .tolist()
    )
    return time_in_seconds

def main():
    text = "Choose reference file (alignment)"
    print(text+'\n')
    file_path = gui_browse.main(params_title=text,         # params_title
                                params_initbrowser="INPUT/",   # params_initbrowser
                                params_extensions=".csv")

    # Example Usage
    timepoints = extract_timepoints(file_path, '00:00')
    print(timepoints)

    return timepoints

if __name__ == "__main__":
    timepoints = main()