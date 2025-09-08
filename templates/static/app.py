from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session
import os
from werkzeug.utils import secure_filename

# ===== Configurações iniciais =====
app = Flask(__name__)
app.secret_key = "chave_super_secreta"  # troca por algo seguro

UPLOAD_FOLDER = "uploads"
PROFILE_FOLDER = "profile"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROFILE_FOLDER, exist_ok=True)

# ===== Credenciais do administrador =====
ADMIN_USER = "admin"
ADMIN_PASS = "1234"  # troca por uma senha forte

# ===== Página inicial pública (lista vídeos) =====
@app.route("/")
def home():
    videos = os.listdir(UPLOAD_FOLDER)
    return render_template("index.html", videos=videos)

# ===== Login do administrador =====
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == ADMIN_USER and password == ADMIN_PASS:
            session["admin"] = True
            return redirect(url_for("dashboard"))
    return render_template("login.html")

# ===== Painel do administrador =====
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "admin" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        # Upload de vídeo
        if "video" in request.files:
            f = request.files["video"]
            if f:
                filename = secure_filename(f.filename)
                f.save(os.path.join(UPLOAD_FOLDER, filename))

        # Upload de foto de perfil
        if "profile" in request.files:
            f = request.files["profile"]
            if f:
                filename = "profile.jpg"
                f.save(os.path.join(PROFILE_FOLDER, filename))

    videos = os.listdir(UPLOAD_FOLDER)
    profile_exists = os.path.exists(os.path.join(PROFILE_FOLDER, "profile.jpg"))
    return render_template("dashboard.html", videos=videos, profile=profile_exists)

# ===== Página de vídeo público =====
@app.route("/video/<name>")
def video(name):
    return render_template("video.html", video=name)

# ===== Servir arquivos de vídeo =====
@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# ===== Servir foto de perfil =====
@app.route("/profile/<path:filename>")
def profile_file(filename):
    return send_from_directory(PROFILE_FOLDER, filename)

# ===== Rodar o servidor =====
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
