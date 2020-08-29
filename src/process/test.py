import mysql.connector;
import util;

def test_count():
    connection = mysql.connector.connect(host="127.0.0.1",
                                port=3307,
                                user='root',
                                password='123456',
                                db = 'weibo');
    
    cur = connection.cursor();

    result = util.counts(cur,"人传人","","IGNORE","2020-01-21 00:00:00", "2020-01-25 00:00:00",'H');

    assert result["counts"][0] >= 3104; assert result["counts"][1] >= 1273;
    assert result["counts"][2] >= 588; assert result["counts"][3] >= 356;
    assert result["counts"][4] >= 303; assert result["counts"][5] >= 483;
    assert result["counts"][6] >= 906; assert result["counts"][7] >= 2037;
    assert result["counts"][8] >= 2519; assert result["counts"][9] >= 2587;
    assert result["counts"][10] >= 2072;

    result = util.counts(cur,"一级响应","","IGNORE","2020-01-23 22:00:00","2020-01-25 00:00:00",'H');

    assert result["counts"][0 ] >= 67 ; assert result["counts"][1 ] >= 172; assert result["counts"][2 ] >= 128;
    assert result["counts"][3 ] >= 82 ; assert result["counts"][4 ] >= 20 ; assert result["counts"][5 ] >= 9  ;
    assert result["counts"][6 ] >= 11 ; assert result["counts"][7 ] >= 8  ; assert result["counts"][8 ] >= 10 ;
    assert result["counts"][9 ] >= 32 ; assert result["counts"][10] >= 45 ; assert result["counts"][11] >= 40 ;
    assert result["counts"][12] >= 45 ; assert result["counts"][13] >= 33 ; assert result["counts"][14] >= 148;
    assert result["counts"][15] >= 191; assert result["counts"][16] >= 180; assert result["counts"][17] >= 192;

    result = util.counts(cur,"浙江","一级响应","AND","2020-01-23 22:00:00","2020-01-25 00:00:00",'H');

    assert result["counts"][0 ] >= 52 ; assert result["counts"][1 ] >= 78 ; assert result["counts"][2 ] >= 62 ;
    assert result["counts"][3 ] >= 49 ; assert result["counts"][4 ] >= 11 ; assert result["counts"][5 ] >= 7  ;
    assert result["counts"][6 ] >= 5  ; assert result["counts"][7 ] >= 6  ; assert result["counts"][8 ] >= 7  ;
    assert result["counts"][9 ] >= 26 ; assert result["counts"][10] >= 34 ; assert result["counts"][11] >= 36 ;
    assert result["counts"][12] >= 41 ; assert result["counts"][13] >= 27 ; assert result["counts"][14] >= 121;
    assert result["counts"][15] >= 161; assert result["counts"][16] >= 134; assert result["counts"][17] >= 162;

    assert result["counts"][0 ] <= 67 ; assert result["counts"][1 ] <= 172; assert result["counts"][2 ] <= 128;
    assert result["counts"][3 ] <= 82 ; assert result["counts"][4 ] <= 20 ; assert result["counts"][5 ] <= 9  ;
    assert result["counts"][6 ] <= 11 ; assert result["counts"][7 ] <= 8  ; assert result["counts"][8 ] <= 10 ;
    assert result["counts"][9 ] <= 32 ; assert result["counts"][10] <= 45 ; assert result["counts"][11] <= 40 ;
    assert result["counts"][12] <= 45 ; assert result["counts"][13] <= 33 ; assert result["counts"][14] <= 148;
    assert result["counts"][15] <= 191; assert result["counts"][16] <= 180; assert result["counts"][17] <= 192;

    result = util.counts(cur,"浙江","广东","OR","2020-01-23 22:00:00","2020-01-25 00:00:00",'H');

    assert result["counts"][0 ] >= 103; assert result["counts"][1 ] >= 197; assert result["counts"][2 ] >= 146;
    assert result["counts"][3 ] >= 96 ; assert result["counts"][4 ] >= 31 ; assert result["counts"][5 ] >= 19 ;
    assert result["counts"][6 ] >= 17 ; assert result["counts"][7 ] >= 16 ; assert result["counts"][8 ] >= 21 ;

    result = util.counts(cur,"浙江","广东","ERRORTEST","2020-01-23 22:00:00","2020-01-25 00:00:00",'H');

    assert len(result["counts"]) == 0;
    

 