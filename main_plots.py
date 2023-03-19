from aes import AES
from halka import HALKA
from utils import split_blocks, pad, str2bits, bits2str
from bitstring import BitArray
import matplotlib.pyplot as plt
import tqdm


# aes = True  
# if aes:


input_bits = []
num_op_AES_round = []
num_op_HALKA_round = []
num_op_AES_all = []
num_op_HALKA_all = []
num_op_AES_blocks = []
num_op_HALKA_blocks = []

for n in tqdm.tqdm([1,2,5,10,20,50,100,200, 400]):
    # 16 byte key (128 bits)
    master_key = b"0xffffffffffffff0xffffffffffffff" #ffffffffffffff
    # print(len(master_key))
    aes = AES(master_key)
    plain_text = b"Introduction to blockchain is the best cource ever!" * n

    plain_text_blocks = split_blocks(
        plain_text, block_size=16, require_padding=False
    )
    for j,block in enumerate(plain_text_blocks):
        if len(block) != 16:
            block = pad(block, length=16)
        # print(len(block), 'bytes')
        # each block is 16 bytes
        block_enc = aes.encrypt_block(block)
        block_dec = aes.decrypt_block(block_enc)
        assert block == block_dec
        # print("original block:", block)
        # print("encrypted block:", block_enc)
        # print("decrypted block:", block_dec)
        # print()
        # print()
        

        if j ==0:
            # print(aes.operations_per_round)
            # print(aes.operations_all_rounds)
            num = 0
            for k in aes.operations_one_round.keys():
                num+=aes.operations_one_round[k]
            num_op_AES_round.append(num)

            num = 0
            for k in aes.operations_all_rounds.keys():
                num+=aes.operations_all_rounds[k]
            num_op_AES_all.append(num)

    num = 0
    for k in aes.operations_all_rounds.keys():
        num+=aes.operations_all_rounds[k]
    num_op_AES_blocks.append(num)
    # else:

    # 80 bits key (or 10 bytes)
    #[0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
    master_key = '0xffffffffffffffffffff'
    key_array = BitArray(hex=master_key)
    master_key_bits = list(key_array.bin)
    master_key_bits = list(map(int, master_key_bits)) # str list -> int list

    halka = HALKA(master_key_bits)
    plain_text = "Introduction to blockchain is the best cource ever!" * n # in bytes
    plain_text_bits = str2bits(plain_text) # from str to bits
    input_bits.append(len(plain_text_bits))

    # halka takes 64 bit (8bytes) block size
    plain_text_blocks = split_blocks(
        plain_text_bits, block_size=64, require_padding=False
    )
    for j, block in enumerate(plain_text_blocks):
        if len(block) != 64:
            block = pad(block, length=64, bit=True)
        # each block is 8 bytes (64 bits)
        block_enc = halka.encrypt_block(block) 
        block_dec = halka.decrypt_block(block_enc)
        # print("original block:", block)
        # print("encrypted block:", block_enc)
        # print("decrypted block:", block_dec)
        assert block == block_dec

        if j==0:
            # print(halka.operations_one_round)
            # print(halka.operations_all_rounds)
            num = 0
            for k in halka.operations_one_round.keys():
                num+=halka.operations_one_round[k]
            num_op_HALKA_round.append(num)

            num = 0
            for k in halka.operations_all_rounds.keys():
                num+=halka.operations_all_rounds[k]
            num_op_HALKA_all.append(num)

    num = 0
    for k in halka.operations_all_rounds.keys():
        num+=halka.operations_all_rounds[k]
    num_op_HALKA_blocks.append(num)
        # print()
        # print()
        

    # print(input_bits)
plt.figure()
plt.plot(input_bits, num_op_HALKA_blocks, '*-', label=f'HALKA all blocks: 64 bits block, 24 rounds', linewidth = 2)
plt.plot(input_bits, num_op_AES_blocks, '*-', label='AES all blocks: 128 bits block, 14 rounds', linewidth = 2)
plt.grid()
plt.title('Total number of operations', fontweight = 'bold')
plt.yscale('log')
plt.xlabel('Plain text in bits')
plt.ylabel('Number of XOR, substitution and permutation')
plt.legend()
plt.savefig('All_blocks.png')

plt.figure()
# plt.plot(input_bits, num_op_HALKA_all, '*-', label='HALKA all rounds')
# plt.plot(input_bits, num_op_AES_all, '*-', label='AES all rounds')
plt.plot(input_bits, num_op_HALKA_round, '*-', label='HALKA per round', linewidth = 2)
plt.plot(input_bits, num_op_AES_round, '*-', label='AES per round', linewidth = 2)
plt.grid()
plt.title('Number of operations for one round', fontweight = 'bold')
plt.xlabel('Plain text in bits')
plt.ylabel('Number of XOR, substitution and permutation')
plt.legend()
plt.savefig('Per_round.png')
