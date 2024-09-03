import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import os
import mimetypes
import sys

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import functions from other scripts using the correct relative paths
from File_Processing.Get_all_files_register import get_all_files
from File_Checking.check_file_names import categorize_files

# Global variable to store the current directory
current_directory = ""

html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Handover Checklist Dashboard</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; cursor: pointer; }}
        tr:nth-child(even) {{ background-color: #f9f9f9; }}
        .file-link {{ color: blue; text-decoration: none; }}
        .file-link:hover {{ text-decoration: underline; }}
        #filter, #directory {{ width: 100%; padding: 8px; margin-bottom: 10px; }}
        .files-cell {{ max-width: 500px; overflow: hidden; text-overflow: ellipsis; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Handover Checklist Dashboard</h1>
        <input type="text" id="directory" placeholder="Paste your directory path here" value="{current_directory}">
        <button onclick="updateDirectory()">Update Directory</button>
        <input type="text" id="filter" placeholder="Filter by category or file name">
        <table id="dashboardTable">
            <thead>
                <tr>
                    <th onclick="sortTable(0)">Category</th>
                    <th onclick="sortTable(1)">Files Found</th>
                    <th>Files</th>
                </tr>
            </thead>
            <tbody>
                {table_rows}
            </tbody>
        </table>
    </div>
    <script>
        function updateDirectory() {{
            var directory = document.getElementById('directory').value;
            fetch('/update_directory', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/x-www-form-urlencoded',
                }},
                body: 'directory=' + encodeURIComponent(directory)
            }})
            .then(response => response.json())
            .then(data => {{
                if (data.status === 'success') {{
                    alert('Directory updated successfully. Refreshing page...');
                    location.reload();
                }} else {{
                    alert('Failed to update directory: ' + data.message);
                }}
            }});
        }}

        function sortTable(n) {{
            // ... (sortTable function code) ...
        }}

        document.getElementById('filter').addEventListener('keyup', function() {{
            // ... (filter function code) ...
        }});
    </script>
</body>
</html>
"""

def process_directory(directory):
    # Step 1: Generate file list
    file_list = get_all_files(directory)
    file_list_path = os.path.join(directory, "file_list.json")
    with open(file_list_path, 'w') as f:
        json.dump(file_list, f, indent=2)
    
    # Step 2: Categorize files
    categorized_files = categorize_files(file_list)
    summary_data = []
    for category, files in categorized_files.items():
        summary_data.append({
            "Category": category,
            "Files Found": len(files),
            "Files": ", ".join(files) if files else "No files found"
        })
    
    summary_path = os.path.join(directory, "handover_checklist_summary.json")
    with open(summary_path, 'w') as f:
        json.dump(summary_data, f, indent=2)
    
    return summary_data

def load_data(directory):
    json_path = os.path.join(directory, 'handover_checklist_summary.json')
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {json_path} not found. Processing directory...")
        return process_directory(directory)

def generate_table_rows(data):
    rows = []
    for item in data:
        files_html = ""
        if item['Files'] == "No files found":
            files_html = '<span style="color: red;">No files found</span>'
        else:
            files = item['Files'].split(', ')
            files_html = '<div class="files-cell">' + '<br>'.join([
                f'<a href="/open?file={urllib.parse.quote(file)}" class="file-link" target="_blank">{os.path.basename(file)}</a>'
                for file in files
            ]) + '</div>'
        
        row = f"""
        <tr>
            <td>{item['Category']}</td>
            <td>{item['Files Found']}</td>
            <td>{files_html}</td>
        </tr>
        """
        rows.append(row)
    return '\n'.join(rows)

class DashboardHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global current_directory
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            if current_directory:
                data = load_data(current_directory)
                table_rows = generate_table_rows(data)
            else:
                table_rows = "<tr><td colspan='3'>Please set a directory first.</td></tr>"
            self.wfile.write(html_content.format(current_directory=current_directory, table_rows=table_rows).encode())
        elif self.path.startswith('/open'):
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
            if 'file' in params:
                file_path = params['file'][0]
                if os.path.exists(file_path):
                    self.send_response(200)
                    mime_type, _ = mimetypes.guess_type(file_path)
                    self.send_header('Content-type', mime_type if mime_type else 'application/octet-stream')
                    self.send_header('Content-Disposition', f'inline; filename="{os.path.basename(file_path)}"')
                    self.end_headers()
                    with open(file_path, 'rb') as file:
                        self.wfile.write(file.read())
                else:
                    self.send_error(404, f'File not found: {file_path}')
            else:
                self.send_error(400, 'Bad Request')
        else:
            self.send_error(404)

    def do_POST(self):
        global current_directory
        if self.path == '/update_directory':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            params = urllib.parse.parse_qs(post_data)
            if 'directory' in params:
                new_directory = params['directory'][0]
                if os.path.exists(new_directory):
                    current_directory = new_directory
                    process_directory(current_directory)
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'status': 'success'}).encode())
                else:
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'status': 'error', 'message': 'Directory does not exist'}).encode())
            else:
                self.send_error(400, 'Bad Request')
        else:
            self.send_error(404)

def run(server_class=HTTPServer, handler_class=DashboardHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Server running on http://localhost:{port}")
    print("Open this URL in your web browser and enter the directory path in the provided input field.")
    httpd.serve_forever()

if __name__ == '__main__':
    run()