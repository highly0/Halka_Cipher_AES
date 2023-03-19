def pad(plaintext, length=16, bit=False):
    """
    Pad the text to lenght n, if bit is True, return a list of bits. 
    Otherwise, return a list of bytes
    """
    padding_len = length - (len(plaintext) % length)

    padding_char = 0 if bit == True else padding_len
    padding = [padding_char] * padding_len
    res = bytes(list(plaintext) + list(padding)) if bit==False else list(plaintext) + list(padding)
    return res

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

def b2matrix(text, n=4):
    """ Converts a n-byte/bit array into a nxn matrix.  """
    return [list(text[i:i+n]) for i in range(0, len(text), n)]

def matrix2b(matrix):
    """ Converts a nxn matrix into a 16-byte array.  """
    return bytes(sum(matrix, []))

def xor_bytes(a, b):
    """ Returns a new byte array with the elements xor'ed. """
    return bytes(i^j for i, j in zip(a, b))


def str2bits(s):
    """ Convert from str to bit/binary. """
    bit_str = ''.join(format(ord(x), 'b') for x in s)
    bit_str = list(bit_str)
    bit_arr = list(map(int, bit_str)) # str list -> int list
    return bit_arr

def bits2str(s):
    return ''.join(chr(int(s[i*8:i*8+8],2)) for i in range(len(s)//8))

def rotate(K):
    newK=K.copy()
    j=0
    for i in range(len(K)-1, -1,-1):
        newK[j]=K[i]
        j=j+1
    return newK

def shift_by(K, sh):
    newK=K.copy()
    for i in range(len(K)):
        if (i+sh)<len(K):
            newK[i]=K[i+sh]
        else:
            newK[i]=K[i-(len(K)-sh)]
    return newK

def xor_bits(a,b):
    """ xor bit wise """
    c=[]
    for i in range(len(a)):
        c.append(a[i]^b[i])
    return c

def bits2number(a, n=8):
    """ convert bits to byte number"""
    N=0
    for i in range(len(a)):
        N=N+a[len(a)-1-i]*2**(i)
    return N

def number2bits(N, n=8):
    """ convert byte number to bits"""
    bits=[]
    divs=N
    for i in range(n):
        bits=[divs%2]+bits
        divs=divs//2
    return bits
