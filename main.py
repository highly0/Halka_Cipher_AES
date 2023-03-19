from aes import AES
from halka import HALKA
from utils import split_blocks, pad, str2bits, bits2str
from bitstring import BitArray

if __name__ == "__main__":
    aes = True
    if aes:
        # 16 byte key (128 bits)
        master_key = b"yourmomisawhoree"
        aes = AES(master_key)
        plain_text = b"your mother is a wholehearted whoreeeee!" * 25

        plain_text_blocks = split_blocks(
            plain_text, block_size=16, require_padding=False
        )
        for block in plain_text_blocks:
            if len(block) != 16:
                block = pad(block, length=16)
            print(len(block), 'bytes')
            # each block is 16 bytes
            block_enc = aes.encrypt_block(block)
            block_dec = aes.decrypt_block(block_enc)
            assert block == block_dec
            print("original block:", block)
            print("encrypted block:", block_enc)
            print("decrypted block:", block_dec)
            print()
            print()
            print(aes.operations_one_round)
            print(aes.operations_all_rounds)
    else:
        # 80 bits key (or 10 bytes)
        #[0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
        master_key = '0xffffffffffffffffffff'
        key_array = BitArray(hex=master_key)
        master_key_bits = list(key_array.bin)
        master_key_bits = list(map(int, master_key_bits)) # str list -> int list

        halka = HALKA(master_key_bits)
        plain_text = "your mother is such a slut!" # in bytes
        plain_text_bits = str2bits(plain_text) # from str to bits

        # halka takes 64 bit (8bytes) block size
        plain_text_blocks = split_blocks(
            plain_text_bits, block_size=64, require_padding=False
        )
        for block in plain_text_blocks:
            if len(block) != 64:
                block = pad(block, length=64, bit=True)
            # each block is 8 bytes (64 bits)
            block_enc = halka.encrypt_block(block) 
            block_dec = halka.decrypt_block(block_enc)
            print("original block:", block)
            print("encrypted block:", block_enc)
            print("decrypted block:", block_dec)
            assert block == block_dec
            print()
            print()
            print(halka.operations_one_round)
            print(halka.operations_all_rounds)