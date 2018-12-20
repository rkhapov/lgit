import unittest
from core.tools.differ import *


def get_differ():
    return Differ()


class DifferUnitTests(unittest.TestCase):
    def test_get_diff__from_empty_string_to_non_empty__should_return_right_list_of_insertions(self):
        differ = get_differ()
        expected = [Insert(0, 'm'), Insert(1, 'y'), Insert(2, '_'), Insert(3, 's'), Insert(4, 't'), Insert(5, 'r')]

        sut = differ.get_diff('', 'my_str')

        self.assertSequenceEqual(expected, sut)

    def test_get_diff__from_non_empty_string_to_empty_string__should_return_right_list_of_deletions(self):
        differ = get_differ()
        expected = [Delete(0, 'm'), Delete(0, 'y'), Delete(0, '_'), Delete(0, 's'), Delete(0, 't'), Delete(0, 'r')]

        sut = differ.get_diff('my_str', '')

        self.assertSequenceEqual(expected, sut)

    def test_get_diff__one_symbol_strings__should_return_list_with_one_replace_action(self):
        differ = get_differ()
        expected = [Replace(0, 'a', 'b')]

        sut = differ.get_diff('a', 'b')

        self.assertListEqual(sut, expected)

    def test_get_diff__two_symbols_and_one_not_equals__should_return_right_actions_list(self):
        differ = get_differ()
        expected = [Replace(1, 'a', 'b')]

        sut = differ.get_diff('aa', 'ab')

        self.assertListEqual(sut, expected)

    def test_get_diff__two_different_symbols__should_return_right_actions_list(self):
        differ = get_differ()
        expected = [Replace(0, 'a', 'b'), Replace(1, 'c', 'd')]

        sut = differ.get_diff('ac', 'bd')

        self.assertListEqual(sut, expected)

    def test_get_diff__eqivalent_strings__should_return_list_with_empty_actions(self):
        differ = get_differ()
        expected = []

        sut = differ.get_diff('abcdefghjk', 'abcdefghjk')

        self.assertListEqual(sut, expected)

    def test_get_diff__string_with_one_symbol_to_replace__should_return_right_list(self):
        differ = get_differ()
        expected = [Replace(2, 'a', 'b')]

        sut = differ.get_diff('mbakk', 'mbbkk')

        self.assertListEqual(sut, expected)

    def test_get_diff__deletion_case__should_return_right_list(self):
        differ = get_differ()
        expected = [Delete(0, 'a'), Delete(0, 'c'), Delete(0, 'd')]

        sut = differ.get_diff('acdbb', 'bb')

        self.assertListEqual(sut, expected)

    def test_get_diff__complex_case__should_return_right_list(self):
        differ = get_differ()
        expected = [Replace(0, 'm', 'p'), Replace(2, 'm', 'p'), Delete(8, 'a'), Replace(9, 'r', 'o'),
                    Replace(10, 'a', 'k'), Replace(11, 'm', 'n'), Replace(12, 'u', 'o')]

        sut = differ.get_diff('mama mila ramu', 'papa mil okno')

        self.assertListEqual(sut, expected)

    def test_get_diff__deletion_suffix__should_return_right_list(self):
        differ = get_differ()
        expected = [Delete(3, 'a'), Delete(3, 'b')]

        sut = differ.get_diff('cccab', 'ccc')

        self.assertListEqual(sut, expected)

    def test_get_diff__insertion_needed__should_return_right_list(self):
        differ = get_differ()
        expected = [Insert(5, 'f')]

        sut = differ.get_diff('aaaaaaa', 'aaaaafaa')

        self.assertListEqual(sut, expected)

    def test_get_diff__one_deletion_needed__should_return_right_list(self):
        differ = get_differ()
        expected = [Delete(5, 'f')]

        sut = differ.get_diff('aaaaafaa', 'aaaaaaa')

        self.assertListEqual(sut, expected)

    def test_get_diff__works_correctly_with_lists_of_strings(self):
        text1 = ['mama', 'mila', 'ramu', 'lol']
        text2 = ['papa', 'mila', 'trash', 'okno', 'lol']
        differ = get_differ()
        expected = [Replace(0, 'mama', 'papa'), Insert(2, 'trash'), Replace(3, 'ramu', 'okno')]

        sut = differ.get_diff(text1, text2)

        self.assertListEqual(sut, expected)

    def test_get_diff__on_text_and_need_to_only_delete__should_return_right_list_of_actions(self):
        text1 = ['aaa', 'bbbb', 'cccc']
        text2 = ['aaa']
        differ = get_differ()
        expected = [Delete(1, 'bbbb'), Delete(1, 'cccc')]

        sut = differ.get_diff(text1, text2)

        self.assertListEqual(sut, expected)
