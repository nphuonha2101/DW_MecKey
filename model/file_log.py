class FileLog:
    def __init__(self, id, id_config, status, time, file_path, description):
        self.id = id
        self.id_config = id_config
        self.status = status
        self.time = time
        self.file_path = file_path
        self.description = description

    @classmethod
    def from_db(cls, result):
        return cls(*result)