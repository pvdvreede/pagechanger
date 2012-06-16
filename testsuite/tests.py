#! /usr/bin/env python

import unittest
import sys
import os
path1 = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(path1)
import pagechanger


class PageChangerTests(unittest.TestCase):
    def setUp(self):
        self.config = {
                'exceptions' : ['testfile1.txt'],
                'name': 'text files',
                'mask': '*.txt',
                'remove': [
                    'text',
                    'colou*r'
                    ]
                }
        self.test_path = os.path.join(os.path.dirname(__file__), 'files')

    def test_exceptions(self):
        self.assertTrue(pagechanger.is_exception('testfile1.txt', self.config))
        self.assertFalse(pagechanger.is_exception('testfile2.txt', self.config))

    def test_get_files_recursive(self):
        actual_files = pagechanger.get_files(self.test_path, self.config['mask'], True, self.config)
        self.assertEqual(2, len(actual_files))

    def test_get_files(self):
        actual_files = pagechanger.get_files(self.test_path, self.config['mask'], False, self.config)
        self.assertEqual(1, len(actual_files))
        
    def test_file_mask(self):
        actual_files = pagechanger.get_files(self.test_path, '*.nothing', True, self.config)
        self.assertEqual(0, len(actual_files))
        actual_files = pagechanger.get_files(self.test_path, '*.doc', True, self.config)
        self.assertEqual(1, len(actual_files))

if __name__ == '__main__':
    unittest.main()
