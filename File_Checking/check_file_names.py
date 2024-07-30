import json
import pandas as pd
import re

# Load the file list from JSON
with open('file_list.json', 'r') as f:
    file_list = json.load(f)

# Convert the list of dictionaries to a DataFrame
df = pd.DataFrame(file_list)

# Define categories and associated keywords
categories = {
    "Building Control": ["building control", "buildingcontrol"],
    "Fire Strategy": ["fire strategy", "firestrategy"],
    "R38 Information": ["r38", "r 38"],
    "As Builts Areas": ["as built", "asbuilt"],
    "Air Test Certificates": ["air test", "airtest"],
    "Incoming services": ["incoming service"],
    "M&E Certification": ["m&e", "mechanical electrical"],
    "Metering: Testing & Commissioning": ["metering", "commissioning"],
    "Fire alarm certification": ["fire alarm", "cause and effect", "cause & effect"],
    "Water installations": ["water installation"],
    "Hydraulic Pressure Test": ["hydraulic", "pressure test"],
    "Cooling & Heating systems": ["cooling", "heating"],
    "Soil & Vent and RWP System": ["soil", "vent", "rwp"],
    "Mechanical Extract Ventilation": ["mechanical extract", "ventilation"],
    "Control Systems, BMS and Plant": ["control system", "bms", "plant"],
    "Electrical Installations": ["electrical"],
    "Emergency Lighting": ["emergency lighting"],
    "Lighting & Lighting Control": ["lighting control"],
    "Lighting Protection": ["lighting protection"],
    "Dry Riser/Sprinkler": ["dry riser", "sprinkler"],
    "Door Access": ["door access"],
    "Intercom": ["intercom"],
    "Fire Stopping": ["fire stop"],
    "Lift Installation": ["lift"],
    "TV Installation": ["tv", "television"],
    "Acoustics": ["acoustic"],
    "NHBC": ["nhbc"],
    "Snagging lists": ["snag"],
    "Overheating Report": ["overheat"],
    "EWS1 Forms": ["ews1"],
    "Window cleaning": ["window cleaning"],
    "Extra item(s) - EPC": ["epc"]
}

# Initialize dictionary to store files for each category
categorized_files = {cat: [] for cat in categories}

# Categorize files
for _, row in df.iterrows():
    file_name = row['file_name'].lower()
    file_path = row['file_path'].lower()
    
    for category, keywords in categories.items():
        if any(keyword in file_name in file_path for keyword in keywords):
            categorized_files[category].append(row['file_path'])

# Create a summary DataFrame
summary_data = []
for category, files in categorized_files.items():
    summary_data.append({
        "Category": category,
        "Files Found": len(files),
        "Files": ", ".join(files) if files else "No files found"
    })

summary_df = pd.DataFrame(summary_data)

# Display summary
print(summary_df[["Category", "Files Found"]])

# Save detailed results to JSON
json_file_path = "handover_checklist_summary.json"
with open(json_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(summary_data, json_file, indent=2, ensure_ascii=False)
print(f"Detailed summary saved to '{json_file_path}'")

# Save detailed results to CSV
summary_df.to_csv("handover_checklist_summary.csv", index=False)
print("\nDetailed summary saved to 'handover_checklist_summary.csv'")



# Identify missing categories
missing_categories = summary_df[summary_df["Files Found"] == 0]["Category"].tolist()
if missing_categories:
    print("\nWarning: No files found for these categories:")
    for cat in missing_categories:
        print(f"- {cat}")
else:
    print("\nAll categories have at least one file.")