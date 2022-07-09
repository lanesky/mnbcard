# APDU Commands
class APDU_CMD:
    SELECT = 0xA4
    READ_BINARY =  0xB0
    VERIFY = 0x20
    COMPUTE_SIGNATURE = 0x2A

# APDU Return Status Codes
class APDU_STATUS:
    SUCCESS = 0x90

# Known Applet Identification Numbers
class APPLET:
    # 公的個人認証AP
    PKI_AUTH =[0xD3, 0x92, 0xF0, 0x00, 0x26, 0x01, 0x00, 0x00, 0x00, 0x01]
    # 券面入力補助AP
    PROFILE = [0xD3, 0x92, 0x10, 0x00, 0x31, 0x00, 0x01, 0x01, 0x04, 0x08]

# Known EF/IEF Identification Numbers
class EF:
    # 認証用証明書
    AUTH_CERT = [0x00, 0x0A]   
    # 認証用証明書CA
    AUTH_CERT_CA =[0x00, 0x0B]
    # 認証用PIN
    AUTH_PIN = [0x00, 0x18]
    # 認証用秘密鍵
    AUTH_SECRET =[0x00, 0x17]
    # 署名用証明書
    SIGN_CERT = [0x00, 0x01]
    # 署名用証明書CA
    SIGN_CERT_CA =[0x00, 0x02]
    # 署名用PIN
    SIGN_PIN = [0x00, 0x1B]
    # 認証用秘密鍵
    SIGN_SECRET = [0x00, 0x1A]
    # 券面入力補助用PIN
    PROFILE_PIN = [0x00, 0x11]
    # マイナンバー
    MY_NUMBER = [0x00, 0x01]
    # 基本4情報
    BASE_FOUR = [0x00, 0x02]

# Base four profile manifest definitons
class BASE_FOUR_MANIFEST:
    NAME_SEGMENT_START          = 9
    ADDRESS_SEGMENT_START       = 11
    BIRTHDATE_SEGMENT_START     = 13
    GENDER_SEGMENT_START        = 15

# Digest info related
class DIGEST:
    # SHA256 object identifier: 2.16.840.1.101.3.4.2.1
    SHA256_OID = [0x60, 0x86, 0x48, 0x01, 0x65, 0x03, 0x04, 0x02, 0x01, 0x05, 0x00, 0x04, 0x20]
    HEADER = [0x30, 0x31, 0x30, 0x0D, 0x06, 0x09]

def SELECT(data, CLA, P1, P2):
    """
        CLA INS P1 P2 Lc DATA
        
        @param P1: 04: selected by DF name, 02: selected by EF identifier directly under current DF
        @param P2: Record Referencing
        @param CLA: 0x00
        @param Lc: Length to read
    """
    return [CLA, APDU_CMD.SELECT, P1, P2] + [len(data)] + data

def SELECT_AP(data, CLA=0x00, P1=0x04, P2=0x0C):
    """
        CLA INS P1 P2 Lc DATA
    """
    return SELECT(data, CLA, P1, P2)

def SELECT_FILE(data, CLA=0x00, P1=0x02, P2=0x0C):
    """
        CLA INS P1 P2 Lc DATA
    """
    return SELECT(data, CLA, P1, P2)

def VERIFY_PIN(PIN, P1=0x00, P2=0x80, CLA=0x00):
    """
        CLA INS P1 P2 Lc DATA
        
        @param pin: list of bytes (length 4-8 bytes)
        @param p1: 0x00 is only valid
        @param p2: Key location
        @return (data, sw1, sw2)
    """
    return [CLA, APDU_CMD.VERIFY, P1, P2, len(PIN)] + PIN

def READ_BINARY(P1, P2, CLA=0x00, Lc=0x00):
    """
        CLA INS P1 P2 Le
        
        @param P1|P2: 
            If bit8=1 in P1, then bit7-6 are set to 0. bit3-1 of P1 are a short EF (Elementary File) identifier and P2 is the offset of the first byte to be read in date units from the beginning of the file.
            If bit8=0 in P1, then P1||P2 is the offset of the first byte to be read in data units from the beginning of the file.
        @param CLA: 0x00
        @param Lc: Length to read 
    """
    return [CLA, APDU_CMD.READ_BINARY, P1, P2, Lc]

