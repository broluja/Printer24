from src.controllers import users, organisations


class Routes:
    def __init__(self, app):
        self.app = app
        self.dispatch(app)

    def dispatch(self, app):
        app.include_router(users.router)
        app.include_router(organisations.router)
        return self
