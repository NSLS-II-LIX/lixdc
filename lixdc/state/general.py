class State():
    def __init__(self):
        self.user = None
        self.project = None
        self.beamline_id = "LIX"
        self.login_timestamp = None

    def __str__(self):
        return "User: {}, Project: {}, Beamline: {}, Login Timestamp: {}".format(self.user, self.project, self.beamline_id, self.login_timestamp)

    def get_default_fields(self):
        return {'owner': self.user, 'project': self.project, 'beamline_id':
                self.beamline_id}
