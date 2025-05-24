from smartcard.System import readers
from smartcard.util import toHexString

SELECT = [0xFF, 0xCA, 0x00, 0x00, 0x00]

reader = readers()[0]
connection = reader.createConnection()
connection.connect()
data, sw1, sw2 = connection.transmit(SELECT)
print("✅ Tag gedetecteerd!")
print("🆔 UID:", toHexString(data))
