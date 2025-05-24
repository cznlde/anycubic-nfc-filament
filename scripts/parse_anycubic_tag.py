from smartcard.System import readers

def read_block(connection, page):
    cmd = [0xFF, 0xB0, 0x00, page, 0x04]
    data, sw1, sw2 = connection.transmit(cmd)
    if (sw1, sw2) == (0x90, 0x00):
        return bytes(data)
    else:
        return None

# Verbinden met reader
reader = readers()[0]
connection = reader.createConnection()
connection.connect()
print("✅ Verbonden met NFC-tag")

# Blokken ophalen
blocks = {page: read_block(connection, page) for page in range(4, 16)}

# Samenvoegen naar logische strings
def extract_ascii(start_page, end_page):
    raw = b''.join(blocks[p] for p in range(start_page, end_page + 1) if blocks[p])
    return raw.rstrip(b'\x00').decode(errors='ignore')

result = {
    "id_hex": blocks[4].hex() if blocks[4] else None,
    "vendor": extract_ascii(5, 6),
    "type": extract_ascii(7, 7),
    "material": extract_ascii(15, 15),
    "code": extract_ascii(10, 10),
    "raw_blocks": {p: blocks[p].hex() if blocks[p] else None for p in blocks}
}

# Print het resultaat
print("\n🔎 Uitlezing:")
for k, v in result.items():
    print(f"{k}: {v}")
