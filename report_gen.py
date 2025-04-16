import re
import json
#
# Replaces tabs and maintains newlines for proper formatting.
#
def convert_tabs_and_newlines(text, tab_size=4):
    return text.replace("\t", " " * tab_size).replace("\n", "\n")

#
# Converts ANSI escape sequences and keywords to inline-styled HTML.
#
def ansi_to_html(text):
    keyword_color_map = {
        "BRIGHT_YELLOW": "#E8CB1A",  # Dark Yellow
        "YELLOW": "#FB9F12",         # Orange
        "RED": "#8B0000",            # Dark Red
        "GREEN": "#006400",          # Dark Green
        "BLUE": "#00008B",           # Dark Blue
    }
    
    # Replace keywords in the text with styled <span> elements.
    for keyword, hex_color in keyword_color_map.items():
        pattern = re.compile(r'\b' + re.escape(keyword) + r'\b')
        text = pattern.sub(rf'<span style="color:{hex_color}">{keyword}</span>', text)

    ansi_color_map = {
        # ANSI standard colors
        '31': 'red',
        '32': 'green',
        '33': '#FB9F12',  # Representing Yellow as Orange
        '34': 'blue',
        '35': 'magenta',
        '36': 'cyan',
        '37': 'black',
        '90': 'gray',
        # Bright colors from ANSI
        '91': '#FF6666',
        '92': '#66FF66',
        '93': '#E8CB1A',  # Representing Bright_Yellow as Dark Yellow
        '94': '#6666FF',
        '95': '#FF66FF',
        '96': '#66FFFF',
        '97': '#FFFFFF'
    }
    
    # Regex pattern for ANSI codes
    ansi_escape = re.compile(r'\x1B\[(?:(\d+);)?(\d+)m')
    
    def replace_ansi(match):
        color_code = match.group(2)
        color = ansi_color_map.get(color_code, 'black')  # Default color is black
        return f'<span style="color:{color}">'
    
    # Replace ANSI codes with styled "<span>" tags.
    styled_text = ansi_escape.sub(replace_ansi, text)
    
    # Add closing </span> tags for every "open" <span>.
    styled_text += '</span>' * styled_text.count('<span')
    
    return styled_text

#
# Generates HTML report
#
def create_html_report(output_files):
    html_content = [
        "<html>",
        "<head>",
        "<style>",
        "body { font-family: monospace; background-color: #E2EAF4; margin: 0.5in; font-size: 18px; }",
        "pre { font-size: 16px; }",
        "ul { margin-top: 0; margin-bottom: 1em; }",
        "</style>",
        "</head>",
        "<body>"
    ]

    for module, file_path in output_files.items():
        html_content.append(f"<h2>{module} Output:</h2>")
        
        if file_path.endswith(".json") and "net_scan_output" in file_path:
            # Custom handling for net_scan_output.json
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                for iface, entries in data.items():
                    html_content.append(f"<h3>Interface: {iface}</h3>")
                    for entry in entries:
                        html_content.append("<ul>")
                        html_content.append(f"<li><strong>Family:</strong> {entry.get('family')}</li>")
                        html_content.append(f"<li><strong>Address:</strong> {entry.get('address')}</li>")
                        html_content.append(f"<li><strong>Netmask:</strong> {entry.get('netmask')}</li>")
                        html_content.append(f"<li><strong>Broadcast:</strong> {entry.get('broadcast')}</li>")

                        if "open_ports" in entry:
                            ports = entry["open_ports"]
                            port_str = ', '.join(str(p) for p in ports) if ports else "None"
                            html_content.append(f"<li><strong>Open Ports:</strong> {port_str}</li>")

                        html_content.append("</ul>")
                    html_content.append("<br>")
            except Exception as e:
                html_content.append(f"<pre><span style='color:red'>Error parsing JSON: {e}</span></pre>")
        elif "os_meta_output.json" in file_path:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            for key, value in data.items():
                val = ', '.join(value) if isinstance(value, list) else value
                html_content.append(f"<strong>{key}:</strong> {val}<br>")
        else:
            # Default behavior for .txt or non-special .json
            html_content.append("<pre>")
            with open(file_path, 'r', encoding='utf-8') as f:
                raw_text = f.read()
                formatted_output = convert_tabs_and_newlines(raw_text)
                styled_output = ansi_to_html(formatted_output)
            html_content.append(styled_output)
            html_content.append("</pre><br>")

    html_content.append("</body></html>")

    with open("report.html", "w", encoding="utf-8") as f:
        f.write("\n".join(html_content))

    print("\n\nSuccessfully generated 'report.html'\n")
