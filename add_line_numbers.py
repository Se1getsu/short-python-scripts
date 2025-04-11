# 【内容】
# クリップボードにコピーされているプログラムに行番号を付加します。

import pyperclip

program = pyperclip.paste()

program = '\n'.join(f"{i+1} {line}" for i, line in enumerate(program.split('\n')))

pyperclip.copy(program)
