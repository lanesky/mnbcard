            ___  ___ _   _ ______  _____               _
            |  \/  || \ | || ___ \/  __ \             | |
            | .  . ||  \| || |_/ /| /  \/ __ _ _ __ __| |
            | |\/| || . ` || ___ \| |    / _` | '__/ _` |
            | |  | || |\  || |_/ /| \__/\ (_| | | | (_| |
            \_|  |_/\_| \_/\____/  \____/\__,_|_|  \__,_|

# mnbcard - マイナンバーカード PYTHON Lib

## できること

- 券面確認 AP・券面入力補助 AP の読み取り
  - 4 属性の取得（名前、住所、生年月日、性別）
  - 個人番号の取得
- 公的個人認証の各種証明書の読み取り
  - 認証用証明書の取得
  - 認証用証明書 CA の取得
  - 認証用証明書の取得
  - 署名用証明書 CA の取得
- 公的個人認証の署名
  - 認証用秘密鍵による署名
  - 署名用秘密鍵による署名

## インストール

- Install [pyscard](http://pyscard.sourceforge.net/) python library

## 使用例

- 詳しくは `example/example.py` を参照。

## OpenSSL による署名検証

- 詳しくは `example/verify.sh` を参照。
