
import mysql.connector;
import pandas as pd;
import datetime;
import matplotlib.pyplot as plt;

def find_in_list(all,target):
    count = 0;
    for i in all:
        print(str(i));
        print(target);
        if str(i) == target:
            return count;
        count += 1;
    return -1;

if __name__ == "__main__":


    event_list = ["钟南山&人传人","湖北团拜会","医务人员感染","进出武汉管控","湖北&小汤山",
                    "湖北&二级相应","孙春兰","怕酒精&不耐高温","浙江广东一级响应","关闭离汉通道","请战书"];
    
    event_time = ["2020-01-20 21:00:00","2020-01-23 17:00:00","2020-01-21 00:00:00",
                    "2020-01-21 14:00:00","2020-01-22 00:00:00","2020-01-22 00:00:00",
                    "2020-01-22 00:00:00","2020-01-22 00:00:00","2020-01-23 00:00:00",
                    "2020-01-23 00:00:00","2020-01-23 00:00:00"];


    connection = mysql.connector.connect(host="127.0.0.1",
                                port=3307,
                                user='root',
                                password='123456',
                                db = 'weibo');
    
    cur = connection.cursor();
    cur.execute("select text,created_at from weibo");

    start = datetime.datetime(2020,1,20);

    end = datetime.datetime(2020,1,25);

    index = pd.date_range(start,end,freq='H');

    time_index = [find_in_list(index,event) for event in event_time];

    print(time_index);

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
    plt.bar(range(len(counts)),counts)

    for time in time_index:
        plt.vlines(time,0,10000,colors='r');

    plt.savefig("images/timeseries.png");

