from utils import bytes2matrix, matrix2bytes, xor_bytes

s_box = (
        0x24, 0x2c, 0x20, 0xdc, 0x26, 0x73, 0xd8, 0x91, 0x25, 0xb7, 0x8f, 0x9c, 0xda, 0x1f, 0xfe, 0xe9, 
        0x9f, 0xa4, 0xd5, 0x6d, 0xc3, 0x71, 0x32, 0x78, 0x96, 0xdb, 0x55, 0xb9, 0x4c, 0x49, 0x6e, 0x42, 
        0x9a, 0xf9, 0x1d, 0x64, 0x03, 0x5c, 0xa0, 0x00, 0x4a, 0xd7, 0xe3, 0x8e, 0x75, 0xaf, 0x0b, 0x0a, 
        0x7d, 0x4d, 0x5b, 0x1a, 0x1c, 0xe7, 0x6a, 0x74, 0x10, 0x06, 0x92, 0x29, 0x81, 0x79, 0x17, 0x40, 
        0x07, 0x7b, 0x69, 0xca, 0xc8, 0xb8, 0xef, 0x84, 0xc2, 0x37, 0x3a, 0x98, 0xdf, 0x66, 0x12, 0xb6, 
        0x13, 0x08, 0x5d, 0xfc, 0x47, 0x31, 0xf1, 0x21, 0x8c, 0x14, 0xe1, 0x51, 0x33, 0x19, 0xb3, 0x65, 
        0x88, 0x4e, 0x90, 0x70, 0x1b, 0xa8, 0x3b, 0xcc, 0x38, 0x15, 0x45, 0xa7, 0x83, 0x39, 0x0c, 0xde,
        0xa1, 0x3e, 0xc1, 0xb5, 0xeb, 0x7f, 0xac, 0xa2, 0x01, 0x76, 0x9b, 0x8a, 0xb4, 0xbd, 0x99, 0x16, 
        0x35, 0xd4, 0x8b, 0x4f, 0x02, 0x54, 0x53, 0xbe, 0x52, 0xc7, 0xea, 0x09, 0x41, 0xc6, 0xf4, 0xb1, 
        0x58, 0x57, 0x6b, 0x2d, 0xf8, 0xab, 0x87, 0x7a, 0xf6, 0x59, 0xa3, 0x85, 0x61, 0x3f, 0x9e, 0xed, 
        0x63, 0xbf, 0xfd, 0xb2, 0xe8, 0x18, 0xd2, 0x48, 0x7c, 0x95, 0x0f, 0x2e, 0x44, 0xce, 0x5f, 0xa6, 
        0xf0, 0x8d, 0x3c, 0xf5, 0x46, 0x23, 0x1e, 0xd0, 0x2f, 0xee, 0xba, 0x34, 0x6f, 0x5a, 0x04, 0x5e, 
        0xc5, 0xf2, 0xc4, 0x11, 0xe2, 0x7e, 0xe0, 0x0e, 0xdd, 0xbb, 0x9d, 0x62, 0x80, 0x2b, 0xae, 0x50, 
        0xaa, 0x97, 0xbc, 0xc9, 0x94, 0x72, 0xe5, 0xd3, 0x77, 0x86, 0x2a, 0xcd, 0xb0, 0x05, 0xd9, 0xd1,
        0xe6, 0xe4, 0xa9, 0xad, 0xd6, 0x56, 0x6c, 0x30, 0x43, 0xff, 0x89, 0xcb, 0x60, 0xf7, 0x67, 0xcf, 
        0xa5, 0x36, 0xc0, 0x0d, 0x93, 0xfb, 0x82, 0xf3, 0x27, 0xec, 0x4b, 0x68, 0x22, 0xfa, 0x28, 0x3d,
        )

