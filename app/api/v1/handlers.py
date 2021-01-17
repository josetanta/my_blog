from . import v1


@v1.app_errorhandler(404)
def get_404(e):
    return e, 404


@v1.app_errorhandler(403)
def get_403(e):
    return e, 403


@v1.app_errorhandler(405)
def get_405(e):
    return e, 405


@v1.app_errorhandler(500)
def get_500(e):
    return e, 500
