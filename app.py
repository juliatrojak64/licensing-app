from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/stages-overview', methods=['GET'])
def get_stages_overview():
    # Mocked data
    stages = [
        {"id": 1, "name": "Stage 1", "description": "Enroll in course", "estimated_time": "2 weeks"},
        {"id": 2, "name": "Stage 2", "description": "Theory lessons", "estimated_time": "4 weeks"},
        {"id": 3, "name": "Stage 3", "description": "Practical lessons", "estimated_time": "6 weeks"},
    ]
    return jsonify(stages)

if __name__ == '__main__':
    app.run(debug=True)