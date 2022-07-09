#! /usr/bin/env python3

import logging
import sys
sys.path.append('./../mnbcard')

from reader import get_reader, connect_card
from api import *
from helper import *

# ログレベルを設定する
root = logging.getLogger()
root.setLevel(logging.DEBUG)

# ログをコンソールに出力
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)

# カードリーダー取得
reader = get_reader()
# カードに接続する
connection = connect_card(reader)

# 署名PIN入力（署名秘密鍵による署名をする場合は必要）
sig_pin = input("Please input the signature PIN: ")
# 認証PIN入力（券面情報読み取り、または認証秘密鍵による署名をする場合は必要）
auth_pin = input("Please input the authentication PIN: ")

# カードインスタンス作成
card = Card(connection)

# 認証用証明書取得
save_to_file(filename ="Auth_Cert.der", data = card.get_cert_for_auth())
# 認証用証明書CA取得
save_to_file(filename ="ca.der", data = card.get_ca_for_auth())
# 署名用証明書取得(署名PIN必要)
save_to_file(filename ="SigCert.der", data = card.get_cert_for_sign( sig_pin))
# 署名用証明書CA取得(署名PIN必要)
save_to_file(filename ="Sign_CA.der", data = card.get_ca_for_sign( sig_pin))

# 個人番号取得(認証PIN必要)
print(card.get_my_number(auth_pin))
# 基本４情報取得(認証PIN必要)
for iter in card.get_basic_info( auth_pin):
    print(iter)

# 署名秘密鍵によるファイル署名(署名PIN必要)
save_to_file(filename ="testfile.file.sig", data = card.sign_file_with_sign_key(sig_pin, "testfile.txt") )
# 認証秘密鍵によるファイル署名(認証PIN必要)
save_to_file(filename ="testfile.auth.sig", data = card.sign_file_with_auth_key(auth_pin, "testfile.txt"))