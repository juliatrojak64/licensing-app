from flask import Blueprint, jsonify
from app.database import mysql

api_bp = Blueprint('api', __name__)

@api_bp.route('/stages-overview/<int:user_id>', methods=['GET'])
def get_user_stages(user_id):
    try:
        cursor = mysql.connection.cursor()
        
        # Zapytanie do bazy danych
        query = """
        SELECT 
            ModuleName, CompletionStatus, CompletionDate 
        FROM Progress 
        WHERE UserID = %s;
        """
        cursor.execute(query, (user_id,))
        progress = cursor.fetchall()

        # Przygotowanie odpowiedzi JSON
        stages = []
        for row in progress:
            stages.append({
                "module_name": row[0],
                "completion_status": row[1],
                "completion_date": str(row[2]) if row[2] else None
            })

        cursor.close()
        return jsonify({
            "user_id": user_id,
            "stages": stages
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
