import shape

class Algorithm:
    def __init__(self):
        self.name = 'Name'
        self.set_default_settings()
    
    def change_shape(self, shape, n_times = 1):
        raise NotImplementedError

    def set_default_settings(self):
        raise NotImplementedError

    def get_settings_frame(self): #has to return settings_frame
        raise NotImplementedError