import sys
import re
from bs4 import BeautifulSoup


def insert_content_into_template(template_path, content):
    """指定されたテンプレートHTMLファイルにコンテンツを挿入する"""
    try:
        # テンプレートファイルを読み込む
        with open(template_path, 'r', encoding='utf-8') as file:
            template_html = file.read()
        
        # <body> タグの中にコンテンツを挿入する
        # 正規表現を使用して <body> と </body> タグ間の内容を置換
        updated_html = re.sub(
            r'(<body[^>]*>)(.*?)(</body>)', 
            f'\\1{content}\\3', 
            template_html, 
            flags=re.DOTALL
        )
        return updated_html
    except FileNotFoundError:
        print("指定されたファイルが見つかりません。")
    except Exception as e:
        print(f"エラーが発生しました: {e}")

def process_deepest_html(content):
    lines = content.strip().split('\n')
    # HTMLタグを含まない行を対象として、最大のインデントレベルを見つける
    max_indent = max(
        int(line.split()[0])
        for line in lines
        if line.strip() and not line.strip().startswith('<')
    )

    # 最大インデントの要素を処理し、終了タグの適切な位置を見つける
    processed_lines = []
    open_tag = None
    end_tag_inserted = False
    for i, line in enumerate(lines):
        if line.strip():  # 空行無視
            if line.strip().startswith('<'):
                processed_lines.append(line)
                continue

            indent = int(line.split()[0])
            if indent == max_indent:
                if open_tag and not end_tag_inserted:
                    # 前のタグを閉じる
                    processed_lines.append(f'</{open_tag}>')
                    end_tag_inserted = True

                # 新しいタグを処理
                tag, rest = line.split()[1], line.split('{', 1)[1]
                attrs, text = rest.split('}', 1)
                classes = ' '.join(a[1:] for a in attrs.split() if a.startswith('.'))
                ids = ' '.join(a[1:] for a in attrs.split() if a.startswith('#'))
                class_attr = f' class="{classes}"' if classes else ''
                id_attr = f' id="{ids}"' if ids else ''
                open_tag = tag
                html_line = f'<{tag}{class_attr}{id_attr}>{text.strip()}'
                processed_lines.append(html_line)
                end_tag_inserted = False
            else:
                if open_tag and not end_tag_inserted:
                    # 非HTMLタグの行で閉じタグを挿入
                    processed_lines.append(f'</{open_tag}>')
                    end_tag_inserted = True
                processed_lines.append(line)

    # 最後の開いたタグを閉じる
    if open_tag and not end_tag_inserted:
        processed_lines.append(f'</{open_tag}>')

    return '\n'.join(processed_lines), max_indent




def convert_to_html(lines):
    # 各行を処理するために分割
    lines = lines.split('\n')
    # 最も深いインデントレベルを探す
    max_indent = max(int(line.split()[0]) for line in lines if line.strip())

    # 最も深いインデントレベルの行だけをHTMLに変換
    for i, line in enumerate(lines):
        if line.strip():  # 空行を無視
            indent, content = line.split(maxsplit=1)
            indent = int(indent)

            if indent == max_indent:
                # タグと属性を解析
                parts = content.split(' ', 1)
                tag = parts[0]
                if len(parts) > 1:
                    rest = parts[1]
                    attrs, text = parse_attributes(rest)
                else:
                    attrs = ''
                    text = ''

                # HTMLに変換
                html = f'<{tag} {attrs}>{text}</{tag}>'
                lines[i] = html  # 変換したHTMLで元の行を置き換える

    return '\n'.join(lines)

def parse_attributes(rest):
    if '{' in rest:
        before_brace, after_brace = rest.split('{', 1)
        attrs_content, text = after_brace.split('}', 1)
        attrs_list = attrs_content.split()
        classes = ' '.join(attr[1:] for attr in attrs_list if attr.startswith('.'))
        ids = ' '.join(attr[1:] for attr in attrs_list if attr.startswith('#'))
        attrs = f'class="{classes}"' if classes else ''
        attrs += (' ' if classes and ids else '') + (f'id="{ids}"' if ids else '')
        return attrs, text.strip()
    return '', rest



def convert_nesting_to_numbers(filtered_content):
    """Markdownの入れ子構造を数字に変換し、先頭のタブを削除"""
    converted_lines = []
    lines = filtered_content.splitlines()
    
    for line in lines:
        # 先頭のスペースを数えて、インデントレベルを計算 (2スペース = 1レベル)
        indent_level = (len(line) - len(line.lstrip(' '))) // 2
        
        # 入れ子の深さ（数字）とともに行を再構成
        new_line = f"{indent_level} {line.lstrip('- ').strip()}"
        converted_lines.append(new_line)
    
    return '\n'.join(converted_lines)


def filter_markdown_lines(markdown_content):
    """Markdown内容から先頭に - を含む行だけを抽出して返す"""
    filtered_lines = []
    lines = markdown_content.splitlines()
    
    for line in lines:
        if line.strip().startswith('-'):
            filtered_lines.append(line)
    
    return '\n'.join(filtered_lines)

def read_markdown_file(file_path):
    """指定されたファイルパスからMarkdownファイルを読み込み、その内容を返す"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print("ファイルが見つかりません。")
        return None
    except Exception as e:
        print(f"ファイルの読み込み中にエラーが発生しました: {e}")
        return None

def generate_html(file_path):
        # ファイル読み込み
    markdown_content = read_markdown_file(file_path)
    if markdown_content:
        # print(markdown_content)  # ファイルの内容を表示
        filtered_md = filter_markdown_lines(markdown_content)
        converted_content = convert_nesting_to_numbers(filtered_md)
        converted_html = convert_to_html(converted_content)
        level = 99
        while level!=0:
            converted_html,level = process_deepest_html(converted_html)
        
        return converted_html
    else:
        print("Markdownファイルの読み込みに失敗しました。")
        return False

def prettify_html(html_string, file_name):
    # BeautifulSoupオブジェクトを作成
    soup = BeautifulSoup(html_string, 'html.parser')
    pretty_html = soup.prettify()
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(pretty_html)

def main(import_file_path, template_path, export_file_name):
    print("START cunstom .md convert to html")
    generated_html = generate_html(import_file_path)
    export_html = insert_content_into_template(template_path, generated_html)
    prettify_html(export_html, export_file_name)
    print("FINISH.")
    

if __name__ == '__main__':
    import_file_path = 'test1.md'
    template_path = 'template.html'
    export_file_name = 'export.html'

    main(import_file_path, template_path, export_file_name)

