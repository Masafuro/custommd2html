# custommd2html

所定の.mdファイルからhtmlを生成します。
記法は次の通りです。

> - タグ名 : { .クラス名 #id名 } 内容

また、箇条書きの入れ子構造が継承されます。

> python cmd2html.py
を実行してください。

## 例

```md
# title
「-」の箇条書きリスト以外は無視されます。

- section : {.class #id}
  - div : {.class1 .class2 #id}
    - p : {.class #id} 内容

```

