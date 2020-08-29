import jieba;
from tqdm import tqdm;
import json;
import mysql.connector;

if __name__ == "__main__":
    connection = mysql.connector.connect(host="127.0.0.1",
                                port=3307,
                                user='root',
                                password='123456',
                                db = 'weibo');
    
    cur = connection.cursor();
    cur.execute("select text,created_at from weibo");

    counts = {};

    for item in tqdm(cur):
        seg_list = jieba.cut(item[0]);
        for seg in seg_list:
            if(seg in counts):
                counts[seg] = counts[seg] + 1;
            else:
                counts[seg] = 1;
    
    file = open("result.json",'w');
    json.dump(counts, file,ensure_ascii=False);
    file.close();