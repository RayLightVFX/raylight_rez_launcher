# RezLauncher

RezLauncher 是一个用于启动和管理 Rez 环境的图形用户界面应用程序。

## 功能特点

- 图形化界面管理 Rez 环境
- 快速启动预配置的 Rez 环境
- 自定义 Rez 包配置
- 因未定义Linux路径，故目前只支持 Windows 平台

# 注意
- 因rez兼容问题，本项目暂时采用python3.9

## 安装指南

1. clone 本仓库
```shell
git clone
```
2. 设置虚拟环境和激活虚拟环境
```shell
python -m venv venv
venv\Scripts\activate.bat
```
3. 安装依赖
```shell
pip install -r requirements.txt
```
4. 运行
```shell
python ren_launcher.py
```

## 使用指南
- rez 的仓库路径地址为 `\\10.6.9.26\rez`，在当前目录中配置了 `rez_repo.json` 文件，文件中指定了各个插件路径，如果新增或修改，请在文件中修改。
- `resource` 文件夹中存放了一些资源文件，如图标等。
- `rez_resolved_context.py` 文件中存放了解析 rez 包的函数，用于解析 rez 包的依赖关系。并且此包可直接输入环境名和启动的命令启动测试。
