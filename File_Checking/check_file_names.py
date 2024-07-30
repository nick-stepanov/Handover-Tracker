import json
import argparse

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

def categorize_files(file_list):
    categorized_files = {cat: [] for cat in categories}
    
    for file_info in file_list:
        file_name = file_info['file_name'].lower()
        file_path = file_info['file_path'].lower()
        
        for category, keywords in categories.items():
            if any(keyword in file_name or keyword in file_path for keyword in keywords):
                categorized_files[category].append(file_info['file_path'])
    
    return categorized_files

def main():
    parser = argparse.ArgumentParser(description="Categorize files based on predefined keywords.")
    parser.add_argument("input_file", help="Path to the input JSON file (file_list.json)")
    parser.add_argument("output_file", help="Path to the output JSON file (handover_checklist_summary.json)")
    args = parser.parse_args()

    with open(args.input_file, 'r') as f:
        file_list = json.load(f)

    categorized_files = categorize_files(file_list)

    summary_data = []
    for category, files in categorized_files.items():
        summary_data.append({
            "Category": category,
            "Files Found": len(files),
            "Files": ", ".join(files) if files else "No files found"
        })

    with open(args.output_file, 'w') as f:
        json.dump(summary_data, f, indent=2)

    print(f"Categorized file summary has been saved to {args.output_file}")

if __name__ == "__main__":
    main()