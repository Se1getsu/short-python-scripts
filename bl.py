# 【内容】
# 部員の名札の印刷の際に、紙をできるだけ無駄にしない印刷方法を
# 長方形詰め込み問題として解くプログラム。

from libs.bl import Rect, put_rect
from PIL import Image, ImageDraw


def calc(paper_x, paper_y, w, h):
    last_discovered_result = []
    n = 0
    while (n := n + 1):
        print(f"--- [n = {n}] ---")
        retflg = True
        for i in range(n+1):
            img_list = [(w, h)] * i + [(h, w)] * (n-i)
            rects, rooms = put_rect(img_list, roomsORIG=[Rect(0,0,paper_x,paper_y)])
            if len(rects) == n:
                retflg = False
                last_discovered_result = rects
                for rect in rects: print(rect)
                print()
        if retflg:
            print("No result\n")
            return n - 1, last_discovered_result


def show_result_image(paper_x, paper_y, result):
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

    image.save("bl_output.png")
    image.show()


if __name__ == "__main__":
    # 詰め込む印刷物のサイズ
    w = 87.5
    h = 54

    # ↓ここでA4/B4を切り替える
    if 1:
        name = "A4"
        px, py = 210, 297
    else:
        name = "B5"
        px, py = 182, 257

    n, result = calc(px, py, w, h)
    rate = 100 * w * h * n / (px * py)

    print(f"size: {name}")
    print(f"n: {n}")
    print(f"Fill rate: {rate:.3f}%")

    show_result_image(px, py, result)
