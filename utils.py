def pad(plaintext, length=16):
    """
    Pads the given plaintext with PKCS#7 padding to a multiple of 16 bytes.
    Note that if the plaintext size is a multiple of 16,
    a whole block will be added.
    """
    padding_len = length - (len(plaintext) % length)
    padding = [padding_len] * padding_len
    return list(plaintext) + list(padding)

def unpad(plaintext):
    """
    Removes a PKCS#7 padding, returning the unpadded text and ensuring the
    padding was correct.
    """
    padding_len = plaintext[-1]
    assert padding_len > 0
    message, padding = plaintext[:-padding_len], plaintext[-padding_len:]
    assert all(p == padding_len for p in padding)
    return message

def split_blocks(message, block_size=16, require_padding=True):
    assert len(message) % block_size == 0 or not require_padding
    return [message[i:i+block_size] for i in range(0, len(message), block_size)]

def bytes2matrix(text, n=4):
    """ Converts a 16-byte array into a nxn matrix.  """
    return [list(text[i:i+n]) for i in range(0, len(text), n)]

def matrix2bytes(matrix):
    """ Converts a nxn matrix into a 16-byte array.  """
    return bytes(sum(matrix, []))

def xor_bytes(a, b):
    """ Returns a new byte array with the elements xor'ed. """
    return bytes(i^j for i, j in zip(a, b))

def bits(n):
    """ From int, generate bit stream. """
    while n:
        b = n & (~n+1)
        yield b
        n ^= b

def bytes2bits(n):
    """ Convert from bytes array to bit. """
    res = []
    for byte in n:
        for bit in bits(byte):
            res.append(bit)
    return res
