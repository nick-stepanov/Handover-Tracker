# Handover-Tracker
Handover Checklist Project
This project provides a set of tools to manage and visualize a handover checklist for construction or development projects. It includes scripts for file registration, categorization, and a web-based dashboard for easy viewing.
Project Structure
The project consists of three main Python scripts:

Get_all_files_register.py: Generates a JSON file containing information about all relevant files in the project.
check_file_names.py: Categorizes files based on predefined keywords and creates a summary.
generate_dashboard.py: Creates a web-based dashboard to visualize the handover checklist data.

Installation
To use these scripts, you need Python 3.6 or later. Clone this repository to your local machine:
Copygit clone https://github.com/your-username/handover-checklist-project.git
cd handover-checklist-project
Install the required Python packages:
Copypip install pandas
Usage
Step 1: Generate File List
Run the following command to generate a JSON file containing all relevant files:
Copypython Get_all_files_register.py
This will create a file_list.json file in the project directory.
Step 2: Categorize Files
Next, run the file name checking script:
Copypython check_file_names.py
This script will read file_list.json, categorize the files based on predefined keywords, and generate a handover_checklist_summary.json file.
Step 3: Generate Dashboard
Finally, to visualize the data, run:
Copypython generate_dashboard.py
This will start a local web server. Open your web browser and navigate to http://localhost:8000 to view the dashboard.
Customization
Directory Path
Before running the scripts, you need to specify the correct directory path for your project. In each script, locate the following line near the top:
pythonCopydirectory = r"C:\Users\Nick.Stepanov\OneDrive - OTAK INC\Visual Code\Handover Checklist\Project Docs\Block F & G"
Replace this path with the path to your project's document directory. Make sure to use a raw string (prefixed with r) or escape backslashes if you're on Windows.
Other Customizations

To modify the categories or keywords used for file categorization, edit the categories dictionary in check_file_names.py.
To change the appearance of the dashboard, modify the HTML and CSS in generate_dashboard.py.

Troubleshooting
If you encounter issues with file paths or permissions, especially when running the dashboard:

Ensure all files are in the correct locations and accessible.
Try running the script as an administrator if on Windows.
Check the console output for detailed error messages and debugging information.
Verify that the directory path is correctly set in all scripts.

Contributing
Contributions to this project are welcome. Please fork the repository and submit a pull request with your changes.