from pyecharts import *
import newgetdata
from conf import setting
import os


project_name = 'safety'
project_id = setting.pool[project_name]['pro_id']
project_name_cn = setting.pool[project_name]['cn_name']
base_path = os.path.abspath('.')
chart_path = os.path.join(base_path, 'chart')


def get_result(by_type, pro_id, L=None):
    """
    获取资源及资源对应的issue数量
    :param by_type: 资源类别，version: 目标版本，category：类别；field：自定义属性字段，tracker：跟踪类型
    :param pro_id: 项目标识
    :param L: 列表，若每个资源类别下的分类太多如目标版本下的版本若太多，不建议使用列表存储
    :return: 由(资源类别下的具体资源分类名称，资源下的issue总数量)构成的元祖为单位组成的列表
    """
    if L is None:
        L = []
    result = newgetdata.get_bugs_num(by_type, pro_id)
    if result is not None:
        for r in result:
            L.append(r)
    else:
        print('请检查资源是否存在，无法获得bug相关的资源')
    return L


def chart_by_type(by_type, pro_id, title, item='bug'):
    """
    生成项目bug数量按不同分类的统计图表
    非缺陷程度（按测试分类、目标版本）的bug统计图类型为折线图；缺陷程度的bug统计图表类型为柱状图
    :param by_type: 分类，默认按版本
    :param pro_id: 项目标识
    :param title: 生成的图表默认的title
    :param item: 生成的图表上的图示
    :return: html格式的图表
    """
    attr = []
    v1 = []
    result = get_result(by_type, pro_id)
    if len(result) != 0 and by_type != 'filed':
        for i in range(len(result)):
            attr.append(result[i][0])
            v1.append(result[i][1])
        line = Line(title, width=1200, height=600)
        # line.add(item, attr, v1, is_label_show=True)
        line.add(item, attr, v1, is_label_show=True, xaxis_interval=0, xaxis_rotate=-30)
        if os.path.exists(os.path.join(chart_path, '%s.html' % title)):
            os.remove(os.path.join(chart_path, '%s.html' % title))
        line.render(os.path.join(chart_path, '%s.html' % title))
    elif len(result) != 0 and by_type == 'field':
        for i in range(len(result)):
            attr.append(result[i][0])
            v1.append(result[i][1])
        bar = Bar(title)
        bar.add(item, attr, v1)
        if os.path.exists(os.path.join(chart_path, '%s.html' % title)):
            os.remove(os.path.join(chart_path, '%s.html' % title))
        bar.render(os.path.join(chart_path, '%s.html' % title))
    else:
        print('没有数据可展示或数据条数为0')


def chart_by_one_ver(by_type, pro_id, L=None):
    """
    为项目的单一测试版本产生的bug生成按bug分类的柱形图，按缺陷程度的柱形图
    由于单版本的不存在按版本的统计图表，单独为项目单一版本写的此方法
    :param by_type: 分类，默认按版本
    :param pro_id: 项目标识
    :param L: 资源类别名称、资源issue数量组成的列表
    :return: html格式的图表
    """
    if L is None:
        L = []
        result = newgetdata.get_issue_by_one_ver(by_type, pro_id)
        for v in result:
            L.append(v)
        attr = []
        v1 = []
    else:
        print('L的类型必须为None，请检查')
    if len(L) != 0 and by_type == 'category':
        for i in range(len(L)):
            attr.append(L[i][0])
        for j in range(len(L)):
            v1.append(L[j][1])
        v = input('请输入项目版本号，格式：V5.2.1\n')
        name = project_name_cn
        bar = Bar('%s %s 不同分类bug分布' % (name, v))
        bar.add('bug分类', attr, v1)
        if os.path.exists(os.path.join(chart_path, '%s %s 不同分类bug分布.html' % (name, v))):
            os.remove(os.path.join(chart_path, '%s %s 不同分类bug分布.html' % (name, v)))
        bar.render(os.path.join(chart_path, '%s %s 不同分类bug分布.html' % (name, v)))
    elif len(L) != 0 and by_type == 'field':
        for i in range(len(L)):
            attr.append(L[i][0])
        for j in range(len(L)):
            v1.append(L[j][1])
        v = input('请输入项目的版本号，格式V5.2.1\n')
        name = project_name_cn
        bar = Bar('%s %s bug缺陷程度分布' % (name, v))
        bar.add('bug缺陷程度', attr, v1)
        if os.path.exists(os.path.join(chart_path, '%s %s bug缺陷程度分布.html' % (name, v))):
            os.remove(os.path.join(chart_path, '%s %s bug缺陷程度分布.html' % (name, v)))
        bar.render(os.path.join(chart_path, '%s %s bug缺陷程度分布.html' % (name, v)))
    else:
        print('没有数据可展示')


if __name__ == '__main__':
    s = input(
        '请输入要生成图表数据类型：\n'
        '1 表示项目所有版本内的信息\n'
        '2 表示项目某个特定版本内的bug信息\n'
        '3 表示单元测试\n'
        '4 表示doctest\n'
    )
    if s == '1':
        chart_by_type('version', project_id, '%s不同版本所有跟踪类型的记录统计' % project_name_cn)
        chart_by_type('category', project_id, '%s不同测试类别bug分布' % project_name_cn)
        chart_by_type('field', project_id, '%sbug缺陷程度分布' % project_name_cn)
        chart_by_type('tracker', project_id, '%s不同版本bug分布' % project_name_cn)
    if s == '2':
        chart_by_one_ver('category', project_id)
        chart_by_one_ver('field', project_id)
    if s == '3':
        result = get_result('field', project_id)
        print(result)
    if s == '4':
        from doctest import testmod
        testmod()




