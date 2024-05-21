# custommd2html

所定の.mdファイルからhtmlを生成します。
記法は次の通りです。

```md
# title

「-」の箇条書きリスト以外は無視されます。

- section : {.class #id}
  - div : {.class1 .class2 #id}
    - p : {.class #id} 内容

```