def COMPUTE_SIGNATURE(hash, CLA=0x80, P1=0x00, P2=0x80):
    """
        CLA INS P1 P2 Lc DATA Le
        P1 - 0x00
        P2 - 0x00
        Lc - length of data
        Le - expected length of returned data
    """
    data = DIGEST.HEADER  + DIGEST.SHA256_OID + hash
    return [CLA, APDU_CMD.COMPUTE_SIGNATURE, P1, P2] + [len(data)] + data + [0x00]


def get_hex(input_list):
    """
        Convert a list of bytes into hex string
    """
    return " ".join([hex(i) for i in input_list])

def get_status_msg(sw1, sw2):
    """
        Get sw1, sw2 status        
        By referring to: https://tex2e.github.io/blog/protocol/apdu-return-status-msg
    """
    if sw1 == 0x90 and sw2 == 0x00:
        return "I: 正常終了"
    if sw1 == 0x61:
        return f"I: 出力成功。残り{int(sw2)}バイトが出力可能です。"
    if sw1 == 0x62:
        if sw2 == 0x81: return "W: 出力データに異常があります。"
        if sw2 == 0x83: return "W: 選択したファイルは無効になりました。"
        return "W: 不揮発性メモリの状態は変更されていません。"
    if sw1 == 0x63:
        if sw2 == 0x81: return "W: ファイルの書き込み可能領域が不足しています。"
        if (sw2 >> 4) == 0xc: return f"W: 検証失敗。残り{int(sw2 & 0x0f)}回リトライ可能です。"
        return "W: 不揮発性メモリの状態は変化しています。"
    if sw1 == 0x64:
        if sw2 == 0x01: return "E: コマンドはタイムアウトしました。"
        return "E: 不揮発性メモリの状態は変更されていません。"
    if sw1 == 0x65:
        if sw2 == 0x01: return "E: 書き込みエラーが発生しました。"
        return "E: 不揮発性メモリの状態は変化しています。"
    if sw1 == 0x66:
        if sw2 == 0x00: return "E: 受信時にタイムアウトエラーが発生しました。"
        if sw2 == 0x01: return "E: 受信時にパリティチェックエラーが発生しました。"
        if sw2 == 0x02: return "E: 受信時にチェックサムエラーが発生しました。"
        if sw2 == 0x69: return "E: 不正な暗号化/復号パディングが含まれています。"
        return "E: セキュリティエラーが発生しました。"
    if sw1 == 0x67:
        if sw2 == 0x00: return "E: データ長（Lc/Leフィールド）が不正です。"
        return "E: データ長が不正です。"
    if sw1 == 0x68:
        return "E: CLAの機能は対応していません。"
    if sw1 == 0x69:
        if sw2 == 0x81: return "E: ファイル構造と互換性のないコマンドです。"
        if sw2 == 0x82: return "E: セキュリティ条件が満たされていません。"
        if sw2 == 0x83: return "E: 認証方法がブロックされています。"
        if sw2 == 0x84: return "E: 参照データがブロックされました。"
        if sw2 == 0x85: return "E: コマンドの使用条件を満たしていません。"
        if sw2 == 0x86: return "E: ファイルが存在しません。"
        if sw2 == 0x87: return "E: セキュアメッセージングに必要なデータオブジェクトが存在しません。"
        if sw2 == 0x88: return "E: セキュアメッセージングのデータオブジェクトが不正です。"
        return "E: コマンドは許可されていません。"
    if sw1 == 0x6a:
        if sw2 == 0x80: return "E: データフィールドのパラメータが正しくないです。"
        if sw2 == 0x81: return "E: サポートされていない機能です。"
        if sw2 == 0x82: return "E: ファイルが存在しません。"
        if sw2 == 0x83: return "E: レコードが存在しません。"
        if sw2 == 0x84: return "E: レコードまたはファイルのメモリ容量が不足しています。"
        if sw2 == 0x85: return "E: LcはTLV構造と一致しません。"
        if sw2 == 0x86: return "E: P1またはP2パラメータが正しくありません。"
        if sw2 == 0x87: return "E: LcがP1-P2と一致しない。"
        if sw2 == 0x88: return "E: 参照データが見つかりません。"
        if sw2 == 0x89: return "E: ファイルが既に存在します。"
        if sw2 == 0x8A: return "E: DF名が既に存在します。"
        return "E: パラメータの値が間違っています。"
    if sw1 == 0x6b:
        return "E: パラメータの値が間違っています。"
    if sw1 == 0x6d:
        return "E: 命令コード(INS)が不正です。"
    if sw1 == 0x6e:
        return "E: 命令クラス(CLA)が不正です。"
    if sw1 == 0x6f:
        return "E: 内部エラーが発生しました。"
    return ""