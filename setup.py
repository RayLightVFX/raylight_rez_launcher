# coding=utf-8

import os
from setuptools import setup, find_packages
from setuptools.command.build_py import build_py
import subprocess


class CustomBuildPy(build_py):
    def run(self):
        build_py.run(self)
        self.run_pyinstaller()

    def run_pyinstaller(self):
        cmd = [
            'pyinstaller',
            '--name=RezLauncher',
            '--add-data=resources:resources',
            r'--add-data=C:\Users\lizhifeng\PycharmProjects\raylight_rez_launcher\venv39\Lib\site-packages\rez:rez',
            r'--add-data=C:\Users\lizhifeng\PycharmProjects\raylight_rez_launcher\venv39\Lib\site-packages\rezplugins:rezplugins',
            '--add-data=rez_repo.json:.',
            r'--icon=C:\Users\lizhifeng\PycharmProjects\raylight_rez_launcher\resources\icon\logo.ico',
            '--windowed',
            '--distpath=build/rez',
            '--clean',
            '-y',
            'rez_launcher.py'
        ]
        print(' '.join(cmd))
        subprocess.check_call(cmd)


setup(
    name='RezLauncher',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pyinstaller',
        # 添加其他依赖项
    ],
    entry_points={
        'console_scripts': [
            'rez_launcher=rez_launcher:main',
        ],
    },
    cmdclass={'build_exe': CustomBuildPy},
    data_files=[
        ('', ['rez_repo.json']),
    ],
    package_data={
        '': ['resources/*', 'resources/icon/*'],
    },
    author='lixinshan',
    author_email='xyxiaozhao@gmail.com',
    description='A Rez launcher application',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
