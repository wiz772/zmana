from session.session import Session
from datetime import datetime

class SessionManager():
    def __init__(self):
        self.current_session = None

    def check(self, app_name):
        if self.current_session is None:
            self.current_session = Session(app_name=app_name, started_at=datetime.now())

        if self.current_session.app_name != app_name:
            self.current_session.ended_at = datetime.now()
            # repository.save_session(self.current_session)
            self.current_session = Session(app_name=app_name, started_at=datetime.now())


        