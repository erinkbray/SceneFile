# {folder_path}/{descriptor}_{task}_{v###}.{ext}

from pathlib import Path
import re


class SceneFile(object):
    """An abstract representation of a Scene file."""

    def __init__(self, path):
        self._init_from_path(path)
        #the regex here selects for "\" (triple escaped), "/", ".", and "_", and splits the string on all of them
        self.folder_path, self.descriptor, self.task, self.version, self.extension = re.split("[\\\\/\._]", path)
        self.version = int(self.version)

    #this method assembles the file name and returns it
    @property
    def filename(self):
        pattern = "{descriptor}_{task}_v{ver:03d}{ext}"
        return pattern.format(descriptor=self.descriptor,
                              task=self.task,
                              ver=self.version,
                              ext=self.extension)

    #this method uses pathlib to return an OS-specific filepath
    @property
    def path(self):
        return self.folder_path / self.filename

    def _init_from_path(self, path):
        path = Path(path)
        self.folder_path = path.parent


scene_file = SceneFile("D:\\tank_model_001.ma")
print(scene_file.folder_path)
print(scene_file.descriptor)
print(scene_file.task)
print(scene_file.version)
print(scene_file.extension)
