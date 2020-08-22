import requests;
import json;
import mysql.connector;
from tqdm import tqdm;

if __name__ == "__main__":
    time_count_url = "http://www.eecso.com/test/weibo/apis/getlatest.php";
    r = requests.get(time_count_url);

    data = json.loads(r.content);

    all_hots = [];

    count = 0;
    for i in tqdm(range(100017,int(data[0]))):
    # for i in range(10):
        hot_url = "http://www.eecso.com/test/weibo/apis/currentitems.php?timeid=%d"%(i+1);
        r = requests.get(hot_url);
        content = r.content.decode('unicode_escape');
        data = json.loads(content);
        for line in data:
            count += 1;
            all_hots.append((count,*line));
        if(count >= 100000):
            break;

    conn = mysql.connector.connect(host='127.0.0.1',
                            user="root",
                            password="123456",
                            database='weibo',
                            port=3307);
    
    cur = conn.cursor();
    cur.execute("drop table if exists hot;");
    cur.execute("create table if not exists hot (id int, hot_event varchar(100), start varchar(20), end varchar(20), time int);");
    cur.executemany("insert into hot (id,hot_event,start,end,time) values (%s,%s,%s,%s,%s)",all_hots);
    cur.close();
    conn.commit();
    conn.close();
