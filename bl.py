# 【内容】
# 部員の名札の印刷の際に、紙をできるだけ無駄にしない印刷方法を
# 長方形詰め込み問題として解くプログラム。

from libs.bl import Rect, put_rect
from PIL import Image, ImageDraw
import subprocess
import sys

# input
_印刷物の横幅 = 87.5
_印刷物の縦幅 = 54
_紙のサイズ名 = "A4"

# カスタムサイズ - サイズ名を"C"にして使用
_紙の横幅 = 280
_紙の縦幅 = 510


def calc(paper_x, paper_y, w, h):
    min_n = max(
        int(paper_x // w) * int(paper_y // h),
        int(paper_x // h) * int(paper_y // w)
    ) - 1
    max_n = int((paper_x * paper_y) // (w * h))

    last_discovered_result = []
    for n in range(min_n, max_n + 1):
        print(f"--- [n = {n}] ---")
        count = 0
        for i in range(n+1):
            img_list = [(w, h)] * i + [(h, w)] * (n-i)
            rects, _ = put_rect(img_list, roomsORIG=[Rect(0,0,paper_x,paper_y)])
            if len(rects) == n:
                count += 1
                last_discovered_result = rects
                for rect in rects: print(rect)
                print()
                save_result_image(paper_x, paper_y, last_discovered_result, f"{n}-{count}")
        if count:
            remove_result_images(f"{n-1}-*")
        else:
            print("No result\n")
            return n - 1, last_discovered_result
    else:
        print(f"--- [n = {n}] ---")
        print("fill rate > 100%\n")
        return n - 1, last_discovered_result


def save_result_image(paper_x, paper_y, result, suffix=""):
    colors = [
        "red", "green", "blue", "yellow", "purple",
        "orange", "cyan", "magenta", "brown", "pink", "lime", "navy"
    ]

    # 新しい画像を作成
    image = Image.new("RGB", (paper_x, paper_y), "white")
    draw = ImageDraw.Draw(image)

    # 長方形を描画
    for i, rect in enumerate(result):
        x, y, width, height = rect.x1, rect.y1, rect.w, rect.h
        draw.rectangle([x, y, x + width, y + height], fill=colors[i % len(colors)])

    # 保存
    if suffix: suffix = "_" + suffix
    image.save(f"out/bl_result{suffix}.png")


def remove_result_images(suffix=None):
    if suffix: suffix = "_" + suffix
    else: suffix = "*"
    _ = subprocess.run(f"rm out/bl_result{suffix}.png", shell=True)


if __name__ == "__main__":
    # 印刷物のサイズ
    w = _印刷物の横幅
    h = _印刷物の縦幅

    # 紙のサイズ
    size_name = _紙のサイズ名.upper()
    match size_name:
        case "A4":  px, py = 210, 297
        case "B5":  px, py = 182, 257
        case "C":   px, py = _紙の横幅, _紙の縦幅
        case _:     print("Invalid paper size"); sys.exit()
    if size_name == "C":
        size_name = f"CUSTOM {px} x {py}"

    # クリーン
    remove_result_images()

    # 計算実行
    n, result = calc(px, py, w, h)
    rate = 100 * w * h * n / (px * py)

    # 出力
    print("--- RESULT --- ")
    print(f"size: {size_name}")
    print(f"n: {n}")
    print(f"fill rate: {rate:.3f}%")
    print("Saved result images in output/ directory\n")
