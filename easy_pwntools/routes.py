from .controllers import main_controllers, menu_controller

def routes_list(app):
    main_controllers.bp.register_blueprint(menu_controller.bp, url_prefix='menu')

    app.register_blueprint(main_controllers.bp)
    app.register_blueprint(menu_controller.bp)
    return app