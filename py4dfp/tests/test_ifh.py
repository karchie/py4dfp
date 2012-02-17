# emacs: -*- coding: utf-8; mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set fileencoding=utf-8 ft=python sts=4 ts=4 sw=4 et:

import py4dfp.ifh as ifh
import unittest
from pyparsing import ParseException

class TestIFH(unittest.TestCase):
    def test_to_dict(self):
        d = ifh.to_dict('py4dfp/tests/data/test.4dfp.ifh')
        self.assertTrue(ifh.kMagic in d)
        self.assertEqual(4, len(d[ifh.kMatrixSize]))

        self.assertRaises(ParseException, ifh.to_dict, 'py4dfp/tests/data/broken.4dfp.ifh')
        self.assertRaises(IOError, ifh.to_dict, 'no.such.ifh')
        

if __name__ == '__main__':
    unittest.main()
