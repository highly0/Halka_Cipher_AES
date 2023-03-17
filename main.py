from aes import AES
from halka import HALKA
from utils import split_blocks, pad, bytes2bits

if __name__ == '__main__':
    aes = False
    if aes:
        # 16 byte key (128 bits)
        master_key = b'yourmomisawhoree' 
        aes = AES(master_key)
        plain_text = b'your mother is a wholehearted whoreeeee!' * 25

        plain_text_blocks = split_blocks(plain_text, block_size=16, require_padding=False)
        for block in plain_text_blocks:
            if len(block) != 16:
                block = pad(block, length=16)

            # each block is 16 bytes
            block_enc = aes.encrypt_block(block)
            block_dec = aes.decrypt_block(block_enc)
            print(block_enc)
            print(block_dec)
            print()
    else:
        # 80 bits key (or 10 bytes)
        master_key = [0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff]
        master_key_bits = bytes2bits(master_key)
        halka = HALKA(master_key_bits)
        plain_text = [0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
                    0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
                    0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,] 
        plain_text_bits = bytes2bits(plain_text) # 64 bits
   
        # halka takes 64 bit (8bytes) block size (half of AES)
        plain_text_blocks = split_blocks(plain_text_bits, block_size=64, require_padding=False)

        for block in plain_text_blocks:
            if len(block) != 64:
                block = pad(block, length=64)
            # each block is 8 bytes (64 bits)
            block_enc = halka.encrypt_block(block) # NOT WORKING RN) BUT IT RUNS
            block_dec = halka.decrypt_block(block)

