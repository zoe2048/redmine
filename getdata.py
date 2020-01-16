from redminelib import Redmine
from redminelib import exceptions
from conf import setting
from collections import Iterable


redmine = Redmine(setting.url, key=setting.key)
project_name = 'safety'
project_id = setting.pool[project_name]['pro_id']


def get_info(by_type, pro_id):
    """
    按资源类别获取项目对应资源合集，redmine库使用官方资料：https://python-redmine.com/
    :param by_type: 资源类别（如version: 目标版本，category：类别）
    :param pro_id: 项目标识
    :return: 资源合集对象

    >>> redmine.version.filter(project_id='safety')
    <redminelib.resultsets.ResourceSet object with Version resources>
    >>> vs = redmine.version.filter(project_id='safety')
    >>> isinstance(vs, Iterable)
    True
    """
    try:
        if by_type == 'version':
            result = redmine.version.filter(project_id=pro_id)
        elif by_type == 'category':
            result = redmine.issue_category.filter(project_id=pro_id)
        else:
            print('请检查要获取的资源的分类类型是否正确')
        return result
    except exceptions.ResourceNotFoundError as e:
        print('except', e)


def get_id(by_type):
    """
    获取自定义字段或跟踪类型信息
    """
    if by_type == 'field':
        result = redmine.custom_field.all()
        for cf in result:
            if cf.name == '缺陷程度':
                cf_qxcd = []
                for value in cf.possible_values:
                    cf_qxcd.append(value['value'])
                return cf_qxcd
            else:
                continue
        if cf.name != '缺陷程度':
            return False
    elif by_type == 'tracker':
        result = redmine.tracker.all()
        for track in result:
            if track.name == '错误':
                return track.id, track.name
            else:
                continue
        if track.name != '错误':
            return False


def get_bugs_num(by_type, pro_id, tracker_id=1):
    """
    获取资源分类及分类下的issue数量
    :param by_type: 资源类别（version: 目标版本，category：类别；field：自定义属性字段）
    :param pro_id: 项目标识
    :param tracker_id: 跟踪类型的id（默认为错误）
    :return: 每个资源名称、资源下的issue总数量
    """
    try:
        if by_type == 'version' or by_type == 'category':
            typeobj = get_info(by_type, pro_id)
            for x in typeobj:   # 每个目标版本或分类类别对应的issue数量（包括所有跟踪类别，若只跟踪错误，添加tracker_id）
                if by_type == 'version':
                    bugsobj = redmine.issue.filter(
                        project_id=pro_id,
                        status_id='*',
                        fixed_version_id=x.id,
                        tracker_id=tracker_id
                    )
                    bugs_num = len(bugsobj)
                elif by_type == 'category':
                    bugsobj = redmine.issue.filter(
                        project_id=pro_id,
                        status_id='*',
                        category_id=x.id,
                        tracker_id=tracker_id
                    )
                    bugs_num = len(bugsobj)
                yield x.name, bugs_num
        elif by_type == 'field':
            cf_qxcd = get_id(by_type)
            for x in cf_qxcd:
                bugsobj = redmine.issue.filter(
                    project_id=pro_id,
                    status_id='*',
                    cf_1=x  # cf_1: 其中1为自定义字段‘缺陷程度’的id值，id值可使用redmine.get_custom_field()获取
                )
                bugs_num = len(bugsobj)
                yield x, bugs_num
        else:
            print('要获取资源的分类不正确，请检查后输入正确的分类标识')
    except exceptions.ResourceNotFoundError as e:
        print('except', e)


def get_issue_by_one_ver(by_type, pro_id):
    """
    只获取某个特定版本内的bug数据，分别按bug分类、bug缺陷程度统计
    :param by_type: 类型，用于条件选择使用的接口和过滤条件
    :param pro_id: 项目标识
    :return:
    """
    try:
        versions = get_info('version', pro_id)
        print('{}'.format('\n'.join([v.name for v in versions])))
        v_nm = input('请输入要生成图表的版本号如：V1\n')
        while v_nm not in [v.name for v in versions]:
            print('请输入要生成图表的版本号如：V1\n')
            v_nm = input()
        v_id = [v.id for v in versions if v.name == v_nm]
        if by_type == 'category':
            categories = get_info(by_type, pro_id)
            for c in categories:
                issues = redmine.issue.filter(
                    project_id=pro_id,
                    status_id='*',
                    fixed_version_id=v_id,
                    tracker_id=1,
                    category_id=c.id
                )
                issues_num = len(issues)
                yield c.name, issues_num, v_nm
        if by_type == 'field':
            cf_x = ['致命', '严重', '普通', '低']
            for c in cf_x:
                issues = redmine.issue.filter(
                    project_id=pro_id,
                    status_id='*',
                    fixed_version_id=v_id,
                    tracker_id=1,
                    cf_1=c
                )
                issues_num = len(issues)
                yield c, issues_num, v_nm
    except exceptions.ResourceNotFoundError as e:
        print('except', e)


if __name__ == '__main__':
    s = input('请输入要查询或测试的类别：\n 1 doctest\n 2 单元测试\n')
    if s == '1':
        from doctest import testmod
        testmod()
    if s == '2':
        results = get_bugs_num('version', project_id)
        for r in results:
            print(r)
            print(type(r))







