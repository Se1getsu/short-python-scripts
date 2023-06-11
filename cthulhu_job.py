# 【内容】
# 高校時代に作った、クトゥルフの職業技能のデータを扱うプログラムです。
# データのソースはこのサイトです。
# https://w.atwiki.jp/a4trpg/pages/21.amp
# 実行すると入力が要求されますが何も入力せずEnterを押します。
# すると、プログラム下の方のpsという変数に設定した、欲しさを表す技能ごとの
# ポイントをもとに、それらの技能を職業技能に持つ職業にポイント加算され、
# 最も高いポイントを得た職業のポイントが表示されます。
# その後表示される「pt>>」に続いて数値を入力すると、そのポイントの職業を列挙
# します。より詳しい仕様はソースを参照してください。

s = """医師
職業技能：医学、応急手当、経理、信用、生物学、説得、薬学、ほかの言語（英語,ラテン語,ドイツ語）

アニマルセラピスト
職業技能：聞き耳、心理学、精神分析、生物学、跳躍、追跡、博物学 
＋１

看護師
職業技能：化学、生物学、応急手当、説得、薬学、心理学、聞き耳、目星

救急救命士
職業技能：医学、応急手当、化学、鍵開け、機械修理、電気修理、登攀

形成外科医
職業技能：医学、応急手当、経理、心理学、説得、値切り、薬学、ほかの言語（英語）

精神科医
職業技能：医学、化学、心理学、精神分析、生物学、説得、薬学、ほかの言語

闇医者
職業技能：医学、応急手当、経理、説得、法律、薬学、ほかの言語 
＋１


エンジニア
職業技能：機械修理、コンピューター、重機械操作、電気修理、図書館、物理学、ほかの言語（英語） 
＋１：化学、地質学、電子工学


狂信者
職業技能：隠す、隠れる、心理学、説得、図書館、ほかの言語（英語,中国語,朝鮮語,ロシア語など） 
＋２：化学、電気修理、法律、薬学、ライフル、ショットガン、スタンガン


警察官
職業技能：説得、聞き耳、心理学、追跡、法律、目星 
＋１：運転（自動車,二輪車）、信用、組みつき、武道（柔道）、日本刀、拳銃、杖

海上保安官
職業技能：機械修理、重機械操作、信用、操縦（船舶）、登攀、ナビゲート、法律、サバイバル（海）

科学捜査研究員
職業技能：医学、化学、コンピューター、写真術、人類学、生物学、法律、薬学

山岳救助隊員
職業技能：応急手当、聞き耳、跳躍、追跡、登攀、ナビゲート、サバイバル（山）、ほかの言語

消防士
職業技能：運転（自動車）、応急手当、回避、機械修理、重機械操作、跳躍、投擲、登攀


芸術家
職業技能：説得、芸術（任意）、コンピューター、写真術、心理学、製作（任意）、目星、歴史

芸術家（基本）
職業技能：説得、芸術（任意）　製作（任意）、心理学、目星、歴史　博物学 
＋３：コンピューター、写真術、生物学、天文学、芸術（任意）　製作（任意）

ダンサー
職業技能：回避、芸術（ダンス）、忍び歩き、跳躍、登攀、目星 
＋２

デザイナー
職業技能：説得、芸術（任意）　製作（任意）、コンピューター、心理学、図書館、目星 
＋２

ファッション系芸術家
職業技能：説得、芸術（任意）　製作（任意）、心理学、値切り、変装、目星 
＋２


古物研究科
職業技能：芸術（任意）、コンピューター、製作（古書修復,古美術修復）、図書館、値切り、ほかの言語（英語,漢文,ラテン語など）、目星、歴史


コンピューター技術者
職業技能：説得、経理、コンピューター、電気修理、電子工学、図書館、物理学、ほかの言語（英語,その他）


作家
職業技能：オカルト、芸術（トリビア知識,詩的表現など）、心理学、説得、図書館、ほかの言語（英語など）、母国語、歴史


自衛官
職業技能：運転（自動車）、応急手当、機械修理、重機械操作、操縦（船舶,潜水艦,戦車,民間プロペラ機,民間ジェット機,定期旅客機,ジェット戦闘機,ヘリコプター）、ナビゲート 
＋２：回避、隠れる、聞き耳、経理、忍び歩き、信用、説得、値切り、法律、ほかの言語（英語など）、こぶし/パンチ、キック、組みつき、武道（任意）、サブマシンガン、ライフル、グレネード・ランチャー、砲、拳銃

陸上自衛隊員
職業技能：応急手当、回避、隠れる、サバイバル（山,砂漠）、任意の近接戦技能、任意の火器技能 
＋２：機械修理、忍び歩き、水泳、登攀、ほかの言語、パラシュート、重機械操作、砲

海上自衛隊員（艦上勤務）
職業技能：応急手当、重機械操作、水泳、操縦（ボート）、ナビゲート、サバイバル（海） 
＋２：機械修理、電気修理、任意の近接戦技能、任意の火器技能、砲

自衛隊パイロット（陸海空）
職業技能：機械修理、重機械操作、操縦（戦闘機,大型機,ヘリコプターなど）、電気修理、天文学、ナビゲート、パラシュート 
＋１

民間軍事会社メンバー
職業技能：回避、隠れる、忍び歩き、水泳　登攀、任意の近接戦技能、任意の火器技能 
＋２：応急手当、機械修理、サバイバル（山,砂漠）、ほかの言語


ジャーナリスト
職業技能：説得、写真術、心理学、図書館、母国語、ほかの言語（英語など）、歴史


宗教家
職業技能：オカルト、聞き耳、経理、心理学、説得、図書館、歴史 
＋１：信用、ほかの言語（漢文,ラテン語など）


商店主／店員
職業技能：説得、聞き耳、経理、心理学、信用、値切り 
＋１：運転（自動車,二輪車）、コンピューター 
＋１


私立探偵
職業技能：説得、鍵開け、心理学、追跡、図書館、法律、目星 
＋１：聞き耳、写真術、値切り、スタンガン


水産業従事者
職業技能：機械修理、重機械操作、水泳、操縦（船舶）、天文学、ナビゲート、博物学、目星


スポーツ選手
職業技能：回避、芸術（任意のスポーツ競技）、跳躍、投擲、登攀 
＋３：応急手当、乗馬、水泳、こぶし/パンチ、キック、組みつき、武道（任意）、日本刀、薙刀、杖、弓、競技用アーチェリー、拳銃、ライフル、ショットガン


大学教授
職業技能：信用、心理学、説得、図書館、値切り、ほかの言語（英語など） 
＋２：医学、化学、考古学、人類学、生物学、地質学、電子工学、天文学、博物学、物理学、法律、歴史

冒険家教授
職業技能：応急手当、説得、跳躍、登攀、図書館、ほかの言語 
＋２：考古学、地質学、歴史など

評論家
職業技能：信用、心理学、説得、図書館、値切り、母国語 
＋２：オカルト、博物学、歴史など


タレント
職業技能：説得、聞き耳、信用、心理学、芸術（何かの音楽演奏,歌唱,ダンス,演技,司会など）、変装、ほかの言語（英語）

アイドル、音楽タレント
職業技能：説得、芸術（歌唱）、芸術（ダンス）、心理学、変装 
＋２

アナウンサー
職業技能：説得、信用、心理学、芸術（アナウンス）、図書館、母国語 
＋１

コメディアン
職業技能：説得、聞き耳、心理学、芸術（物語）、芸術（演劇）、変装 
＋２

スポーツタレント
職業技能：説得、心理学、芸術（演劇）、跳躍　登攀、変装、任意の素手の近接戦技能 
＋２

テレビ・コメンテーター
職業技能：説得、聞き耳、信用、心理学、図書館、値切り 
＋１

俳優
職業技能：説得、運転（自動車）、芸術（演劇）、心理学、変装 
＋２

プロデューサー、マネージャー
職業技能：説得、運転（自動車）、隠れる、聞き耳、忍び歩き、値切り、法律 
＋１


超心理学者
職業技能：オカルト、人類学、写真術、心理学、精神分析、図書館、ほかの言語（英語,ラテン語など）、歴史

ゴーストハンター
職業技能：オカルト、化学、機械修理、写真術、生物学、説得、電気修理、物理学

占い師、スピリチュアリスト、霊媒師
職業技能：説得、オカルト、芸術（演劇）、信用、心理学、値切り 
＋１


ディレッタント
職業技能：運転（自動車）、芸術（音楽,美術,文学,ダンス,何かのスポーツ）、信用、図書館、法律、ほかの言語（英語など） 
＋２：乗馬、写真術、操縦（航空機,船舶）、拳銃、ライフル、ショットガン、武道（任意）


ドライバー
職業技能：運転（自動車,二輪車）、機械修理、聞き耳、重機械操作、電気修理、ナビゲート、値切り、目星


農林業従事者
職業技能：応急手当、機械修理、重機械操作、製作（農作物,畜産,養蜂など）、追跡、電気修理、博物学 
＋１：杖、ライフル、ショットガン、チェーンソー


パイロット
職業技能：機械修理、重機械操作、電気修理、操縦（民間プロペラ機,民間ジェット機,定期旅客機,ジェット戦闘機,ヘリコプター,飛行機）、天文学、ナビゲート、物理学、ほかの言語（英語,その他）


ビジネスマン
職業技能：説得、経理、コンピューター、信用、値切り、法律、ほかの言語（英語,その他ビジネス相手の国の言語）

執事・メイド
職業技能：説得、応急手当、聞き耳、芸術　製作（ワインの鑑定,料理,裁縫,掃除など）、経理、心理学、目星、ほかの言語

セールスマン
職業技能：説得、運転（自動車）、芸術（演劇）、経理、心理学、値切り 
＋１


法律家
職業技能：説得、経理、信用、心理学、図書館、値切り、法律


放浪者
職業技能：説得、隠れる、聞き耳、忍び歩き、心理学、値切り、目星 
＋１：運転（自動車,二輪車）、芸術（ギャンブル）、ほかの言語（英語など）


暴力団組員
職業技能：説得、隠す、芸術（刺青彫り,イカサマ）、心理学、値切り、目星 
＋２：隠れる、こぶし/パンチ、キック、組みつき、武道（任意）、日本刀、ナイフ、拳銃


ミュージシャン
職業技能：説得、聞き耳、芸術（歌唱,何かの音楽演奏）、製作（作詞,作曲）、心理学、値切り、ほかの言語（英語など）


メンタルセラピスト
職業技能：説得、芸術（絵画,音楽演奏,歌唱,アロマなど）、信用、心理学、精神分析、法律、ほかの言語（英語,ドイツ語など）"""
#＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝#

