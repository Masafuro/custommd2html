# custommd2html

## gpt4aによる利用例

```md
まずマークダウンで下書きを作成したいと思います。次のカスタム記法を使って、PLCからのセンサーデータを表示するUI案を作成してください。また、クラスについてはBULMAを用いるように考えてください。

カスタム記法
- タグ名{ .クラス名 #id名} 要素の内容

またリストの階層で、要素の階層構造を表現してください。

カスタム記法の例
- section { .section }
    - div { .container}
        - h1 { .title } タイトル
        - p { .paragraph } こんにちは
```


## 内容

所定の.mdファイルからhtmlを生成します。
記法は次の通りです。

> - タグ名 { .クラス名 #id名 } 内容

また、箇条書きの入れ子構造が継承されます。

> python cmd2html.py
を実行してください。

## 例

```md
# title
「-」の箇条書きリスト以外は無視されます。

- section {.class #id}
  - div {.class1 .class2 #id}
    - p {.class #id} 内容

```

