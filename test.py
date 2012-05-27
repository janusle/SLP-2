#!/usr/bin/env python2.6
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

        '''
        result = writelines("testData/test_permission", ["aaaa"])
        self.assertEqual(result,0)
        '''

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


    def test_classInfo(self):
        result = self.e.classInfo("class9")
        sample = ("a0", "Wed", "3.5.11", "Hi", [] )
        self.assertEqual( result, sample )

        result = self.e.classInfo("class3")
        sample = ("a1", "Tue", "3.3.3", "Janus", ["s1","s2","s3"] )
        self.assertEqual( result, sample )


        result = self.e.classInfo("class4")
        sample = ("a2", "Mon", "3.5555.10", "Null", ["s0","s1","s2","s4","s5"] )
        self.assertEqual( result, sample )

        self.assertRaises(KeyError, self.e.classInfo, "nosuchclass")


    def test_checkStudent(self):

        # without specifying subject code
        result = self.e.checkStudent("s2")
        sample = [ "class3", "class4" ]
        self.assertEqual(len(result), len(sample))
        for klass in sample:
            self.assertTrue( klass in result )

        result = self.e.checkStudent("s0")
        sample = [ "class4" ]
        self.assertEqual(len(result), len(sample))
        for klass in sample:
            self.assertTrue( klass in result )
        # test student id which is not existed
        result = self.e.checkStudent("s10")
        sample = []
        self.assertEqual( result, sample )

        # with specifying subject code

        result = self.e.checkStudent("s1","a2")
        sample = "class4"
        self.assertEqual( result, sample )

        result = self.e.checkStudent("s2", "a1")
        sample = "class3"
        self.assertEqual( result, sample )

        # test a subject in which student isn't enrolled
        result = self.e.checkStudent("s1","a3")
        self.assertEqual( result, None )

        # test a subject which is not existed
        self.assertRaises(KeyError, self.e.checkStudent, "s1","a77" )


    def test_enrol(self):
        # normal test
        result = self.e.enrol("s1", "class10")
        self.assertEqual( result, 1 )
        result = self.e.checkStudent("s1", "a4")
        self.assertEqual( result, "class10")
        self.e = Enrol("testData")
        result = self.e.checkStudent("s1","a4")
        self.assertEqual( result, "class10")

        # test changing class
        result = self.e.enrol("s1", "class6")
        self.assertEqual( result, 1)
        result = self.e.checkStudent("s1","a4")
        self.assertEqual( result, "class6")
        self.e = Enrol("testData")
        result = self.e.checkStudent("s1","a4")
        self.assertEqual( result, "class6")

        # test over capacity
        result = self.e.enrol("s0", "class6")
        self.assertEqual( result, None)

        # test new student
        result = self.e.enrol("s100", "class10")
        self.assertEqual( result, 1 )
        result = self.e.checkStudent("s100", "a4")
        self.assertEqual( result, "class10" )
        self.e = Enrol("testData")
        result = self.e.checkStudent("s100","a4")
        self.assertEqual( result, "class10")

        # test class which is not existed
        self.assertRaises(KeyError, self.e.enrol, "s0", "NoSuchClass")

    def tearDown(self):

        # delete testing data
        import os
        try:
          os.remove("testData/class6.roll")
          os.remove("testData/class10.roll")
        except:
          pass

if __name__ == '__main__':

    from enrol import Enrol
    unittest.main()

