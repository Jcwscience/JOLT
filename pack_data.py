import struct

def pack_data(data):
    # Check the type of data
    data_type = type(data)

    if data_type == str:
        # For strings
        return b'\x01' + data.encode('utf-8')
    elif data_type == int:
        # For integers
        return b'\x02' + struct.pack('<i', data)
    elif data_type == float:
        # For floats
        return b'\x03' + struct.pack('<f', data)
    else:
        raise ValueError(f"Data type {data_type} not supported")
