from gaesessions import SessionMiddleware

def webapp_add_wsgi_middleware(app):
    app = SessionMiddleware(app, cookie_key="sssssssssssssssssssssssssssssseeee")
    return app