# 【内容】
# CSV 形式の問題集からランダムに問題を出題し、暗記を助けるプログラム
#
# 【使用例】
# ```
# $ python anki.py words.csv
# ----------------------------------------
# 進捗: 0 / 466 (0.0% 完了)
#
# Q. interpolate
# q:Quit 他:答えを見る>
#
# A. 補間する
# o:OK 他:NG> o
#
# ----------------------------------------
# 進捗: 1 / 466 (0.2% 完了)
#
# Q. polynomial
# q:Quit 他:答えを見る>
# ```
# - もう覚えたと思ったら o を入力, そうでない場合は単に Enter を押します。
# - `*_進捗.csv` が生成され、まだ覚えてない問題が保存されます。
# - `*_進捗.csv` を削除すれば、進捗をリセットできます。
# - 出題は完全ランダムです。さっき出たばかりの問題が出たら Enter を 2 回叩いて素早く飛ばしましょう。

import csv
import os
import random
import sys

# 問題と答えが何列目にあるか
QUESTION_COLUMN = 1
ANSWER_COLUMN = 2
# OK の時に入力する文字
OK = 'o'
# 灰色 (ANSI エスケープシーケンス)
WEAK = "\033[90m"
# 文字色リセット (ANSI エスケープシーケンス)
R = "\033[0m"

# CSV ファイルを読み取って 2 次元リストに変換する
def read_csv(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = [row for row in reader]
        return rows[0], rows[1:]

# 2 次元リストを CSV ファイルに書き込む
def write_csv(file_path, header, data):
    with open(file_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows([header] + data)

# ファイルが存在するか確認する
def exists(file_path):
    return os.path.exists(file_path)

# ファイルを削除する
def remove(file_path):
    os.remove(file_path)

# 水平線を灰色で表示する
def print_hr():
    print(WEAK + '-' * 40 + R)

if __name__ == '__main__':
    # コマンドライン引数を確認
    if len(sys.argv) != 2:
        print("Usage: python a.py <暗記するCSVファイル>")
        sys.exit(1)

    # コマンドライン引数を取得
    target_file = sys.argv[1]
    if not exists(target_file):
        print(f"{target_file} が見つかりません")
        sys.exit(1)
    if not target_file.endswith('.csv'):
        print("CSV ファイルを指定してください")
        sys.exit(1)

    # ターゲットファイルをロード
    header, target_data = read_csv(target_file)

    # 暗記の進捗ファイルを作成
    anki_file = target_file[:-len(".csv")] + '_進捗.csv'
    if not exists(anki_file):
        write_csv(anki_file, header, target_data)

    # 暗記の進捗ファイルをロード
    _, anki_data = read_csv(anki_file)

    while anki_data:
        # 次に暗記する問題をランダムに選択
        index = random.randint(0, len(anki_data) - 1)
        question = anki_data[index][QUESTION_COLUMN - 1]
        answer = anki_data[index][ANSWER_COLUMN - 1]

        # 進捗を表示
        print_hr()
        progress = (len(target_data) - len(anki_data)) / len(target_data) * 100
        print(WEAK + f'進捗: {len(target_data) - len(anki_data)} / {len(target_data)} ({progress:.1f}% 完了)' + R)

        # 問題を表示
        print(WEAK + "\nQ. " + R + question)
        if input(WEAK + "q:Quit 他:答えを見る> " + R) == 'q':
            break

        # 答えを表示
        print(WEAK + "\nA. " + R + answer)
        if input(WEAK + OK + ":OK 他:NG> " + R) == OK:
            # OK なら進捗ファイルから削除
            anki_data.pop(index)
            write_csv(anki_file, header, anki_data)
        print()

    else:
        # 進捗を表示
        print_hr()
        print(WEAK + "進捗 100% お疲れ様でした！" + R)

        # 進捗ファイルを削除
        remove(anki_file)
