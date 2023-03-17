from aes import AES, split_blocks, pad

if __name__ == '__main__':
    master_key = key = b'yourmomisawhoree' 
    aes = AES(master_key)
    plain_text = b'your mother is a wholehearted whoreeeee!' * 25

    plain_text_blocks = split_blocks(plain_text, require_padding=False)
    for block in plain_text_blocks:
        if len(block) != 16:
            block = pad(block)
        block_enc = aes.encrypt_block(block)
        block_dec = aes.decrypt_block(block_enc)
        print(block_enc)
        print(block_dec)
    #print(plain_text_blocks)

    #plain_text = aes.encrypt_block(plain_text)
    #print(plain_text)