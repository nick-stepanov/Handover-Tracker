import json
import pandas as pd
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import os
import mimetypes

# Load data from JSON file
with open('handover_checklist_summary.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Get the directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))

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
        #filter {{ width: 100%; padding: 8px; margin-bottom: 10px; }}
        .files-cell {{ max-width: 500px; overflow: hidden; text-overflow: ellipsis; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Handover Checklist Dashboard</h1>
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
        function sortTable(n) {{
            var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
            table = document.getElementById("dashboardTable");
            switching = true;
            dir = "asc";
            while (switching) {{
                switching = false;
                rows = table.rows;
                for (i = 1; i < (rows.length - 1); i++) {{
                    shouldSwitch = false;
                    x = rows[i].getElementsByTagName("TD")[n];
                    y = rows[i + 1].getElementsByTagName("TD")[n];
                    if (dir == "asc") {{
                        if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {{
                            shouldSwitch = true;
                            break;
                        }}
                    }} else if (dir == "desc") {{
                        if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {{
                            shouldSwitch = true;
                            break;
                        }}
                    }}
                }}
                if (shouldSwitch) {{
                    rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
                    switching = true;
                    switchcount++;
                }} else {{
                    if (switchcount == 0 && dir == "asc") {{
                        dir = "desc";
                        switching = true;
                    }}
                }}
            }}
        }}

        document.getElementById('filter').addEventListener('keyup', function() {{
            var filter = this.value.toLowerCase();
            var table = document.getElementById("dashboardTable");
            var tr = table.getElementsByTagName("tr");

            for (var i = 1; i < tr.length; i++) {{
                var td = tr[i].getElementsByTagName("td");
                var displayStyle = "none";
                for (var j = 0; j < td.length; j++) {{
                    var cell = td[j];
                    if (cell) {{
                        if (cell.innerHTML.toLowerCase().indexOf(filter) > -1) {{
                            displayStyle = "";
                            break;
                        }}
                    }}
                }}
                tr[i].style.display = displayStyle;
            }}
        }});
    </script>
</body>
</html>
"""

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
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            table_rows = generate_table_rows(data)
            self.wfile.write(html_content.format(table_rows=table_rows).encode())
        elif self.path.startswith('/open'):
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
            if 'file' in params:
                file_path = params['file'][0]
                # Try absolute path first
                if not os.path.exists(file_path):
                    # If not found, try relative to script directory
                    file_path = os.path.join(script_dir, file_path)
                
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

def run(server_class=HTTPServer, handler_class=DashboardHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Server running on port {port}")
    print(f"Script directory: {script_dir}")
    httpd.serve_forever()

if __name__ == '__main__':
    run()