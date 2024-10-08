# Handover Checklist Project

This project provides a tool to manage and visualize a handover checklist for construction or development projects. It includes functionality for file registration, categorization, and a web-based dashboard for easy viewing.

## Project Structure

The project is organized as follows:

```
handover-checklist-project/
├── Handover_checklist_UI/
│   └── generate_dashboard.py
├── File_Processing/
│   └── get_all_files_register.py
├── File_Checking/
│   └── check_file_names.py
└── README.md
```

## Installation

To use this script, you need Python 3.6 or later. Clone this repository to your local machine:

```
git clone https://github.com/your-username/handover-checklist-project.git
cd handover-checklist-project
```

Install the required Python packages:

```
pip install pandas
```

## Usage

To start the dashboard, navigate to the Handover_checklist_UI directory and run:

```
cd Handover_checklist_UI
python generate_dashboard.py
```

This will start a local web server. The console will display a message indicating where temporary files will be stored. These files are used internally by the script and will not affect your project directories.

Open your web browser and navigate to `http://localhost:8000` to view the dashboard.

On the dashboard:
1. You'll see an input field at the top of the page.
2. Paste the full path to your project directory (where your project files are located) into this field.
3. Click the "Update Directory" button.
4. The script will automatically:
   - Generate a list of all files in the directory
   - Categorize the files based on predefined keywords
   - Create a summary of the categorized files
   - Display the results in the dashboard

You can change the directory at any time by entering a new path and clicking "Update Directory". The script will reprocess the new directory and update the dashboard.

## Important Notes

- The script does not create or modify any files in your target directory. All intermediate files are stored in a temporary directory created by the system.
- The temporary files are automatically cleaned up when the script exits or when the system reboots.

## Customization

To modify the categories or keywords used for file categorization, edit the `categories` dictionary in the `File_Checking/check_file_names.py` file.

## Troubleshooting

If you encounter issues:

1. Ensure the directory path you entered is correct and you have permission to access it.
2. Check the console output for any error messages.
3. Verify that the directory contains the files you expect to be categorized.
4. Make sure you're running the script from the correct directory (Handover_checklist_UI).
5. If you're having issues with file access, check that the script has necessary permissions to read the target directory and create temporary files.

## Contributing

Contributions to this project are welcome. Please fork the repository and submit a pull request with your changes.

## Using the Executable

For Windows users who don't have Python installed, we provide a standalone executable version of the Handover Checklist tool.

1. Download the `gui_dashboard.exe` file from the `executable_files` folder [provide download link or location].
2. Double-click the `gui_dashboard.exe` file to run the application.
3. Use the "Browse" button to select a directory for analysis.
4. Click "Process Directory" to analyze the files.
5. View the results in the tree view:
   - Categories are shown in grey with the number of files found.
   - Files are listed under each category.
   - Double-click a file to open it with the default application.
6. Click "Generate Excel Register" (or "Generate CSV Register" if Excel export is not available) to create a report of the processed data.

Note: If you encounter any "missing DLL" errors, you may need to install the Microsoft Visual C++ Redistributable package on your system. You can download it from the official Microsoft website.