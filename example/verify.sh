# Signed with authentication
openssl x509 -in Auth_Cert.der -inform der -out Auth_Cert.pem -outform pem
openssl x509 -pubkey -noout -in Auth_Cert.pem -out Auth_Pub.pem
openssl dgst -verify Auth_Pub.pem -signature testfile.auth.sig testfile.txt

# Signed with signature
openssl x509 -in SigCert.der -inform der -out SigCert.pem -outform pem
openssl x509 -pubkey -noout -in SigCert.pem -out SigPub.pem
openssl dgst -verify SigPub.pem -signature testfile.file.sig testfile.txt
