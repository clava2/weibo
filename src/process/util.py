
from datetime import datetime;
import pandas as pd;

import json;
import re;

import logging;

import time;

import matplotlib.pyplot as plt;

'''
将搜索结果转换为时间轴上的数量分布
    :param cur: 数据库连接
    :param keyword1: 关键词1
    :param keyword2: 关键词2
    :param relationship: 关键词关系，支持此的关系为'AND', 'OR','NOT'
                            'AND': 关键词1和关键词2与关系
                            'OR':  关键词1和关键词2或关系
                            'IGNORE': 忽略关键词2，只考虑关键词1
    :param start_time: 开始时间
    :param end_time: 结束时间
    :param freq: 时间间隔，可取值为'H'(小时),'D'(天).
    :return counts: 字典类型，包含两个key:
                "index": 时间索引
                "counts": 数量
'''
def counts(cur,keyword1,keyword2,relationship,start_time,end_time,freq):

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler("log/counts.log",mode='w')
    file_handler.setLevel(logging.INFO)
    ch = logging.StreamHandler();
    ch.setLevel(logging.INFO);
    formatter = logging.Formatter("[%(asctime)s][%(name)s][%(levelname)s]:%(message)s")
    file_handler.setFormatter(formatter);
    ch.setFormatter(formatter);

    logger.addHandler(file_handler);
    logger.addHandler(ch);

    if(relationship not in set(["AND","OR","NOT","IGNORE"])):
        logger.error("关键词关系错误，合法值为'AND','OR','NOT','IGNORE'");
        return {"index":[],"counts":[]};



    logger.info("initializing container and time info");



    start = datetime.strptime(start_time,'%Y-%m-%d %H:%M:%S');
    end = datetime.strptime(end_time,'%Y-%m-%d %H:%M:%S');

    index = pd.date_range(start,end,freq=freq);
    x = [str(i)[11:16] for i in index];
    frame = pd.DataFrame([0] * len(index),columns=["count"],index = index);

    index_set = set(index)


    logger.info("initialized.")



    for time in index:
        current_index = str(time)[:14] + "00:00"
        logger.info("searching in time index: " + current_index)
        
        if((relationship == 'AND') or (relationship == 'OR')):
            cur.execute("select count(*) from weibo where (locate('" + keyword1 + "',text) > 0 " + relationship + " locate('" + keyword2 + "',text) > 0) and YEAR(created_at) = " + current_index[0:4] + " and MONTH(created_at) = " + current_index[5:7] + " and DAY(created_at) = " + current_index[8:10] + " and HOUR(created_at) = " + current_index[11:13] + ";")
        elif(relationship == 'IGNORE') :
            cur.execute("select count(*) from weibo where locate('" + keyword1 + "',text) > 0 and YEAR(created_at) = " + current_index[0:4] + " and MONTH(created_at) = " + current_index[5:7] + " and DAY(created_at) = " + current_index[8:10] + " and HOUR(created_at) = " + current_index[11:13] + ";")
        for r in cur:
            frame.loc[current_index]["count"] = int(r[0]);

    logger.info("complete");

    counts = []
    for single in frame["count"]:
        counts.append(single)
    result = {"index": index,"counts": counts};
    return result;


def plot(popularity):
    plt.plot(popularity);
    plt.savefig("images/curve_popularity.png");

def scatter(x,y):
    plt.scatter(x,y);
    plt.savefig("images/scatter.png");


def get_top_hot_words(json_file_name,filter_non_chinese, filter_non_word,filter_unimportant_word,count):
    file = open("json_file_name",'r');
    result = json.load(file);
    key = result.keys();
    all_count = [];

    chinese_word = re.compile(u'[\u4e00-\u8fa5]')
    sign = re.compile("[\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b]")
    except_word = set(["的","了","在","是","有","不","我","和","也",
                        "要","不是","上","很","中","啊","从","吗","能","让",
                        "就是","他","与","无","看","这个","后","会","好","可能","工作",
                        "但","为","等","可以","名","我们","被","不要","说","对","月","就",
                        "日","个","同时","将","吧","进行","时","请","来","已","没","市民","时候",
                        "们","——","并"]);
    for k in key:
        # 判断是不是中文字符，不是则返回
        if(filter_non_chinese and (not chinese_word.search(k))):
            continue;
        # 判断是不是中文标点，是则返回
        if(filter_non_word and sign.search(k)):
            continue;
        # 判断是不是排除的字符，如果是则返回
        if(filter_unimportant_word and (k in except_word)):
            continue;
        all_count.append([k,result[k]]);
    
    all_count.sort(key = lambda count: count[1]);
    all_count = all_count[-count:];
    result = {};
    for count in all_count:
        result[count[0]] = count[1];
    
    return result;