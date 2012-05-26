#!/usr/bin/env python
import unittest

class TestReadlinesFunctions(unittest.TestCase):

    def test_readlines(self):
        from enrol import readlines
        list = readlines("testData/test_readlines")
        self.assertEqual(list , ["aaa","bbb","ccc","ddd","eee"])

        self.assertRaises(IOError,readlines,"NoSuchAFile")


class TestReadtableFunctions(unittest.TestCase):

    def test_readtable(self):
        from enrol import readtable
        list = readtable("testData/test_readtable")
        sample_list = [["aaa","bbb","ccc"],["bbb","ccc","ddd"],\
                ["eee","fff"],["ggg"],["hhh","iii"],["jjj","kkk"],["lll","mmm","nnn","ooo"],\
                ["ppp","qqq","rrr"]]

        self.assertEqual(list , sample_list)
        self.assertRaises(IOError,readtable,"NoSuchAFile")


class TestWritelinesFunctions(unittest.TestCase):

    def test_writelines(self):
        from enrol import writelines,readlines
        test_data = ["aaa","bbb","ccc","ddd","eee"]

        result = writelines("testData/write_data", test_data)
        lines = readlines("testData/write_data" )
        self.assertEqual(test_data, lines)
        self.assertEqual(result,1)

        result = writelines("NoSuchDirectory/write_data", ["aaaa"])
        self.assertEqual(result,0)

        result = writelines("testData/test_permission", ["aaaa"])
        self.assertEqual(result,0)

    def tearDown(self):
        import os
        os.remove("testData/write_data")



class TestEnrolClass(unittest.TestCase):

    def setUp(self):
        self.e = Enrol("testData")

    def test_subjects(self):

        sample_list = [ "a0", "a1", "a2", "a3", "a4" ]
        result = self.e.subjects()

        self.assertEqual( len(sample_list), len(result) )

        for subject in result:
            self.assertTrue( subject in sample_list)


    def test_subjectName(self):
        name = self.e.subjectName("a0")
        self.assertEqual( name, "test0" )

        name = self.e.subjectName("a1")
        self.assertEqual( name, "test1" )

        name = self.e.subjectName("a2")
        self.assertEqual( name, "test2" )

        name = self.e.subjectName("a3")
        self.assertEqual( name, "test3" )

        name = self.e.subjectName("a4")
        self.assertEqual( name, "test4" )

        self.assertRaises(KeyError, self.e.subjectName, "nosuchsubject")


    def test_classes(self):
        classes = self.e.classes("a0")
        sample = [ "class9", "class2" ]
        for klass in classes:
          self.assertTrue( klass in sample)

        classes = self.e.classes("a1")
        sample = ["class3"]
        for klass in classes:
          self.assertTrue( klass in sample)

        classes = self.e.classes("a4")
        sample = ["class6", "class10"]
        for klass in classes:
          self.assertTrue( klass in sample)

        self.assertRaises(KeyError, self.e.classes, "nosuchsubject")


if __name__ == '__main__':

    from enrol import Enrol
    unittest.main()