def GetInfo(jst):
    name, sks, *oth = jst.split("\n")
        
    assert sks.startswith("職業技能：")
    sks = sks[5:].split('、')
        
    for st in oth:
        assert st[0] == '＋'
        if len(st) == 2:
            sks += ["自由"] * int(st[1])
        else:
            sks += st[3:].split('、')
            #ｎ個選ぶは考慮しない
        
    for i in range(len(sks)):
        if '（' in sks[i]: sks[i] = sks[i][:sks[i].index('（')]

    return name, set(sks)


s = s.replace(' ', '')

# カテゴリー毎に分ける
JOBS = dict()
ListedS = [ss.split("\n\n") for ss in s.split("\n\n\n")]
del s


# 辞書型に変換
for cate in ListedS:
    
    # 単独ジョブ
    if len(cate) == 1:
        name, sks = GetInfo(cate[0])
        JOBS[name] = sks

    else:
        # カテゴリーを分解
        base_name, base_sks = GetInfo(cate[0])
        JOBS["◆"+base_name] = base_sks

        for jst in cate[1:]:
            name, sks = GetInfo(jst)
            JOBS[name] = base_sks | sks

while True:
    name = input(">> ")
    if name == "": break
    for skill in JOBS[name]: print(skill, end=" ")
    print()


ps = """3　回避　精神分析　目星　聞き耳　自由
2　応急手当　説得　鍵開け　医学　心理学
1　オカルト　図書館"""

want = dict()
for ln in ps.split('\n'):
    pt, *ll = ln.split('　')
    for sk in ll:
        want[sk] = int(pt)

jobpt = dict()
maxpt = 0
for jn in JOBS:
    pt = 0
    for sk in JOBS[jn]:
        if sk in want: pt += want[sk]
        else: pt-=1
    jobpt[jn] = pt
    maxpt = max(pt,maxpt)

print(maxpt)

while True:
    n = int(input("pt>> "))
    for jn in jobpt:
        if n == jobpt[jn]: print(jn)

            
    
























