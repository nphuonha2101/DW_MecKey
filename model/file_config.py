class FileConfig:
    def __init__(self, id, feed_name, source_url, folder_data_path, feed_key, to_staging_proc_name, transform_proc_name, load_proc_name, num_pages):
        self.id = id
        self.feed_name = feed_name
        self.source_url = source_url
        self.folder_data_path = folder_data_path
        self.feed_key = feed_key
        self.to_staging_proc_name = to_staging_proc_name
        self.transform_proc_name = transform_proc_name
        self.load_proc_name = load_proc_name
        self.num_pages = num_pages

    @classmethod
    def from_db(cls, result):
        return cls(*result)

