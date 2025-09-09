from flask import Flask, request, send_file, render_template
import os, shutil, zipfile, subprocess


# Create Flask app
app = Flask(__name__, template_folder="templates")

# Home route -> render index.html
@app.route("/")
def home():
    return render_template("index.html")

# Start server
if __name__ == "__main__":
    # Run in production mode
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,         # disables debug PIN + lazy loading
        use_reloader=False   # disables auto-reloader (no lazy loading message)
    )