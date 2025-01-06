from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import boto3  # AWS SDK for Python
from botocore.exceptions import NoCredentialsError

app = Flask(__name__)

# AWS S3 Configuration
S3_BUCKET = "your-s3-bucket-name"
S3_REGION = "your-region"
S3_ACCESS_KEY = "your-access-key"
S3_SECRET_KEY = "your-secret-key"

s3_client = boto3.client('s3',
                         aws_access_key_id=S3_ACCESS_KEY,
                         aws_secret_access_key=S3_SECRET_KEY,
                         region_name=S3_REGION)

ALLOWED_EXTENSIONS = {'pdf', 'docx', 'mp4', 'mov', 'avi'}

# Mock database for study materials
study_materials = []

# Helper function to find material by ID
def find_material(material_id):
    return next((material for material in study_materials if material['id'] == material_id), None)

# Helper function to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Helper function to validate metadata
def validate_metadata(data):
    errors = []
    if not data.get('title'):
        errors.append("Title is required.")
    if not data.get('description'):
        errors.append("Description is required.")
    if not data.get('category'):
        errors.append("Category is required.")
    return errors

# Helper function to upload file to S3
def upload_to_s3(file: FileStorage, filename: str):
    try:
        s3_client.upload_fileobj(
            file,
            S3_BUCKET,
            filename,
            ExtraArgs={"ACL": "public-read"}
        )
        file_url = f"https://{S3_BUCKET}.s3.{S3_REGION}.amazonaws.com/{filename}"
        return file_url
    except NoCredentialsError:
        raise Exception("AWS credentials not available")

# Endpoint: Upload study materials
@app.route('/api/materials', methods=['POST'])
def upload_material():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': f'File type not allowed. Allowed types: {ALLOWED_EXTENSIONS}'}), 400

    filename = secure_filename(file.filename)

    data = request.form
    validation_errors = validate_metadata(data)
    if validation_errors:
        return jsonify({'errors': validation_errors}), 400

    try:
        file_url = upload_to_s3(file, filename)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    new_material = {
        'id': len(study_materials) + 1,  # Simple ID generator
        'title': data.get('title'),
        'description': data.get('description'),
        'category': data.get('category'),
        'file_url': file_url,  # URL to the S3 file
        'status': 'pending_review'  # Default status
    }
    study_materials.append(new_material)
    return jsonify({'message': 'Material uploaded successfully', 'material': new_material}), 201

# Endpoint: Edit study material
@app.route('/api/materials/<int:material_id>', methods=['PUT'])
def edit_material(material_id):
    material = find_material(material_id)
    if not material:
        return jsonify({'error': 'Material not found'}), 404

    data = request.json
    validation_errors = validate_metadata(data)
    if validation_errors:
        return jsonify({'errors': validation_errors}), 400

    material.update({
        'title': data.get('title', material['title']),
        'description': data.get('description', material['description']),
        'category': data.get('category', material['category']),
        'file_url': data.get('file_url', material['file_url'])
    })
    return jsonify({'message': 'Material updated successfully', 'material': material})

# Endpoint: Delete study material
@app.route('/api/materials/<int:material_id>', methods=['DELETE'])
def delete_material(material_id):
    material = find_material(material_id)
    if not material:
        return jsonify({'error': 'Material not found'}), 404

    # Optional: Delete file from S3 (if needed)
    file_key = material['file_url'].split('/')[-1]
    try:
        s3_client.delete_object(Bucket=S3_BUCKET, Key=file_key)
    except Exception as e:
        return jsonify({'error': f"Error deleting file from S3: {str(e)}"}), 500

    study_materials.remove(material)
    return jsonify({'message': 'Material deleted successfully'})

# Endpoint: Retrieve all study materials
@app.route('/api/materials', methods=['GET'])
def get_all_materials():
    return jsonify({'materials': study_materials})

# Endpoint: Retrieve study materials by category
@app.route('/api/materials/category/<string:category>', methods=['GET'])
def get_materials_by_category(category):
    filtered_materials = [material for material in study_materials if material['category'].lower() == category.lower()]
    return jsonify({'materials': filtered_materials})

# Endpoint: Retrieve a single study material
@app.route('/api/materials/<int:material_id>', methods=['GET'])
def get_material(material_id):
    material = find_material(material_id)
    if not material:
        return jsonify({'error': 'Material not found'}), 404

    return jsonify({'material': material})

# Endpoint: Approve a study material
@app.route('/api/materials/<int:material_id>/approve', methods=['PATCH'])
def approve_material(material_id):
    material = find_material(material_id)
    if not material:
        return jsonify({'error': 'Material not found'}), 404

    if material['status'] != 'pending_review':
        return jsonify({'error': 'Material is not pending review'}), 400

    material['status'] = 'approved'
    return jsonify({'message': 'Material approved successfully', 'material': material})

# Endpoint: Reject a study material
@app.route('/api/materials/<int:material_id>/reject', methods=['PATCH'])
def reject_material(material_id):
    material = find_material(material_id)
    if not material:
        return jsonify({'error': 'Material not found'}), 404

    if material['status'] != 'pending_review':
        return jsonify({'error': 'Material is not pending review'}), 400

    material['status'] = 'rejected'
    return jsonify({'message': 'Material rejected successfully', 'material': material})

if __name__ == '__main__':
    app.run(debug=True)
