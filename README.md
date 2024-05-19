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

## 実行環境

- Python 3.8.5 以上

## 必要なライブラー

- [pyscard](https://pyscard.sourceforge.io/)

## 使用例

- 詳しくは `example/example.py` を参照。

```
python example.py

```

RESULTS:

```
Please input the signature PIN: (******)
Please input the profile PIN:  (****)
Please input the authentication PIN:  (****)
2022-07-09 12:46:23,258 - api - INFO - 認証用証明書: 90 0
2022-07-09 12:46:24,961 - api - INFO - 認証用証明書CA: 90 0
2022-07-09 12:46:26,432 - api - INFO - SELECT 署名用PIN: 90 0
2022-07-09 12:46:26,497 - api - INFO - VERIFY 署名用PIN: 90 0
2022-07-09 12:46:26,543 - api - INFO - 認証用証明書: 90 0
2022-07-09 12:46:28,437 - api - INFO - SELECT 署名用PIN: 90 0
2022-07-09 12:46:28,502 - api - INFO - VERIFY 署名用PIN: 90 0
2022-07-09 12:46:28,547 - api - INFO - 署名用証明書CA: 90 0
2022-07-09 12:46:29,968 - api - INFO - 券面入力補助AP: 90 0
2022-07-09 12:46:30,000 - api - INFO - SELECT 券面入力補助用PIN: 90 0
2022-07-09 12:46:30,057 - api - INFO - VERIFY 券面入力補助用PIN: 90 0
2022-07-09 12:46:30,103 - api - INFO - マイナンバー: 90 0
（***個人番号 ***）
2022-07-09 12:46:30,233 - api - INFO - 券面入力補助AP: 90 0
2022-07-09 12:46:30,278 - api - INFO - SELECT 券面入力補助用PIN: 90 0
2022-07-09 12:46:30,335 - api - INFO - VERIFY 券面入力補助用PIN: 90 0
2022-07-09 12:46:30,369 - api - INFO - 基本4情報: 90 0
（***名前 ***）
（***住所 ***）
（***生年月日 ***）
（***性別 ***）
2022-07-09 12:46:30,710 - api - INFO - SELECT 署名用PIN: 90 0
2022-07-09 12:46:30,773 - api - INFO - VERIFY 署名用PIN: 90 0
2022-07-09 12:46:30,818 - api - INFO - SELECT 署名用秘密鍵: 90 0
2022-07-09 12:46:31,535 - api - INFO - COMPUTE DIGITAL SIGNATURE: 90 0
2022-07-09 12:46:31,668 - api - INFO - SELECT 認証用PIN: 90 0
2022-07-09 12:46:31,730 - api - INFO - VERIFY 認証用PIN: 90 0
2022-07-09 12:46:31,775 - api - INFO - SELECT 認証用秘密鍵: 90 0
2022-07-09 12:46:32,482 - api - INFO - COMPUTE DIGITAL SIGNATURE: 90 0

```

## OpenSSL による署名検証

- 検証方法は `example/verify.sh` を参照。

## 注意点

### 基本４情報の「性別」

性別は１桁の数字で出力する。

- 1: 男
- 2: 女
- 3: その他

### 例外処理

APDU 送信して結果が成功しない場合、exception はスローされる。

### ディジタル署名

署名アルゴリズムは、SHA256 のみを使用する。

### 対応 OS

- Windowsx
- MacOS
- Linux

### テスト済の OS、カード

現時点、以下の組み合わせではテスト済。

- OS: MacOS, Card Reader: I-O DATA USB-NFC3

## Card クラスのAPI仕様

### Initialization
#### Class: `Card`
- **Constructor Parameters**:
  - `connection`: A connection object to communicate with the card.
  - `log_level`: (Optional) Logging level (e.g., `logging.DEBUG`).

### Methods

#### Select File PKI AP
- **Method**: `select_file_pki_ap()`
- **Description**: Selects the PKI authentication applet.
- **Parameters**: None
- **Returns**: None
- **Raises**: Exception if an error occurs.

#### Select File Certificate for Authentication
- **Method**: `select_file_cert_for_auth()`
- **Description**: Selects the file for the authentication certificate.
- **Parameters**: None
- **Returns**: None
- **Raises**: Exception if an error occurs.

#### Select File CA for Authentication
- **Method**: `select_file_ca_for_auth()`
- **Description**: Selects the file for the authentication certificate CA.
- **Parameters**: None
- **Returns**: None
- **Raises**: Exception if an error occurs.

#### Select File Authentication PIN
- **Method**: `select_file_auth_pin()`
- **Description**: Selects the file for the authentication PIN.
- **Parameters**: None
- **Returns**: None
- **Raises**: Exception if an error occurs.

#### Verify Authentication PIN
- **Method**: `verify_auth_pin(pin_bytes)`
- **Description**: Verifies the authentication PIN.
- **Parameters**:
  - `pin_bytes`: List of bytes representing the PIN.
- **Returns**: None
- **Raises**: Exception if an error occurs.

#### Select File Authentication Private Key
- **Method**: `select_file_auth_private_key()`
- **Description**: Selects the file for the authentication private key.
- **Parameters**: None
- **Returns**: None
- **Raises**: Exception if an error occurs.

#### Select File Certificate for Signature
- **Method**: `select_file_cert_for_signature()`
- **Description**: Selects the file for the signature certificate.
- **Parameters**: None
- **Returns**: None
- **Raises**: Exception if an error occurs.

#### Select File CA for Signature
- **Method**: `select_file_ca_for_signature()`
- **Description**: Selects the file for the signature certificate CA.
- **Parameters**: None
- **Returns**: None
- **Raises**: Exception if an error occurs.

#### Select File Signature PIN
- **Method**: `select_file_signature_pin()`
- **Description**: Selects the file for the signature PIN.
- **Parameters**: None
- **Returns**: None
- **Raises**: Exception if an error occurs.

#### Verify Signature PIN
- **Method**: `verify_signature_pin(pin_bytes)`
- **Description**: Verifies the signature PIN.
- **Parameters**:
  - `pin_bytes`: List of bytes representing the PIN.
- **Returns**: None
- **Raises**: Exception if an error occurs.

#### Select File Signature Private Key
- **Method**: `select_file_signature_private_key()`
- **Description**: Selects the file for the signature private key.
- **Parameters**: None
- **Returns**: None
- **Raises**: Exception if an error occurs.

#### Select File Profile AP
- **Method**: `select_file_profile_ap()`
- **Description**: Selects the file for the profile AP.
- **Parameters**: None
- **Returns**: None
- **Raises**: Exception if an error occurs.

#### Select File Profile PIN
- **Method**: `select_file_profile_pin()`
- **Description**: Selects the file for the profile PIN.
- **Parameters**: None
- **Returns**: None
- **Raises**: Exception if an error occurs.

#### Verify Profile PIN
- **Method**: `verify_profile_pin(pin_bytes)`
- **Description**: Verifies the profile PIN.
- **Parameters**:
  - `pin_bytes`: List of bytes representing the PIN.
- **Returns**: None
- **Raises**: Exception if an error occurs.

#### Select File My Number
- **Method**: `select_file_my_number()`
- **Description**: Selects the file for the My Number (personal number).
- **Parameters**: None
- **Returns**: None
- **Raises**: Exception if an error occurs.

#### Select File Basic 4 Info
- **Method**: `select_file_base_4_info()`
- **Description**: Selects the file for the basic 4 information.
- **Parameters**: None
- **Returns**: None
- **Raises**: Exception if an error occurs.

#### Read Binary Certificate
- **Method**: `read_binary_cert()`
- **Description**: Reads the binary certificate.
- **Parameters**: None
- **Returns**: Certificate data in DER format.
- **Raises**: Exception if an error occurs.

#### Read Binary 256 Bytes
- **Method**: `read_binary_256()`
- **Description**: Reads 256 bytes of binary data.
- **Parameters**: None
- **Returns**: 256 bytes of data.
- **Raises**: Exception if an error occurs.

#### Compute Digital Signature
- **Method**: `compute_digital_signature(hash)`
- **Description**: Computes the digital signature.
- **Parameters**:
  - `hash`: Hash to be signed.
- **Returns**: Signature data.
- **Raises**: Exception if an error occurs.

#### Get Certificate for Authentication
- **Method**: `get_cert_for_auth()`
- **Description**: Retrieves the authentication certificate.
- **Parameters**: None
- **Returns**: Authentication certificate in DER format.
- **Raises**: Exception if an error occurs.

#### Get CA for Authentication
- **Method**: `get_ca_for_auth()`
- **Description**: Retrieves the CA for authentication.
- **Parameters**: None
- **Returns**: CA certificate in DER format.
- **Raises**: Exception if an error occurs.

#### Get Certificate for Signature
- **Method**: `get_cert_for_sign(sig_pin)`
- **Description**: Retrieves the signature certificate.
- **Parameters**:
  - `sig_pin`: Signature PIN.
- **Returns**: Signature certificate in DER format.
- **Raises**: Exception if an error occurs.

#### Get CA for Signature
- **Method**: `get_ca_for_sign(sig_pin)`
- **Description**: Retrieves the CA for signature.
- **Parameters**:
  - `sig_pin`: Signature PIN.
- **Returns**: CA certificate in DER format.
- **Raises**: Exception if an error occurs.

#### Get My Number
- **Method**: `get_my_number(auth_pin)`
- **Description**: Retrieves the My Number (personal number).
- **Parameters**:
  - `auth_pin`: Authentication PIN.
- **Returns**: My Number (personal number).
- **Raises**: Exception if an error occurs.

#### Get Basic Info
- **Method**: `get_basic_info(auth_pin)`
- **Description**: Retrieves the basic 4 information (name, address, birthdate, gender).
- **Parameters**:
  - `auth_pin`: Authentication PIN.
- **Returns**: Tuple (name, address, birthdate, gender).
- **Raises**: Exception if an error occurs.

#### Sign File with Signature Key
- **Method**: `sign_file_with_sign_key(sig_pin, filename)`
- **Description**: Signs a file using the signature key.
- **Parameters**:
  - `sig_pin`: Signature PIN.
  - `filename`: Name of the file to be signed.
- **Returns**: Signature data.
- **Raises**: Exception if an error occurs.

#### Sign File with Authentication Key
- **Method**: `sign_file_with_auth_key(auth_pin, filename)`
- **Description**: Signs a file using the authentication key.
- **Parameters**:
  - `auth_pin`: Authentication PIN.
  - `filename`: Name of the file to be signed.
- **Returns**: Signature data.
- **Raises**: Exception if an error occurs.


