import os
import pandas as pd

def process_events_files(bids_dir, subjects):
    for subject in subjects:  # 특정 subject 디렉토리만 처리
        subject_dir = os.path.join(bids_dir, subject)
        if not os.path.exists(subject_dir):
            print(f"Directory not found: {subject_dir}")
            continue
        
        # Traverse the subject's directory tree
        for root, dirs, files in os.walk(subject_dir):
            for file in files:
                if file.endswith('_events.tsv'):
                    file_path = os.path.join(root, file)
                    print(f"Processing file: {file_path}")
                    
                    # Read the TSV file
                    df = pd.read_csv(file_path, sep="\t")

                    # Rename columns
                    df.rename(columns={'stim_id': 'image', 'trial_no': 'trial_number'}, inplace=True)

                    # Modify image column values
                    if 'image' in df.columns:
                        df['image'] = df['image'].apply(lambda x: f"imagenet_{x}" if pd.notnull(x) and x != 'n/a' else x)

                    # Keep only the specified columns in the correct order
                    columns_order = ['onset', 'duration', 'trial_number', 'image', 'response_time']
                    df = df[[col for col in columns_order if col in df.columns]]

                    # Save the modified file back
                    df.to_csv(file_path, sep="\t", index=False)
                    print(f"Updated file saved: {file_path}")

# Define the BIDS directory and subjects to process
bids_directory_path = "/nas-tmp/research/03-Neural_decoding/3-bids"
subjects_to_process = [f"sub-0{i}" if i < 10 else f"sub-{i}" for i in range(13, 18)]

process_events_files(bids_directory_path, subjects_to_process)
