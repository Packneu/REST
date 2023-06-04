from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

def create_table():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS images
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  data BLOB NOT NULL)''')
    conn.commit()
    conn.close()

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    filename = file.filename
    file.save(f'{app.config["UPLOAD_FOLDER"]}/{filename}')

    with open(f'{app.config["UPLOAD_FOLDER"]}/{filename}', 'rb') as f:
        image_data = f.read()

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO images (name, data) VALUES (?, ?)",
              (filename, image_data))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Image uploaded successfully'})

@app.route('/download/<int:image_id>', methods=['GET'])
def download(image_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT name, data FROM images WHERE id=?", (image_id,))
    row = c.fetchone()
    conn.close()

    if row:
        filename, image_data = row
        with open(f'{app.config["UPLOAD_FOLDER"]}/{filename}', 'wb') as f:
            f.write(image_data)

        return jsonify({'message': 'Image downloaded successfully'})
    else:
        return jsonify({'message': 'Image not found'})

if __name__ == '__main__':
    create_table()
    app.run()
