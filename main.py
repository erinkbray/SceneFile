#{folder_path}/{descriptor}_{task}_{v###}.{ext}

class SceneFile(object):
    """An abstract representation of a Scene file."""
    def __init__(self, folder_path, descriptor, task, ver, ext):
        self.folder_path = folder_path
        self.descriptor = descriptor
        self.task = task
        self.version = ver
        self.extension = ext

    @property
    def filename(self):
        pattern = "{descriptor}_{task}_v{ver:03d}{ext}"
        return pattern.format(descriptor=self.descriptor,
                              task=self.task,
                              ver=self.version,
                              ext=self.extension)


scene_file = SceneFile("D:\\", "tank", "model", 1, ".ma")
print(scene_file.filename)

