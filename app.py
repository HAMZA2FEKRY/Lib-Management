from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from src.routes.books import books_bp

app = Flask(__name__)

app.register_blueprint(books_bp)

SWAGGER_URL = '/api-docs'  
API_URL = '/swagger.yaml'  
My_swagger_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "Library Management API"}
)
app.register_blueprint(My_swagger_blueprint, url_prefix=SWAGGER_URL)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)
