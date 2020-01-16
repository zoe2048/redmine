import platform
import shutil
import os

'''
根据当前环境python版本
安装pyecharts对应的版本
执行对应的生成图表的脚本
'''


def chk_python_version():
    v = platform.python_version()
    if v[:-2] == '3.7':
        version = '3.7'
        return version
    elif v[:-2] == '3.8':
        version = '3.8'
        return version
    else:
        print('检查当前环境python版本')


def create_req_file():
    v = chk_python_version()
    if v == '3.7':
        shutil.copyfile('requirements3.7.txt', 'requirements.txt')
    elif v == '3.8':
        shutil.copyfile('requirements3.8.txt', 'requirements.txt')
    else:
        raise


def install_libs_from_req(filenm='requirements.txt'):
    if os.path.exists(os.path.join(os.path.abspath('.'), filenm)):
        os.system('pip show pyecharts')
        command = os.system('pip show pyecharts')
        if command == 1:
            os.system('pip install -r requirements.txt')
            result = os.system('pip install -r requirements.txt')
            if result == 0:
                return True
            else:
                return False
        elif command == 0:
            return True
        else:
            print('检查pyecharts等包是否已安装')
    else:
        create_req_file()
        return install_libs_from_req()


if __name__ == '__main__':
    is_installed = install_libs_from_req()
    if is_installed:
        current_version = chk_python_version()
        if current_version == '3.7':
            import newchartdada
            newchartdada.test()
        elif current_version == '3.8':
            import chartdata
            chartdata.test()
    else:
        print('脚本执行需要的安装包未安装或安装失败，请先检查')

