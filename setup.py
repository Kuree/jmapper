from setuptools import setup
import subprocess
import os
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
from distutils.command.build import build
import shutil


MAPPER_PATH = "CGRAMapper"
COREIR_PATH = "coreir"


class CoreIRExtension(Extension):
    def __init__(self, name, sourcedir=''):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)


class CoreIRBuild(build_ext):
    def run(self):
        if not os.path.isdir(MAPPER_PATH):
            subprocess.check_call(["git", "submodule", "update", "--init",
                                   "--recursive"])

        build_dir = os.path.join(COREIR_PATH, "build")
        subprocess.check_call(["cmake", "-DSTATIC=ON", ".."], cwd=build_dir)

        subprocess.check_call(["make", "-C", build_dir, "-j4"])
        os.environ["LIBRARY_PATH"] = os.path.abspath(os.path.join(COREIR_PATH, "lib"))
        subprocess.check_call(["make", "-C", MAPPER_PATH, "-j4"])

        # we only have one extension
        assert len(self.extensions) == 1
        ext = self.extensions[0]
        extdir = \
            os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))
        extdir = os.path.join(extdir, "jmapper")
        if not os.path.isdir(extdir):
            os.mkdir(extdir)

        # copy binary over
        filename = os.path.join(MAPPER_PATH, "bin", "cgra-mapper")
        shutil.copy(filename, extdir)
        filename = os.path.join(MAPPER_PATH, "lib", "libcoreir-cgralib.so")
        shutil.copy(filename, extdir)

setup(
    name='jmapper',
    packages=[
        "jmapper"
    ],
    version='0.1.14',
    author='Keyi Zhang',
    author_email='keyi@stanford.edu',
    description='Mapper for Jade CGRA',
    url="https://github.com/Kuree/jmapper",
    ext_modules=[CoreIRExtension('jmapper')],
    scripts=["bin/mapper"],
    cmdclass=dict(build_ext=CoreIRBuild),
)
