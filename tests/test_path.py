import unittest

from core.repository.path import Path


class PathUnitTests(unittest.TestCase):
    def test_combine__should_return_path_joined_to_root(self):
        path = Path("root/shmoot")

        sut = path.combine("lol")

        self.assertEquals(sut, "root/shmoot/lol")

    def test_path__should_return_root_path(self):
        path = Path("root")

        sut = path.root

        self.assertEquals(sut, "root")

    def test_sub__should_return_path_with_combined_root(self):
        path = Path("root/soos")

        sut = path.sub("subdir")

        self.assertEquals(sut.root, "root/soos/subdir")
