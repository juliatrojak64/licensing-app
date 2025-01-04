@api_bp.route('/time-estimation/<int:user_id>', methods=['GET'])
def estimate_completion_times(user_id):
    try:
        cursor = mysql.connection.cursor()

        # Zapytanie do tabeli Progress
        query = """
        SELECT 
            ModuleName, CompletionStatus, CompletionDate 
        FROM Progress 
        WHERE UserID = %s;
        """
        cursor.execute(query, (user_id,))
        progress = cursor.fetchall()

        # Obliczenie czasu na podstawie danych historycznych
        stages_with_estimates = []
        for row in progress:
            estimated_time = calculate_estimated_time(row[0])  # Funkcja pomocnicza
            stages_with_estimates.append({
                "module_name": row[0],
                "completion_status": row[1],
                "completion_date": str(row[2]) if row[2] else None,
                "estimated_completion_time": estimated_time
            })

        cursor.close()
        return jsonify({
            "user_id": user_id,
            "stages": stages_with_estimates
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def calculate_estimated_time(module_name):
    # Prosta funkcja obliczająca przewidywany czas ukończenia w dniach
    historical_data = {
        "Traffic Rules": 7,
        "Driving Basics": 14,
        "Advanced Driving": 21,
    }
    return historical_data.get(module_name, "Unknown")
