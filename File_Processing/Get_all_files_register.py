#This creates a registry of all files in the target folder.

import os
import pandas as pd

# Specify the directory
directory = r"C:\Users\Nick.Stepanov\OneDrive - OTAK INC\Visual Code\Handover Checklist\Project Docs\Block F & G"

# Initialize lists to store file names and paths
file_names = []
file_paths = []

# Walk through the directory
for root, dirs, files in os.walk(directory):
    for file in files:
        file_names.append(file)
        file_paths.append(os.path.join(root, file))

# Create the DataFrame
df = pd.DataFrame({
    'file_name': file_names,
    'file_path': file_paths
})

# Display the first few rows of the DataFrame
print(df.head())

# 4. Save as JSON
df.to_json('file_list.json', orient='records')
print("JSON file saved as 'file_list.json'")