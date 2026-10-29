import sys
import re
from flask import Flask, render_template_string, request

import main

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="font-family: sans-serif; max-width: 900px; margin: 30px auto; padding: 0 20px;">
<form method="POST">
<select name="mode" style="width:100%;font-size:16px;padding:8px;">
<option value="pre" {% if mode == 'pre' %}selected{% endif %}>Proofread English</option>
<option value="prg" {% if mode == 'prg' %}selected{% endif %}>Proofread German</option>
<option value="tte" {% if mode == 'tte' %}selected{% endif %}>Translate to English</option>
<option value="ttg" {% if mode == 'ttg' %}selected{% endif %}>Translate to German</option>
</select><br><br>
<textarea name="text" rows="8" placeholder="Text to correct" style="width:100%;font-size:16px;padding:10px;box-sizing:border-box;">{{ text }}</textarea><br><br>
<input type="text" name="note" value="{{ note }}" placeholder="Optional hint/note" style="width:100%;font-size:16px;padding:10px;box-sizing:border-box;"><br><br>
<button type="submit" style="font-size:18px;padding:12px 24px;">Run Leek</button>
</form>
<h3>Output:</h3>
<pre style="white-space:pre-wrap;background:#1e1e1e;color:#d4d4d4;padding:15px;font-family:monospace;font-size:16px;line-height:1.5;border-radius:6px;">{{ output|safe }}</pre>
</body>
</html>
"""


def ansi_to_html(text):
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    def replace_ansi(match):
        code = match.group(1)
        if not code or code == "0":
            return "</span>"
        parts = code.split(";")
        styles = []
        i = 0
        while i < len(parts):
            if parts[i] == "38" and i + 4 < len(parts) and parts[i + 1] == "2":
                styles.append(
                    f"color: rgb({parts[i + 2]},{parts[i + 3]},{parts[i + 4]})"
                )
                i += 5
            elif parts[i] == "48" and i + 4 < len(parts) and parts[i + 1] == "2":
                styles.append(
                    f"background-color: rgb({parts[i + 2]},{parts[i + 3]},{parts[i + 4]})"
                )
                i += 5
            elif parts[i] == "34":
                styles.append("color: #3498db")
                i += 1
            else:
                i += 1
        if styles:
            return f'<span style="{"; ".join(styles)}">'
        return ""

    text = re.sub(r"\x1b\[([0-9;]*)m", replace_ansi, text)
    text = re.sub(r"\x1b\[[0-9;]*[a-zA-Z]", "", text)
    return text + "</span>" * 10


@app.route("/", methods=["GET", "POST"])
def index():
    output = ""
    mode = "pre"
    text = ""
    note = ""

    if request.method == "POST":
        mode = request.form.get("mode", "pre")
        text = request.form.get("text", "")
        note = request.form.get("note", "")

        args = ["main.py", mode, "-s", text]
        if note:
            args.append(note)

        old_argv = sys.argv
        sys.argv = args

        try:
            raw_output = main.execute() or ""
        except Exception as e:
            raw_output = f"Execution error: {str(e)}"
        finally:
            sys.argv = old_argv

        output = ansi_to_html(raw_output)

    return render_template_string(
        HTML_TEMPLATE, output=output, mode=mode, text=text, note=note
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
