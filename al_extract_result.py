import gui.gui_browse_t as gui_browse
import pandas as pd


def extract_columns(file_path, time_column, peaks_column):
    """
    Extracts and processes timepoints and peaks values from a CSV file.

    Args:
        file_path (str): Path to the CSV file.
        time_column (str): Name of the column containing time values.
        peaks_column (str): Name of the column containing peaks values.

    Returns:
        tuple of lists: (timepoints_in_seconds, peaks_processed)
    """
    df = pd.read_csv(file_path)
    
    # Convert time values to seconds (e.g., "1m32.433s" to 92.433)
    time_in_seconds = (
        df[time_column]
        .dropna()  # Remove any NaN values
        .apply(lambda x: sum(float(t) * 60**i for i, t in enumerate(reversed(x.replace('s', '').split('m')))))
        .tolist()
    )
    
    # Process peaks values (e.g., divide by 100 and round to 2 decimal points)
    peaks_processed = (
        df[peaks_column]
        .dropna()  # Remove any NaN values
        .apply(lambda x: round(x / 100, 2))
        .tolist()
    )
    
    return time_in_seconds, peaks_processed

def main():
    text = "Choose second file (to compare to reference)"
    print(text+'\n')
    file_path_2 = gui_browse.main(params_title=text,         # params_title
                                params_initbrowser="INPUT/",   # params_initbrowser
                                params_extensions=".csv")

    # Example Usage
    timepoints, peaks = extract_columns(file_path_2, 'peaks_timecode', 'peaks_unscaled')

    timepoints, peaks

    print("timepoints")
    print(timepoints)
    print("")
    print("peaks")
    print(peaks)

    return timepoints

if __name__ == "__main__":
    timepoints = main()