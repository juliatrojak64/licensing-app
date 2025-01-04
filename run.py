from flask import Flask
from app.routes import api_bp  # Importujemy blueprint z endpointami
from app.database import init_app  # Funkcja do inicjalizacji bazy danych

def create_app():
    app = Flask(__name__)

    # Konfiguracja bazy danych
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'your_password'
    app.config['MYSQL_DB'] = 'DriversLicenseSystem'

    # Inicjalizacja bazy danych
    init_app(app)

    # Rejestracja blueprintów
    app.register_blueprint(api_bp, url_prefix='/api')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
