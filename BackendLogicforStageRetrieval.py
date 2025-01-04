@api_bp.route('/current-stage/<int:user_id>', methods=['GET'])
def get_current_stage(user_id):
    try:
        cursor = mysql.connection.cursor()

        # Zapytanie do tabeli Licenses
        query = """
        SELECT 
            LicenseStage, 
            Status 
        FROM Licenses 
        WHERE UserID = %s;
        """
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()

        # Przygotowanie odpowiedzi
        if result:
            current_stage = {
                "license_stage": result[0],
                "status": result[1]
            }
            cursor.close()
            return jsonify(current_stage), 200
        else:
            cursor.close()
            return jsonify({"error": "User not found or no license data available"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500
