from pyecharts import options as opts
from pyecharts.charts import Bar, Line
import getdata
from conf import setting
import os


project_name = 'safety'
project_id = setting.pool[project_name]['pro_id']
project_name_cn = setting.pool[project_name]['cn_name']
base_path = os.path.abspath('.')
chart_path = os.path.join(base_path, 'chart')


def get_result(by_type, pro_id, L=None):
    """
    获取资源和资源对应的bug数量
    :param by_type: 资源类别（如version: 目标版本，category：类别）
    :param pro_id: 项目标识
    :param L: 存储数据列表
    :return: [(分类，分类bug数量)]
    """
    if L is None:
        L = []
    result = getdata.get_bugs_num(by_type, pro_id)
    if result is not None:
        for r in result:
            L.append(r)
    else:
        print('请检查资源是否存在，无法获得bug相关的资源')
    return L


def chart_by_type(by_type, pro_id, title, item='bug'):
    """
    生成项目按不同分类的bug分布图表
    :param by_type: 分类
    :param pro_id: 项目标识
    :param title: 生成的图表title
    :param item: 生成的图表上的图示
    :return: html格式的图表
    """
    result = get_result(by_type, pro_id)
    if len(result) != 0:
        xaxis_data = [x[0] for x in result]
        yaxis_data = [x[1] for x in result]
        line = Line()
        line.add_xaxis(xaxis_data)
        line.add_yaxis(item, yaxis_data)
        line.set_global_opts(title_opts=opts.TitleOpts(title=title))
        if os.path.exists(os.path.join(chart_path, '%s.html' % title)):
            os.remove(os.path.join(chart_path, '%s.html' % title))
        line.render(os.path.join(chart_path, '%s.html' % title))
    else:
        print('没有数据可展示或数据条数为0')


def chart_by_one_ver(by_type, pro_id, item, title, L=None):
    """
    生成项目特定版本下的不同分类的bug分布图表
    :param by_type: 分类
    :param pro_id: 项目标识
    :param L: 资源类别名称、资源bug数量组成的列表
    :param item: 图表图示
    :param title: 图表title
    :return: html格式的图表
    """
    if L is None:
        L = []
        result = getdata.get_issue_by_one_ver(by_type, pro_id)
        for v in result:
            L.append(v)
        xaxis_data = []
        yaxis_data = []
    else:
        print('L的类型必须为None，请检查')
    if len(L) != 0:
        xaxis_data = [x[0] for x in L]
        yaxis_data = [x[1] for x in L]
        v_name = [x[2] for x in L][0]
        title = ''.join([title, v_name, '版本'])
        bar = Bar()
        bar.add_xaxis(xaxis_data)
        bar.add_yaxis(item, yaxis_data)
        bar.set_global_opts(title_opts=opts.TitleOpts(title=title))
        if os.path.exists(os.path.join(chart_path, '{}.html'.format(title))):
            os.remove(os.path.join(chart_path, '{}.html'.format(title)))
        bar.render(os.path.join(chart_path, '{}.html'.format(title)))
    else:
        print('没有数据可展示')


def test():
    s = input(
        '请输入要生成图表数据类型：\n'
        '1 项目所有版本内的信息\n'
        '2 项目某个特定版本内的bug信息\n'
        '3 单元测试\n'
        '4 doctest\n'
    )
    if s == '1':
        chart_by_type('version', project_id, '{}不同版本bug分布'.format(project_name_cn))
        chart_by_type('category', project_id, '{}不同测试类别bug分布'.format(project_name_cn))
        chart_by_type('field', project_id, '{}bug缺陷程度分布'.format(project_name_cn))
    if s == '2':
        chart_by_one_ver('category', project_id, 'bug分类', '{}不同类别bug分布'.format(project_name_cn))
        chart_by_one_ver('field', project_id, 'bug缺陷程度', '{}不同缺陷程度bug分布'.format(project_name_cn))
    if s == '3':
        results = get_result('field', project_id)
        print(results)
    if s == '4':
        from doctest import testmod
        testmod()


if __name__ == '__main__':
    test()

