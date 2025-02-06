import os
import pandas as pd

def remove_columns_from_events(bids_dir):
    # Define columns to remove
    columns_to_remove = ['onset', 'duration', 'response_time', 'trial_number', '73k_id']
    
    # Traverse the BIDS directory
    for root, dirs, files in os.walk(bids_dir):
        for file in files:
            if file.endswith('_events.tsv'):
                file_path = os.path.join(root, file)
                print(f"Processing file: {file_path}")
                
                # Read the TSV file
                df = pd.read_csv(file_path, sep='\t')
                
                # Modify 73k_id values if the column exists
                if '73k_id' in df.columns:
                    df['73k_id'] = df['73k_id'].apply(lambda x: f"coco_{x}" if pd.notnull(x) else x)

                # Remove the specified columns if they exist
                df = df.drop(columns=[col for col in columns_to_remove if col in df.columns], errors='ignore')
                
                # Save the modified file back
                df.to_csv(file_path, sep='\t', index=False)
                print(f"Updated file saved: {file_path}")


bids_directory_path = "/nas-tmp/research/03-Neural_decoding/3-bids"
remove_columns_from_events(bids_directory_path)
