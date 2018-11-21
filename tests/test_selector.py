import unittest

import core.selector
from core.init import Init


class SelectorUnitTests(unittest.TestCase):
    def test_build_command_by_name_should_return_init(self):
        self.assertIsInstance(core.selector.build_command_by_name('init'), Init)

    
