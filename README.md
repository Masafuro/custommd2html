# custommd2html4gpt

- custommd2html4gptは、ChatGPTなどのAIでHTMLを考えてもらうために開発しました。
- 現在ChatGPTなどのAIでは、HTML生成時に文字数が多くなりすぎ、安定したHTMLを出力しにくいです。
- そこでより簡易化したマークダウン記法を用いてChatGPTに考えてもらい、それをHTMLに変換して出力します。
- CSSやJavascriptとシームレスに結合させるため、クラスとIDの記法があります。
    - type記法を追加しました。 
- また階層構造を箇条書きリストによって表現しています。
- 2024/05/21現在、Geminiはまだうまく作成できないですが、gpt4oでは比較的うまく動作しそうです。
    - 先にBULMAなど使おうとしているフレームワークのクラスに何がありますか？とか聞いておくとうまくいくかも。

## 注意事項
- 現在のバージョンでは、　必ず　{　}　がついている必要があります。
- gpt4oの挙動
    - クラスによっては、　「.」 を忘れる時があるので間違いがあれば、指摘する。
    - クラスがない時、{  } を省略する時があるので指摘する。

## gpt4oに対するプロンプト例

```md
BULMAについて知っていますか？CSSのフレームワークです。知っていれば、まずクラスの一覧を表示してください。
```

```md
まずマークダウンでWEBサイトの下書きを作成したいと思います。マークダウンの内容をコードブロックで表示してください。
次のカスタム記法を使って、PLCからのセンサーデータを表示するUI案を作成してください。
また、クラスについてはBULMAを用いるように考えてください。

カスタム記法
- タグ名{ .クラス名 #id名} 要素の内容

またリストの階層で、要素の階層構造を表現してください。

以下はカスタム記法の例です。
- section { .section }
    - div { .container #id }
        - h1 { .title } タイトル
        - p { .paragraph #id } こんにちは
        - input { _type } 入力
        - a { } 
```


## プログラムの内容

所定の.mdファイルからhtmlを生成します。
記法は次の通りです。

> - タグ名 { .クラス名 #id名 } 内容

また、箇条書きの入れ子構造が継承されます。

> python cmd2html.py
を実行してください。

## マークダウンファイルの例

```md
# title
「-」の箇条書きリスト以外は無視されます。

- section {.class #id}
  - div {.class1 .class2 #id}
    - p {.class #id} 内容
　　- input { _type } 

```

## 全体テンプレートと使い方

1. template.htmlを参照してください。
2. 全体のテンプレートを指定します。カスタム記法の.mdファイルはHTMLに変換されてbodyの間に挿入されます。

```python

if __name__ == '__main__':
    import_file_path = 'gpt4o2.md'
    template_path = 'template.html'
    export_file_name = 'export.html'

    main(import_file_path, template_path, export_file_name)

```
