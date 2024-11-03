class FileConfig:
    def __init__(self, id, feed_name, source_url, folder_data_path, feed_key, to_staging_proc_name, transform_proc_name, load_proc_name, num_pages, staging_raw_table_name):
        self.id = id
        self.feed_name = feed_name
        self.source_url = source_url
        self.folder_data_path = folder_data_path
        self.feed_key = feed_key
        self.to_staging_proc_name = to_staging_proc_name
        self.transform_proc_name = transform_proc_name
        self.load_proc_name = load_proc_name
        self.num_pages = num_pages
        self.staging_raw_table_name = staging_raw_table_name

    @classmethod
    def from_db(cls, result):
        return cls(*result)


    def __str__(self):
        return (
            f"FileConfig(id={self.id}, feed_name={self.feed_name}, source_url='{self.source_url}', "
            f"folder_data_path='{self.folder_data_path}', feed_key='{self.feed_key}', to_staging_proc_name={self.to_staging_proc_name}, "
            f"transform_proc_name={self.transform_proc_name}, load_proc_name={self.load_proc_name}, num_pages={self.num_pages})"
        )


