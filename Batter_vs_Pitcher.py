from random import choices
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.project

class Versus():
    league_obp = '82 - 0.338, \
        83 - 0.323,\
        84 - 0.326,\
        85 - 0.332,\
        86 - 0.322,\
        87 - 0.335,\
        88 - 0.336,\
        89 - 0.336,\
        90 - 0.339,\
        91 - 0.336,\
        92 - 0.345,\
        93 - 0.320,\
        94 - 0.327,\
        95 - 0.322,\
        96 - 0.327,\
        97 - 0.334,\
        98 - 0.331,\
        99 - 0.352,\
        00 - 0.347,\
        01 - 0.357,\
        02 - 0.335,\
        03 - 0.345,\
        04 - 0.347,\
        05 - 0.342,\
        06 - 0.330,\
        07 - 0.340,\
        08 - 0.342,\
        09 - 0.358,\
        10 - 0.351,\
        11 - 0.344,\
        12 - 0.334,\
        13 - 0.350,\
        14 - 0.365,\
        15 - 0.357,\
        16 - 0.364,\
        17 - 0.353,\
        18 - 0.353,\
        19 - 0.337,\
        20 - 0.349'
    list = league_obp.split(',')
    obp_dic = {}
    for item in list:
        item_split = item.split('-')
        obp_dic[item_split[0].strip()] = float(item_split[1].strip())

    # 리그 평균 출루율, oz
    sum = 0
    for i in obp_dic:
        sum += obp_dic[i]
    avg = round(sum / obp_dic.__len__(), 3)
    total_league_obp = avg
    total_league_obp_oz = total_league_obp / (1 - total_league_obp)


    def versus(self, obp_dic, total_league_obp_oz):
        hitter_data = db.kbo_batter_stat.find({'year': 2018, 'team': 'SK', 'name': '로맥'})
        pitcher_data = db.kbo_pitcher_stat.find({'year': 2018, 'team': 'SK', 'name': '김광현'})
        hitter = []
        pitcher = []
        for item in hitter_data:
            hitter.append(item['year'])
            hitter.append(float(item['obp']))
        for item in pitcher_data:
            pitcher.append(item['year'])
            pitcher.append(float(item['obp']))
        hitter_year = hitter[0] - 2000
        pitcher_year = pitcher[0] - 2000
        batter_obp = hitter[1]
        pitcher_obp = pitcher[1]
        batter_league_obp = obp_dic[str(hitter_year)]
        pitcher_league_obp = obp_dic[str(pitcher_year)]

        batter_oz = batter_obp / (1 - batter_obp)
        pitcher_oz = (1 - pitcher_obp) / pitcher_obp
        batter_league_obp_oz = batter_league_obp / (1 - batter_league_obp)
        pitcher_league_obp_oz = (1 - pitcher_league_obp) / pitcher_league_obp
        vs = ((batter_oz / batter_league_obp_oz) / (pitcher_oz / pitcher_league_obp_oz)) * total_league_obp_oz
        vs_obp = round(vs / (1 + vs), 3)

        # print('타자 vs 투수 출루율 : ', vs_obp)
        hit_or_out = ['출루', '아웃']
        hit_rate = [vs_obp, 1 - vs_obp]

        result = choices(hit_or_out, hit_rate)
        # print(result)

        if result[0] == '출루':
            return False
        else:
            return True


    def hit_result(self):
        hitter_data = db.kbo_batter_stat.find({'year': 2018, 'team': 'SK', 'name': '로맥'})
        hitter = []
        for item in hitter_data:
            hitter.append(item['total_hit'])
            hitter.append(item['one_hit'])
            hitter.append(item['double_hit'])
            hitter.append(item['triple_hit'])
            hitter.append(item['home_run'])
            hitter.append(item['BB'])
        total_hit = int(hitter[0])
        hit_one = int(hitter[1])
        hit_two = int(hitter[2])
        hit_three = int(hitter[3])
        home_run = int(hitter[4])
        BB = int(hitter[5])
        hit = total_hit + BB

        hit_kind = ['안타', '2루타', '3루타', '홈런', '볼넷']
        run_rate = [hit_one / hit, hit_two / hit, hit_three / hit, home_run / hit, BB / hit]

        hit_def = choices(hit_kind, run_rate)
        # print(hit_def)
        return hit_def

    def out_result(self):
        out_kind = ['삼진아웃', '땅볼아웃', '뜬공아웃']
        out_rate = [0.33333334, 0.33333333, 0.3333333]

        out_def = choices(out_kind, out_rate)
        # print(out_def)
        return out_def

    def pitch_count(self):      # 투구 수 결과 (투구 수 1 ~ 10개 중 출력)
        pitch_count_kind = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        count_rate = [0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.07, 0.07, 0.07, 0.07]
        pitch_count_def = choices(pitch_count_kind, count_rate)
        pitch_count = int(pitch_count_def[0])
        # print('투구 수 : ', pitch_count)

        return pitch_count

    def pitch_count_case_BB(self):  # 볼넷일 시 투구수 결과 (투구 수 3 ~ 10개 중 출력)

        pitch_count_kind = [4, 5, 6, 7, 8, 9, 10]
        hit_count_rate = [0.16, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14]
        pitch_count_def = choices(pitch_count_kind, hit_count_rate)
        pitch_count = int(pitch_count_def[0])
        # print('투구 수 : ', pitch_count)

        return pitch_count

    def pitch_count_case_K(self):  # 삼진일 시 투구수 결과 (투구 수 3 ~ 10개 중 출력)

        pitch_count_kind = [3, 4, 5, 6, 7, 8, 9, 10]
        hit_count_rate = [0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125]
        pitch_count_def = choices(pitch_count_kind, hit_count_rate)
        pitch_count = int(pitch_count_def[0])
        # print('투구 수 : ', pitch_count)

        return pitch_count

    def h_vs_p(self):   # 타 vs 투
        if Versus.versus(0, Versus.obp_dic, Versus.total_league_obp_oz) == True:
            result = Versus.out_result(0)[0]
            if result == '삼진':
                ball_count = Versus.pitch_count_case_K(0)
            else:
                ball_count = Versus.pitch_count(0)
        else:
            result = Versus.hit_result(0)[0]
            if result == '볼넷':
                ball_count = Versus.pitch_count_case_BB(0)
            else:
                ball_count = Versus.pitch_count(0)
        # print(result, ', 투구 수 : ', ball_count)
        return result, ball_count