inv_s_box = ( 
            0x27, 0x78, 0x84, 0x24, 0xbe, 0xdd, 0x39, 0x40, 0x51, 0x8b, 0x2f, 0x2e, 0x6e, 0xf3, 0xc7, 0xaa, 
            0x38, 0xc3, 0x4e, 0x50, 0x59, 0x69, 0x7f, 0x3e, 0xa5, 0x5d, 0x33, 0x64, 0x34, 0x22, 0xb6, 0x0d, 
            0x02, 0x57, 0xfc, 0xb5, 0x00, 0x08, 0x04, 0xf8, 0xfe, 0x3b, 0xda, 0xcd, 0x01, 0x93, 0xab, 0xb8, 
            0xe7, 0x55, 0x16, 0x5c, 0xbb, 0x80, 0xf1, 0x49, 0x68, 0x6d, 0x4a, 0x66, 0xb2, 0xff, 0x71, 0x9d, 
            0x3f, 0x8c, 0x1f, 0xe8, 0xac, 0x6a, 0xb4, 0x54, 0xa7, 0x1d, 0x28, 0xfa, 0x1c, 0x31, 0x61, 0x83, 
            0xcf, 0x5b, 0x88, 0x86, 0x85, 0x1a, 0xe5, 0x91, 0x90, 0x99, 0xbd, 0x32, 0x25, 0x52, 0xbf, 0xae, 
            0xec, 0x9c, 0xcb, 0xa0, 0x23, 0x5f, 0x4d, 0xee, 0xfb, 0x42, 0x36, 0x92, 0xe6, 0x13, 0x1e, 0xbc,
            0x63, 0x15, 0xd5, 0x05, 0x37, 0x2c, 0x79, 0xd8, 0x17, 0x3d, 0x97, 0x41, 0xa8, 0x30, 0xc5, 0x75, 
            0xcc, 0x3c, 0xf6, 0x6c, 0x47, 0x9b, 0xd9, 0x96, 0x60, 0xea, 0x7b, 0x82, 0x58, 0xb1, 0x2b, 0x0a, 
            0x62, 0x07, 0x3a, 0xf4, 0xd4, 0xa9, 0x18, 0xd1, 0x4b, 0x7e, 0x20, 0x7a, 0x0b, 0xca, 0x9e, 0x10, 
            0x26, 0x70, 0x77, 0x9a, 0x11, 0xf0, 0xaf, 0x6b, 0x65, 0xe2, 0xd0, 0x95, 0x76, 0xe3, 0xce, 0x2d, 
            0xdc, 0x8f, 0xa3, 0x5e, 0x7c, 0x73, 0x4f, 0x09, 0x45, 0x1b, 0xba, 0xc9, 0xd2, 0x7d, 0x87, 0xa1, 
            0xf2, 0x72, 0x48, 0x14, 0xc2, 0xc0, 0x8d, 0x89, 0x44, 0xd3, 0x43, 0xeb, 0x67, 0xdb, 0xad, 0xef, 
            0xb7, 0xdf, 0xa6, 0xd7, 0x81, 0x12, 0xe4, 0x29, 0x06, 0xde, 0x0c, 0x19, 0x03, 0xc8, 0x6f, 0x4c,
            0xc6, 0x5a, 0xc4, 0x2a, 0xe1, 0xd6, 0xe0, 0x35, 0xa4, 0x0f, 0x8a, 0x74, 0xf9, 0x9f, 0xb9, 0x46, 
            0xb0, 0x56, 0xc1, 0xf7, 0x8e, 0xb3, 0x98, 0xed, 0x94, 0x21, 0xfd, 0xf5, 0x53, 0xa2, 0x0e, 0xe9,
            )

permutation_map = [10, 21, 28, 38, 44, 48, 59, 1, 51, 15, 41, 2, 60, 34, 24, 20, 56, 6,
                17, 31, 36, 53, 12, 46, 30, 52, 11, 4, 23, 35, 40, 63, 8, 39, 3, 43,57,49,
                16,25,37,42,61,50, 0, 9, 18,26,58,55, 7, 19,29,14,47,32,33, 5, 62,45,13,54,22,27]

