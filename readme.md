# Dropbox-Like Service

This project is a simplified Dropbox-like service where users can upload, retrieve, delete, and update their files through a set of RESTful APIs.

## Features

- Upload files
- Retrieve specific files
- Update existing files
- Delete specific files
- List all available files

## Technologies

- Backend: Python, Flask
- Database: MySQL
- Storage: Local File System
- Containerization: Docker

## Setup and Installation

(Explain how to set up the project, install dependencies, and get the server running)

## API Endpoints

1.Upload File API
POST /files/upload
curl -X POST -F "file=@<file_path>" http://localhost:5000/files/upload

2.Read File API
Endpoint: GET /files/{fileId}
curl -o <output_file> http://localhost:5000/files/<file_id>

3.Update File API
To update the file's binary data:
curl -X PUT -F "file=@<new_file_path>" http://localhost:5000/files/<file_id>

To update the file's metadata (e.g., file name):
curl -X PUT -H "Content-Type: application/json" -d "{\"new_file_name\": \"<new_name>\"}" http://localhost:5000/files/<file_id>



4. Delete File API
Endpoint: DELETE /files/{fileId}
curl -X DELETE http://localhost:5000/files/<file_id>


5. List Files API
Endpoint: GET /files
curl http://localhost:5000/files

## License

Free to use