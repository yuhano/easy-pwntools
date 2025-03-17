from .controllers import main_controllers

def routes_list(app):
    app.register_blueprint(main_controllers.bp)
    return app