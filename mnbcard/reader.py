from smartcard.Exceptions import NoCardException
from smartcard.System import readers

def get_reader():
    rd = readers()

    if rd is None or len(rd) <=0:
        raise Exception('No reader deteched')

    return readers()[0]

def connect_card(reader):
    try:
        connection = reader.createConnection()
        connection.connect()
        return connection
    except NoCardException:
        raise Exception('No card deteched')