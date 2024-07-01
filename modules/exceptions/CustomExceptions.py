class ConfigurationFileDoesNotExistsException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class DirectoryDoesNotExistsException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class FileDoesNotExistsException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)