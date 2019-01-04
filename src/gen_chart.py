from pyecharts import Bar
from dbmanager import DbManager
from pyecharts import WordCloud
from pyecharts import Pie


# 生成各分支人数的云图
def gen_subtype_wordcloud():
    file_name = '../output/subtype.html'
    title = ''#''各分支人数统计'
    sub_title = ''#''截止到2018年12月31日'
    sql = '''select subtype , count(*) as cnt
                from tb_members
                group by subtype
                having locate(';',subtype)=0
                order by cnt '''
    gen_chart_by_sql(file_name, title, sub_title, sql,'wordcloud')


# 生成各世代人数统计的柱状图
def gen_descent_no_bar():
    file_name = '../output/descent_no.html'
    title = ''#''各世人数统计'
    sub_title = ''#''截止到2018年12月31日'
    sql = '''select concat(descent_no,'世') as no, count(*) as cnt
                        from tb_members
                        where descent_no  <> 0
                        group by descent_no
                        order by descent_no'''
    gen_chart_by_sql(file_name, title, sub_title, sql)


# 生成各性别人数统计的饼状图
def gen_sex_pie():
    file_name = '../output/sex_pie.html'
    title = ''#''男女人数分布'
    sub_title = ''#''截止到2018年12月31日'
    sql = '''select (case sex when 1 then '男' when 0 then '女' end) as sex_name, count(*) 
            from tb_members 
            group by sex_name'''
    gen_chart_by_sql(file_name, title, sub_title, sql, 'pie')


def gen_chart_by_sql(file_name, title, sub_title, sql, chart_type='bar'):
    db_manager = DbManager()
    cur = db_manager.conn.cursor()

    name = []
    value = []

    cur.execute(sql)
    for r in cur:
        print(r[0], r[1])
        name.append(r[0])
        value.append(r[1])

    cur.close()
    db_manager.close()

    if chart_type == 'bar':
        gen_bar(file_name, title, sub_title, name, value)
    elif chart_type == 'wordcloud':
        gen_wordcloud(file_name, title, sub_title, name, value)
    elif chart_type == 'pie':
        gen_pie(file_name, title, sub_title, name, value)


# 生成柱状图
def gen_bar(file_name, title, sub_title, name, value):
    bar = Bar(title, sub_title)
    bar.width = 900
    bar.height = 1050
    bar.add("", name, value,
            xaxis_interval=0,
            bar_category_gap=20, # 类目轴的柱状距离，当设置为 0 时柱状是紧挨着（直方图类型），默认为 '20%'
            is_convert=False,
            #is_label_show=True,
            #xaxis_type='category',
            #is_xaxis_inverse = True,
            is_yaxis_boundarygap=True,
            is_xaxis_boundarygap=True

            )
    bar.render(file_name)


# 生成云图
def gen_wordcloud(file_name, title, sub_title, name , value):
    wordcloud = WordCloud(width=2000, height=820, title=title,subtitle=sub_title )
    wordcloud.add("", name, value, word_size_range=[50, 150],shape='circle')
    wordcloud.render(file_name)


def gen_pie(file_name, title, sub_title, name, value):
    pie = Pie('')#Pie("男女人数分布")
    pie.add("", name, value, is_label_show=True)
    pie.render(file_name)


if __name__ == "__main__":
    gen_subtype_wordcloud()
    gen_descent_no_bar()
    gen_sex_pie()