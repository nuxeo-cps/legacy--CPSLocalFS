import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

import unittest
from Testing import ZopeTestCase
import CPSLocalFSTestCase
from os.path import exists, isdir
from Products.CPSLocalFS.CPSLocalFS import CPSLocalFS


class TestCPSLocalFS(CPSLocalFSTestCase.CPSLocalFSTestCase):

    def afterSetUp(self):
        self.login('root')

    def beforeTearDown(self):
        self.logout()

    def testAccessCPSLocalfsOK(self):
        """ Make sure a file can be acceded """
        path = ZOPE_HOME + "/Products/CPSLocalFS/tests"
        title = "Test CPSLocalFS OK"
        datamodel = {'basepath': path, 'Title': title}
        cpslocalfs = CPSLocalFS("idTestCPSLocalFS", datamodel=datamodel)
        files = cpslocalfs.fileValues()
        # Check if file 'install.txt' can be acceded
        self.assert_("tests.txt" in [file.url for file in files])
        for file in files :
            if file.url == "tests.txt":
                self.assertEqual(file.id, "tests.txt")
                self.assertEqual(file.icon, "misc_/LocalFS/text.gif")
                self.assertEqual(file.type, "text/plain")
        local_file = cpslocalfs["tests.txt"]
        self.assertEqual(local_file.data[:9],"Test file")
        
def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestCPSLocalFS))
    return suite
