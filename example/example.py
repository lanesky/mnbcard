#! /usr/bin/env python3

import logging
import sys
sys.path.append('./../mnbcard')

from reader import get_reader, connect_card
from api import *
from helper import *


root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)

reader = get_reader()
connection = connect_card(reader)

sig_pin = input("Please input the signature PIN: ")
auth_pin = input("Please input the authentication PIN: ")

card = Card(connection)

save_to_file(filename ="Auth_Cert.der", data = card.get_cert_for_auth())
save_to_file(filename ="ca.der", data = card.get_ca_for_auth())
save_to_file(filename ="SigCert.der", data = card.get_cert_for_sign( sig_pin))
save_to_file(filename ="Sign_CA.der", data = card.get_ca_for_sign( sig_pin))

print(card.get_my_number(auth_pin))
for iter in card.get_basic_info( auth_pin):
    print(iter)

save_to_file(filename ="testfile.file.sig", data = card.sign_file_with_sign_key(sig_pin, "testfile.txt") )
save_to_file(filename ="testfile.auth.sig", data = card.sign_file_with_auth_key(auth_pin, "testfile.txt"))