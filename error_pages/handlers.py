from flask import Blueprint, render_template

error_pages_blueprint = Blueprint('error_pages', __name__)

@error_pages_blueprint.errorhandler(404)
def page_error_not_found(e):
    return render_template('error/404.html'), 404
