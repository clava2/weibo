
import json;
import matplotlib.pyplot as plt;
from matplotlib import font_manager
import re;

if __name__ == "__main__":


    font = font_manager.FontProperties(fname="/var/home/zc/FengYu-HuaWenYuanTi-2.ttf");


    file = open("result.json",'r');
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
        if(not chinese_word.search(k)):
            continue;
        # 判断是不是中文标点，是则返回
        if(sign.search(k)):
            continue;
        # 判断是不是排除的字符，如果是则返回
        if(k in except_word):
            continue;
        all_count.append([k,result[k]]);
    all_count.sort(key = lambda count: count[1]);
    all_count = all_count[-10:];
    top_count = [];
    index = [];
    for count in all_count:
        index.append(count[0]);
        top_count.append(count[1]);
    print(index);
    plt.bar(range(len(top_count)),top_count);
    plt.xticks(range(len(top_count)),index,fontproperties=font);
    plt.savefig("images/top_count.png");