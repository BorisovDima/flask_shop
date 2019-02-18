from flask import current_app
from flask import render_template


class ErrorHandler:

    @current_app.errorhandler(404)
    def page_not_found(e):
        current_app.logger.error(str(e))
        return (render_template('errors/404.html'), 404)

    @current_app.errorhandler(500)
    def page_not_found(e):
        current_app.logger.error(str(e))
        return (render_template('errors/500.html'), 500)
