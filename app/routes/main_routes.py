from app.routes.bank_csv_routes import bank_api
from app.routes.category_routes import category_api
from app.routes.user_routes import user_api
from app.routes.file_routes import upload_api


def register_all(app):
    app.register_blueprint(user_api, url_prefix='/api/users')
    app.register_blueprint(category_api, url_prefix='/api/categories')
    app.register_blueprint(bank_api, url_prefix='/api/banks')
    app.register_blueprint(upload_api, url_prefix='/api/upload')
