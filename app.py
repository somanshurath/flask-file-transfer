from flask import Flask, render_template, request, send_from_directory, redirect, url_for
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
CLIPBOARD_FILE = './clipboard.txt'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
if not os.path.exists(CLIPBOARD_FILE):
    with open(CLIPBOARD_FILE, "w") as clipboard:
        pass


@app.route('/')
def index():
    files = os.listdir(UPLOAD_FOLDER)
    return render_template('index.html', files=files)


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    return redirect(url_for('index'))


@app.route('/delete/<filename>')
def delete_file(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return redirect(url_for('index'))
    else:
        return 'File not found'


@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


@app.route('/clipboard')
def clipboard():
    clipboard = open(CLIPBOARD_FILE, "r+")
    texts = clipboard.read().split("@#@")
    clipboard.close()
    return render_template('clipboard.html', texts=texts)

@app.route('/add-text', methods=['POST'])
def add_text():
    text = request.form['text']
    with open(CLIPBOARD_FILE, "a") as clipboard:
        text = text.strip()
        clipboard.write("@#@" + text)
    return redirect(url_for('clipboard'))


@app.route('/delete-text/<text>')
def delete_text(text):
    with open(CLIPBOARD_FILE, "r+") as clipboard:
        texts = clipboard.read().split("@#@")
        if text in texts:
            texts.remove(text)
            clipboard.seek(0)
            clipboard.write("@#@".join(texts))
            clipboard.truncate()
    return redirect(url_for('clipboard'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)
