# 单个时间的流行度变化

import mysql.connector;
import pandas as pd;
import datetime;
import matplotlib.pyplot as plt;

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

def search_event(cur,keyword):
    keyword1 = "";
    keyword2 = "";
    relationship = "";
    if("&" in keyword):
        keyword1 = keyword.split("&")[0];
        keyword2 = keyword.split("&")[1];
        relationship = " and ";
    elif("|" in keyword):
        keyword1 = keyword.split("|")[0];
        keyword2 = keyword.split("|")[1];
        relationship = " or ";
    else:
        keyword1 = keyword;
    if((relationship == " and ") or (relationship == " or ")):
        cur.execute("select text,created_at from weibo where locate('" + keyword1 + "',text) > 0" + relationship + " locate('" + keyword2 + "',text)>0");
    else:
        cur.execute("select text,created_at from weibo where locate('" + keyword1 + "',text) > 0");
    
    return cur;

if __name__ == "__main__":

    event_name = "医务人员感染"

    connection = mysql.connector.connect(host="127.0.0.1",
                                port=3307,
                                user='root',
                                password='123456',
                                db = 'weibo');
    
    cur = connection.cursor();
    # cur.execute("select text,created_at from weibo where locate('" + event_name + "',text)");
    cur.execute("select text,created_at from weibo where locate('医务人员',text) > 0 and locate('感染',text) > 0;");

    start = datetime.datetime(2020,1,20);

    end = datetime.datetime(2020,1,25);

    index = pd.date_range(start,end,freq='H');

    x = [str(i)[11:16] for i in index];

    print(len(index))

    frame = pd.DataFrame([0] * len(index),columns=["count"],index = index);

    index_set = set(index)
    print(frame)
    print(frame.loc['2020-01-24 00:00:00'])
    for r in cur:
        current_index = str(r[1])[:14] + "00:00"

        if(pd.to_datetime(current_index) not in index_set):
            print(current_index)
            continue;
        frame.loc[current_index]["count"] = frame.loc[current_index]["count"] + 1;
    
    # counts = []
    # for r in cur:
    #     counts.append(frame["count"][current_index])

    counts = []
    for single in frame["count"]:
        counts.append(single)
    
    print(counts);
    fig,ax = plt.subplots();
    ax.bar(range(len(counts)),counts)
    # ax.set_yscale('log');

    pos = []
    lable = []
    for i in range(len(x)):
        if i%20 == 0:
            pos.append(i);
            lable.append(x[i]);
    plt.xticks(pos,lable);

    plt.savefig("images/" + event_name + "_popularity_timeseries.png");
