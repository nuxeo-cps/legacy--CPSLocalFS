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

    def test_Access_CPSLocalFS_ok(self):
        """ Make sure a file can be acceded """
        path = ZOPE_HOME + "/Products/CPSLocalFS/doc"
        title = "Test CPSLocalFS OK"
        kw = {}
        datamodel = {}
        datamodel['basepath'] = path
        datamodel['Title'] = title
        kw['datamodel'] = datamodel
        cpslocalfs = CPSLocalFS("sqfmdfj",**kw)
        files = cpslocalfs.fileValues()
        # Check if file 'install.txt' can be acceded
        found = 0
        for file in files:
            if file.url == "install.txt":
                found = 1
        self.assert_(found)

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestCPSLocalFS))
    return suite
