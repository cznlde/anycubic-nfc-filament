from smartcard.System import readers

reader = readers()[0]
connection = reader.createConnection()
connection.connect()

print("✅ NFC-tag verbonden. Lezen...")

for page in range(4, 16):  # blokken 4 t/m 15 (4 bytes per stuk)
    cmd = [0xFF, 0xB0, 0x00, page, 0x04]
    data, sw1, sw2 = connection.transmit(cmd)
    if (sw1, sw2) == (0x90, 0x00):
        hex_data = ' '.join(f"{b:02X}" for b in data)
        print(f"Blok {page:02}: {hex_data}")
    else:
        print(f"❌ Blok {page:02} niet gelezen (SW={sw1:02X} {sw2:02X})")
