from flask import Flask, request, jsonify

app = Flask(__name__)

# Mock database for study materials
study_materials = []

# Helper function to find material by ID
def find_material(material_id):
    return next((material for material in study_materials if material['id'] == material_id), None)

# Endpoint: Upload study materials
@app.route('/api/materials', methods=['POST'])
def upload_material():
    data = request.json
    new_material = {
        'id': len(study_materials) + 1,  # Simple ID generator
        'title': data.get('title'),
        'description': data.get('description'),
        'category': data.get('category'),
        'file_url': data.get('file_url'),  # URL/path for the uploaded file
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

    study_materials.remove(material)
    return jsonify({'message': 'Material deleted successfully'})

# Endpoint: Retrieve all study materials
@app.route('/api/materials', methods=['GET'])
def get_all_materials():
    return jsonify({'materials': study_materials})

# Endpoint: Retrieve a single study material
@app.route('/api/materials/<int:material_id>', methods=['GET'])
def get_material(material_id):
    material = find_material(material_id)
    if not material:
        return jsonify({'error': 'Material not found'}), 404

    return jsonify({'material': material})

if __name__ == '__main__':
    app.run(debug=True)
