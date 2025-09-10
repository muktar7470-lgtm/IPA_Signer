import os
from flask import Flask, request, render_template, send_file

app = Flask(__name__)
app.secret_key = "supersecret"

UPLOAD_FOLDER = "tmp"
ALLOWED_EXTENSIONS = {"ipa"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# ✅ check if file is .ipa
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def index():
    message = None
    if request.method == "POST":
        ipa = request.files.get("file")
        cert = request.files.get("cert")
        profile = request.files.get("profile")
        password = request.form.get("password")

        if not ipa or ipa.filename == "":
            message = "❌ No IPA file uploaded."
            return render_template("index.html", message=message)

        if not allowed_file(ipa.filename):
            message = "❌ Only .ipa files are allowed."
            return render_template("index.html", message=message)

        # Save uploads
        ipa_path = os.path.join(app.config["UPLOAD_FOLDER"], ipa.filename)
        ipa.save(ipa_path)

        if cert:
            cert.save(os.path.join(app.config["UPLOAD_FOLDER"], cert.filename))
        if profile:
            profile.save(os.path.join(app.config["UPLOAD_FOLDER"], profile.filename))

        print(f"Certificate password: {password}")  # for debug

        # 🔹 Fake signing
        signed_file = ipa_path.replace(".ipa", "_signed.ipa")
        os.rename(ipa_path, signed_file)

        message = "✅ IPA signed successfully!"
        return send_file(signed_file, as_attachment=True)

    return render_template("index.html", message=message)

if __name__ == "__main__":
    app.run(debug=True)