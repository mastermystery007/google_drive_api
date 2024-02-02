from flask import Flask, request, send_file, jsonify
from werkzeug.utils import secure_filename
from models import db, FileMetadata
from config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

# make an uploads folder
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Implement the APIs (upload, get, update, delete, list) here as shown in the previous message
@app.route('/files/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify(error="No file part"), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify(error="No selected file"), 400
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        # Save metadata to the database
        file_metadata = FileMetadata(
            file_name=filename,
            size=os.path.getsize(os.path.join(app.config['UPLOAD_FOLDER'], filename)),
            file_type=file.content_type
        )
        db.session.add(file_metadata)
        db.session.commit()
        
        return jsonify(id=file_metadata.id), 200

@app.route('/files/<int:file_id>', methods=['GET'])
def get_file(file_id):
    file_metadata = FileMetadata.query.filter_by(id=file_id).first()
    if file_metadata:
        return send_file(os.path.join(app.config['UPLOAD_FOLDER'], file_metadata.file_name), as_attachment=True)
    else:
        return jsonify(error="File not found"), 404


@app.route('/files/<int:file_id>', methods=['PUT'])
def update_file(file_id):
    # Fetch the existing file metadata from the database
    file_metadata = FileMetadata.query.get(file_id)
    if not file_metadata:
        return jsonify(error="File not found"), 404
    
    # Update the file if a new file is provided
    file = request.files.get('file')
    if file:
        # Remove the old file
        old_file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_metadata.file_name)
        if os.path.exists(old_file_path):
            os.remove(old_file_path)
        
        # Save the new file
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        # Update file metadata
        file_metadata.file_name = filename
        file_metadata.size = os.path.getsize(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        file_metadata.file_type = file.content_type
    
    # Update other metadata if provided in JSON format
    if request.content_type == 'application/json':
        data = request.json
        if 'new_file_name' in data:
            file_metadata.file_name = data['new_file_name']
        # Add more metadata updates here as needed

    # Commit changes to the database
    db.session.commit()

    # Return the updated metadata
    return jsonify({
        'id': file_metadata.id,
        'file_name': file_metadata.file_name,
        'created_at': file_metadata.created_at,
        'size': file_metadata.size,
        'file_type': file_metadata.file_type
    }), 200




@app.route('/files/<int:file_id>', methods=['DELETE'])
def delete_file(file_id):
    file_metadata = FileMetadata.query.filter_by(id=file_id).first()
    if file_metadata:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file_metadata.file_name))
        db.session.delete(file_metadata)
        db.session.commit()
        return jsonify(success="File deleted"), 200
    else:
        return jsonify(error="File not found"), 404


@app.route('/files', methods=['GET'])
def list_files():
    files = FileMetadata.query.all()
    return jsonify([{
        'id': file.id,
        'file_name': file.file_name,
        'created_at': file.created_at,
        'size': file.size,
        'file_type': file.file_type
    } for file in files]), 200


if __name__ == '__main__':
    app.run(debug=True)
