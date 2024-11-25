import numpy as np
# import pandas as pd
import al_extract_raw
import al_extract_result
import json

def compute_alignment_score(reference, proposed):
    """
    Computes a numeric score indicating how well-aligned the proposed timepoints
    are to the reference timepoints.

    Args:
        reference (list of float): The reference timepoints.
        proposed (list of float): The proposed timepoints.

    Returns:
        dict: A dictionary with alignment metrics.
    """
    # Sort the lists to ensure efficient computation
    reference = np.sort(np.array(reference))
    proposed = np.sort(np.array(proposed))
    
    # Find the nearest reference timepoint for each proposed timepoint
    nearest_distances = np.abs(proposed[:, None] - reference).min(axis=1)
    
    # Penalty for unmatched timepoints
    unmatched_penalty = abs(len(reference) - len(proposed))
    
    # Compute alignment metrics
    mae = np.mean(nearest_distances)  # Mean Absolute Error
    rmse = np.sqrt(np.mean(nearest_distances ** 2))  # Root Mean Squared Error
    total_error = np.sum(nearest_distances) + unmatched_penalty
    
    return {
        'mae': mae,
        'rmse': rmse,
        'total_error': total_error,
        'unmatched_penalty': unmatched_penalty,
        'nearest_distances': nearest_distances.tolist()
    }

# Example Usage
# reference_timepoints = [10.0, 20.0, 30.0, 40.0, 50.0]
reference_timepoints = al_extract_raw.main()

# proposed_timepoints = [9.5, 21.0, 31.5, 45.0]
proposed_timepoints = al_extract_result.main()

alignment_score = compute_alignment_score(reference_timepoints, proposed_timepoints)

# Save the dictionary as a JSON file
json_file_path = "OUTPUT/align_.json"  # Specify the file name
with open(json_file_path, "w") as json_file:
    json.dump(alignment_score, json_file, indent=4)  # indent=4 for pretty formatting

print(f"Dictionary saved as JSON in {json_file_path}")

print("Alignment Score:", alignment_score)
