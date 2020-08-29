from functools import reduce
import json;

if __name__ == "__main__":

    base1 = 303
    base2 = 319
    base = base1 + base2

    heights1 = [225,256,269,274,277,275,267,252,226,213,214,213,209,212,222,223,220,219,218,215,209,199,190,201];
    heights2 = [228,268,285,292,295,294,285,271,251,235,231,231,232,233,236,236,235,235,235,230,221,212,203,210];
    heights = [heights1[i] + heights2[i] for i in range(len(heights1))]

    heights_sum = reduce(lambda x,y: x+y,heights)
    heights_sum_biased = base*len(heights) - heights_sum
    k = 100/heights_sum_biased

    rates = [k*(base-height) for height in heights]

    result = {"rate":{i:rates[i] for i in range(len(rates))}};
    result_file = open("data/tweet_and_retweet_rate_of_one_day.json",'w')
    json.dump(result,result_file);