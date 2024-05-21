# custommd2html

- custommd2htmlは、ChatGPTなどのAIでHTMLを考えてもらうために開発しました。
- 現在ChatGPTなどのAIでは、HTML生成時に文字数が多くなりすぎ、安定したHTMLを出力しにくいです。
- そこでより簡易化したマークダウン記法を用いてChatGPTに考えてもらい、それをHTMLに変換して出力します。
- CSSやJavascriptとシームレスに結合させるため、クラスとIDの記法があります。
- また階層構造を箇条書きリストによって表現しています。
- 2024/05/21現在、Geminiはまだうまく作成できないですが、gpt4oでは比較的うまく動作しそうです。
    - 先にBULMAなど使おうとしているフレームワークのクラスに何がありますか？とか聞いておくとうまくいくかも。


## gpt4oに対するプロンプト例

```md
まずマークダウンでWEBサイトの下書きを作成したいと思います。
次のカスタム記法を使って、PLCからのセンサーデータを表示するUI案を作成してください。
また、クラスについてはBULMAを用いるように考えてください。

カスタム記法
- タグ名{ .クラス名 #id名} 要素の内容

またリストの階層で、要素の階層構造を表現してください。

カスタム記法の例
- section { .section }
    - div { .container}
        - h1 { .title } タイトル
        - p { .paragraph } こんにちは
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
