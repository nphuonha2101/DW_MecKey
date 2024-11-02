class FileLog:
    def __init__(self, id, id_config, status, time, file_path):
        self.id = id
        self.id_config = id_config
        self.status = status
        self.time = time
        self.file_path = file_path

    @classmethod
    def from_db(cls, result):
        return cls(
            id=result['id'],
            id_config=result['id_config'],
            status=result['status'],
            time=result['time'],
            file_path=result['file_path']
        )