# {folder_path}/{descriptor}_{task}_{v###}.{ext}

import logging
from pymel.core.system import Path
import pymel.core as pmc

log = logging.getLogger(__name__)


class SceneFile(object):
    # An abstract representation of a Scene file.

    def __init__(self, path=None):
        print("init")
        self.folder_path = Path()
        self.descriptor = 'main'
        self.task = None
        self.version = 1
        self.extension = '.ma'
        scene = pmc.system.sceneName()
        if not path and scene:
            path = scene
        if not path and not scene:
            log.warning("Unable to initialize SceneFile object"
                        "from a new scene. Please specify a path")
            return
        self._init_from_path(path)

    # this method assembles the file name and returns it
    @property
    def filename(self):
        print("filename")
        pattern = "{descriptor}_{task}_v{ver:03d}{ext}"
        return pattern.format(descriptor=self.descriptor,
                              task=self.task,
                              ver=self.version,
                              ext=self.extension)

    # this method uses pathlib to return an OS-specific filepath
    @property
    def path(self):
        print("path")
        return self.folder_path / self.filename

    def _init_from_path(self, path):
        path = Path(path)
        self.folder_path = path.parent
        self.ext = path.ext
        self.descriptor, self.task, ver = path.name.stripext().split('_')
        self.version = int(ver.split("v")[-1])

    def next_avail_ver(self):
        print("next available version")
        """Returns the next available version in the folder"""
        pattern = "{descriptor}_task_v*{ext}".format(
            descriptor=self.descriptor, task=self.task, ext=self.extension)
        print("past pattern")
        matching_scenefiles = []
        for file_ in self.folder_path.files():
            if file_.name.fnmatch(pattern):
                matching_scenefiles.append(file_)
                print("if yes")
        if not matching_scenefiles:
            print("if no")
            return 1
        matching_scenefiles.sort(reverse=True)
        latest_scenefile = matching_scenefiles[0]
        latest_scenefile = latest_scenefile.name.stripext()
        latest_ver_num = int(latest_scenefile.split("-v")[-1])
        return latest_ver_num + 1

    def save(self):
        """Saves the Scene File

        Returns:
            Path: The path to the scene file if successful
            """
        try:
            return pmc.system.saveAs(self.path)
        except RuntimeError as err:
            log.warning("Missing Directories. Creating them now.")
            self.folder_path.makedirs_p()
            return pmc.system.saveAs(self.path)

    def increment_save(self):
        """Increments the version and saves the scenefile.

        If the existing version of a file already exists, it should increment from the largest
        version number present in the folder

        Returns:
            Path: The path to the filescene if successful
        """
        self.version = self.next_avail_ver()
        self.save()


# test case
scene_file = SceneFile("C:\\tank_model_001.ma")
scene_file.increment_save()
scene_file.increment_save()
