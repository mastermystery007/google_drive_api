from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class FileMetadata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    size = db.Column(db.Integer)
    file_type = db.Column(db.String(20))

    def __repr__(self):
        return f'<File {self.file_name}>'
