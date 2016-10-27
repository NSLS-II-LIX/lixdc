class State():
    def __init__(self):
        self.user = None
        self.proposal_id = None
        self.run_id = None
        self.beamline_id = "LIX"
        self.login_timestamp = None
        self.configs = None

    def __str__(self):
        return "User: {}, Proposal: {}, Beamline: {}, Login Timestamp: {}".format(self.user, self.proposal_id, self.beamline_id, self.login_timestamp)

    def get_default_fields(self):
        return {'owner': self.user, 'proposal_id': self.proposal_id, 'beamline_id':
                self.beamline_id, 'run_id': self.run_id}

    def get_user_path(self):
        return "{}/{}/{}/".format(self.configs['base_path'], self.proposal_id,
                                 self.run_id)
