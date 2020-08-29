# 用于计算统计信息

import mysql.connector;
from tqdm import tqdm;
import matplotlib.pyplot as plt;

if __name__ == "__main__":

    connection = mysql.connector.connect(host="127.0.0.1",
                                port=3307,
                                user='root',
                                password='123456',
                                db = 'weibo');
    
    cur = connection.cursor();
    cur.execute("select reposts_count from weibo");
    popularities = []
    max = 0;
    for r in cur:
        if(r[0] < 10):
            continue;
        if(r[0] > max):
            max = r[0];
        popularities.append(r[0]);
    print(len(popularities));
    print(max);
    plt.yscale('log');
    n,bins,patches = plt.hist(popularities,50);
    
    plt.savefig("images/histogram.png");
