# coding=utf-8

import os
import json
from rez.config import config
from rez.resolved_context import ResolvedContext
from rezplugins import package_repository  # noqa
from rez.vendor.yaml import *  # noqa

config.default_shell = 'cmd'


class RezResolvedContext(ResolvedContext):

    def get_package_version(self):
        pack_version = []
        for pak in self.resolved_packages:
            name = pak.handle.variables.get('name')
            version = pak.handle.variables.get('version')
            pack_version.append({
                "name": name,
                "version": version
            })
        return pack_version

    def get_version(self, dcc_name):
        for pak in self.resolved_packages:
            name = pak.handle.variables.get('name')
            if name in dcc_name:
                return pak.handle.variables.get('version')
            elif dcc_name == 'hiero' and name == 'nuke':
                return pak.handle.variables.get('version')
        return None

    def run(self, command):
        self.execute_shell(command=command).communicate()


def get_rez_package_paths():
    with open(
            os.path.join(os.path.dirname(__file__), 'rez_repo.json'),
            'r', encoding='utf-8'
    ) as f:
        data = json.load(f)
    return data


def rev_command(name, version, file):
    current_cmd = "start "

    if 'nuke' in name:
        nuke_version = version.split('v')[0]
        if name == 'nuke':
            current_cmd += f"nuke{nuke_version}"
        elif name == 'nukex':
            current_cmd += f"nuke{nuke_version} --nukex"
    elif 'hiero' in name:
        nuke_version = version.split('v')[0]
        current_cmd += f"nuke{nuke_version} --hiero"
    elif "katana" in name:
        current_cmd += 'katanabin'
    else:
        current_cmd += name

    if file:
        current_cmd += f' "{file}"'

    return current_cmd


def launcher(env, app_name):
    resolved = RezResolvedContext(
        env, package_paths=[get_rez_package_paths().get('rez_package_paths')]
    )
    version = resolved.get_version(app_name)
    cmd = rev_command(app_name, version, None)
    resolved.run(cmd)


if __name__ == '__main__':

    # 传入要启动的环境和env名字即可启动
    launcher(['LHSN'], 'katanabin')
