import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

import unittest
from Testing import ZopeTestCase
import CPSLocalFSTestCase
from os.path import exists, isdir
from zLOG import LOG, DEBUG, INFO

class TestCPSLocalFS(CPSLocalFSTestCase.CPSLocalFSTestCase):

    def afterSetUp(self):
        self.login('root')

    def beforeTearDown(self):
        self.logout()

    def testVersionLocalFS(self):
        required_version ="LocalFS-1-2-andreas"
        version_path = str(ZOPE_HOME) + "/Products/LocalFS/version.txt"
        version_file= open(version_path)
        installed_version = version_file.readline()
        version_file.close()
        self.assert_(required_version==installed_version)
        
       
    def testReachConfigFile(self):
        config_file_path = str(ZOPE_HOME) +"/var/localfs_dirs.txt"
        self.assert_(exists(config_file_path))


        


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestCPSLocalFS))
    return suite