def shift_rows(s):
    s_flatten = []
    for row in s:
        s_flatten+=row

    new_s_flatten = s_flatten.copy()
    for i,s_b in enumerate(s_flatten):
        new_s_flatten[permutation_map[i]] = s_flatten[i]
    
    ind = 0
    for i,row in enumerate(s):
        for j,col in enumerate(row):
            s[i][j] = new_s_flatten[ind]
            ind+=1

# TODO: Change P-box decrypt
def inv_shift_rows(s):
    s_flatten = []
    for row in s:
        s_flatten+=row

    new_s_flatten = s_flatten.copy()
    for i,s_b in enumerate(s_flatten):
        new_s_flatten[permutation_map.index(i)] = s_flatten[i]

    ind = 0
    for i,row in enumerate(s):
        for j,col in enumerate(row):
            s[i][j] = new_s_flatten[ind]
            ind+=1

def add_round_key(s, k):
    for i in range(4):
        for j in range(4):
            s[i][j] ^= k[i][j]


def sub_bytes(s):
    for i in range(2):
        for j in range(2):
            s[i][j] = s_box[s[i][j]]


def inv_sub_bytes(s):
    for i in range(2):
        for j in range(2):
            s[i][j] = inv_s_box[s[i][j]]

class HALKA:
    """
    Class for HALKA
    """
    def __init__(self, master_key):
        """
        Initializes the object with a given key.
        """
        assert len(master_key) == 80 # key size must be 80 bits
        self.n_rounds = 24 
        # for halka, length of self._key_matrices should be 25, each subarr is 64 bits
        self._key_matrices = self._expand_key(master_key)

    # TODO: change how the key is shifted
    def _expand_key(self, master_key):
        """
        Expands and returns a list of key matrices for the given master_key.
        """
        # TODO (THIS IS JUST A PLACEHOLDER, NEED REAL KEY ALGO)
        res = []
        start_idx = 0
        end_idx = start_idx + 64
        for i in range(25):
            if start_idx < end_idx and (end_idx - start_idx == 64):
                curr_key = bytes2matrix(master_key[start_idx:end_idx], n=8)
                res.append(curr_key)
            else: # wrap around 
                curr_key_i = master_key[start_idx:]
                curr_key_i += master_key[:end_idx]
                res.append(bytes2matrix(curr_key_i))
            start_idx += 64
            end_idx += 64
            start_idx %= 80
            end_idx %= 80
        return res

    def encrypt_block(self, plaintext):
        """
        Encrypts a single block of 8 byte long plaintext.
        """
        # each block is 64 bits
        assert len(plaintext) == 64

        # 8x8 array -> 8 bytes words
        plain_state = bytes2matrix(plaintext, n=8)

        add_round_key(plain_state, self._key_matrices[0])

        for i in range(1, self.n_rounds):
            # S block -> XOR with eight 8-bit S-boxes
            sub_bytes(plain_state) # getting back 8 bytes
            # P block, no mix columns in Halka
            shift_rows(plain_state)

            add_round_key(plain_state, self._key_matrices[i])


        sub_bytes(plain_state)
        shift_rows(plain_state)
        add_round_key(plain_state, self._key_matrices[-1])

        return sum(plain_state, []) 

    def decrypt_block(self, ciphertext):
        """
        Decrypts a single block of 16 byte long ciphertext.
        """
        assert len(ciphertext) == 64

        cipher_state = bytes2matrix(ciphertext, n=8)

        add_round_key(cipher_state, self._key_matrices[-1])
        inv_shift_rows(cipher_state)
        inv_sub_bytes(cipher_state)

        for i in range(self.n_rounds - 1, 0, -1):
            add_round_key(cipher_state, self._key_matrices[i])
            inv_shift_rows(cipher_state) # no mix columns
            inv_sub_bytes(cipher_state)

        add_round_key(cipher_state, self._key_matrices[0])

        return sum(cipher_state, [])