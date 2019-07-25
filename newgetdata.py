from redminelib import Redmine
from redminelib import exceptions
from conf import setting
from collections import Iterable


redmine = Redmine(setting.REDMINE_URL, key=setting.REDMINE_KEY)
# pro_id = setting.PROJECT_ID
# spec_id = setting.SPEC_ID
name = 'safety'
pro_id = setting.PROJECT_POOL[name]['PROJECT_ID']
spec_id = setting.PROJECT_POOL[name]['SPEC_ID']


def get_info(bytype, pro):
    """
    按资源类别获取项目对应资源的合集
    https://python-redmine.com/
    :param bytype: 资源类别，version: 目标版本，category：类别；field：自定义属性字段，tracker：跟踪类型
    :param pro: 项目标识
    :return: 资源合集对象或资源属性

    >>> redmine.version.filter(project_id='homme')
    <redminelib.resultsets.ResourceSet object with Version resources>
    >>> vs = redmine.version.filter(project_id='homme')
    >>> isinstance(vs, Iterable)
    True
    """
    try:
        if bytype == 'version':
            result = redmine.version.filter(project_id=pro)
        elif bytype == 'category':
            result = redmine.issue_category.filter(project_id=pro)
        elif bytype == 'field':
            fields = redmine.custom_field.all()
            for f in fields:
                if f.name == '缺陷程度':
                    result = f.id
                    break
        elif bytype == 'tracker':   # 获取跟踪类型为错误的id， 为redmine.issue.filter(**filters)中tracker_id参数提供数据
            trackers = redmine.tracker.all()
            for tracker in trackers:
                if tracker.name == '错误':
                    result = tracker.id
                    break
        else:
            print('请检查要获取的资源的分类类型是否正确')
        return result
    except exceptions.ResourceNotFoundError as e:
        print('except', e)


def get_bugnums(bytype, pro):
    """
    生成器，由资源分类名称、分类下的issue数量组成
    :param bytype: 资源类别，version: 目标版本，category：类别；field：自定义属性字段，tracker：跟踪类型
    :param pro: 项目标识
    :return: 每个资源名称、资源下的issue总数量
    """
    try:
        if bytype == 'version' or bytype == 'category':
            typeobj = get_info(bytype, pro)
            for x in typeobj:   # 每个目标版本或分类类别，对应的issue数量（包括所有跟踪类别，若只跟踪错误，添加tracker_id）
                if bytype == 'version':
                    bugsobj = redmine.issue.filter(project_id=pro, status_id='*', fixed_version_id=x.id)
                    bugslen = len(bugsobj)
                elif bytype == 'category':
                    bugsobj = redmine.issue.filter(project_id=pro, status_id='*', category_id=x.id)
                    bugslen = len(bugsobj)
                yield x.name, bugslen
        elif bytype == 'field':
            cf_x = ['致命', '严重', '普通', '低']
            for x in cf_x:
                bugsobj = redmine.issue.filter(
                    project_id=pro,
                    status_id='*',
                    cf_1=x  # cf_x，其中x为自定义字段‘缺陷程度’的id值，id值可使用get_custom_field()获取
                )
                bugslen = len(bugsobj)
                yield x, bugslen
        elif bytype == 'tracker':
            versions = get_info('version', pro)
            tracker_id = get_info(bytype, pro)
            for x in versions:
                if tracker_id:
                    bugsobj = redmine.issue.filter(
                        project_id=pro,
                        status_id='*',
                        fixed_version_id=x.id,
                        tracker_id=tracker_id
                    )
                    bugslen = len(bugsobj)
                    yield x.name, bugslen
        else:
            print('要获取资源的分类不正确，请检查后输入正确的分类标识')
    except exceptions.ResourceNotFoundError as e:
        print('except', e)


def get_issue_by_onever(bytype, pro):
    """
    只获取某个特定版本内的bug数据，分别按bug分类、bug缺陷程度统计
    :param bytype: 类型，用于条件选择使用的接口和过滤条件
    :param project: 项目标识
    :return:
    """
    try:
        versions = get_info('version', pro)
        for v in versions:
            print(v.id, v.name)
        v = int(input('请输入需要过滤查询的版本号id\n'))
        if bytype == 'category':
            categories = get_info(bytype, pro)
            for c in categories:
                issues = redmine.issue.filter(
                    project_id=pro,
                    status_id='*',
                    fixed_version_id=v,
                    tracker_id=1,  # 跟踪类型为‘错误’
                    category_id=c.id
                )
                issues_num = len(issues)
                yield c.name, issues_num
        if bytype == 'field':
            cf_x = ['致命', '严重', '普通', '低']
            for c in cf_x:
                issues = redmine.issue.filter(
                    project_id=pro,
                    status_id='*',
                    fixed_version_id=v,
                    tracker_id=1,
                    cf_1=c
                )
                issues_num = len(issues)
                yield c, issues_num
    except exceptions.ResourceNotFoundError as e:
        print('except', e)


if __name__ == '__main__':
    s = input('请输入要查询或测试的类别：\n 1 doctest\n 2 单元测试\n')
    if s == '1':
        from doctest import testmod
        testmod()
    if s == '2':
        result = get_bugnums('version', pro_id)
        for r in result:
            print(r)
            print(type(r))







