import os
import glob
import pytest
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/testing_modules/'))

from test_msh import mesh_file_test
from test_geo import geo_files_test

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../plugins/mesh_netcdf/'))

from modular_meshing import Modular_meshing


pwd = os.path.dirname(os.path.realpath(__file__))
test = pwd+"/output"
data = pwd+"/support"
rtponedomain = data+"/rtopo_shape_DN__2.shp"
rtpmultdomain = data+"/ID0Layer.shp"

idfile = data+"/a_idLayer.shp"


# used too pass arguments to the test function
def pytest_generate_tests(metafunc):
    # called once per each test function
    for funcargs in metafunc.cls.params[metafunc.function.__name__]:
        # schedule a new test function run with applied **funcargs
        metafunc.addcall(funcargs=funcargs)


class TestClass:
    """ Runs various tests on files """

    #parameters to the test function
    params = {

    	'test_annulus_bn_geo' : [dict(curr_file=x) for x in glob.glob(pwd +"/output/BY/*.geo")],
        'test_annulus_bn_msh': [dict(curr_file=x) for x in glob.glob(pwd +"/output/BY/*.msh")],
    }


    def test_annulus_bn_geo(self, curr_file):

		if not os.path.exists("mkdir "+test +"/BY"):
		    os.makedirs("mkdir "+test +"/BY")

		Modular_meshing("-l BY -g "+test+"/BY/testfileBY_0."+rtponedomain+" --mesh")
		Modular_meshing("-l BY -g "+test+"/BY/testfileBY_1.geo --id "+idfile+" "+rtponedomain+" --mesh")
		Modular_meshing("-l BY -g "+test+"/BY/testfileBY_2.geo "+rtpmultdomain+" --mesh")
		Modular_meshing("-l BY -g "+test+"/BY/testfileBY_3.geo --id "+idfile+" "+rtpmultdomain+"  --mesh")

		assert geo_files_test(curr_file),"%s does not match the model answer" % (ntpath.basename(a).rstrip())



    # Tests whether nodes of the file being are similar to the nodes in the
    # model answer. Throws an AssertionError if the files don't match
    def test_annulus_bn_msh(self, curr_file):

        assert mesh_file_test(curr_file),"%s does not match the model answer" % (ntpath.basename(curr_file).rstrip())
