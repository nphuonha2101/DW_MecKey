class FileConfig:
    def __init__(self, id, feed_name, source_url, file_path, feed_key, status, to_staging_proc_name, transform_proc_name, load_proc_name):
        self.id = id
        self.feed_name = feed_name
        self.source_url = source_url
        self.file_path = file_path
        self.feed_key = feed_key
        self.status = status
        self.to_staging_proc_name = to_staging_proc_name
        self.transform_proc_name = transform_proc_name
        self.load_proc_name = load_proc_name


