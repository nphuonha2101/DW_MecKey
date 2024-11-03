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

    def __str__(self):
        return (
            f"FileLog(id={self.id}, id_config={self.id_config}, status='{self.status}', "
            f"time='{self.time}', file_path='{self.file_path}', description={self.description})"
        )