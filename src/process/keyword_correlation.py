import util;
import matplotlib.pyplot as plt;
import mysql.connector;

if __name__ == "__main__":
    connection = mysql.connector.connect(host="127.0.0.1",
                                port=3307,
                                user='root',
                                password='123456',
                                db = 'weibo');
    cur = connection.cursor();

    hot_keyword = util.get_top_hot_words("data/result.json",True,True,True,10);

    search_result = util.search_by_single_keyword(cur,"人传人");
    freq1 = util.counts(search_result,"2020-01-20 00:00:00","2020-01-25 00:00:00",'H');
    search_result = util.search_by_single_keyword(cur,"钟南山");
    freq2 = util.counts(search_result,"2020-01-20 00:00:00","2020-01-25 00:00:00","H");
    plt.scatter(freq1["counts"],freq2["counts"]);
    plt.savefig("images/scatter_.png");