#SYMMETRIC ENCRYPTION
#Kukuh Rilo Pambudi
#5114100178
#KIJ-A

import string
import random

def input_processing(inp):
    inp_length = int(len(inp))
    inp_loop = inp_length / 4
    if inp_length%4!=0:
        inp_loop+=1
    return inp_loop

def make_list(inp_list):
    inp_listout=list()
    inp_listout.append({'value': [inp_list[i] for i in range(0 + len(inp_list))]})
    inp_listout.append({'ascii': [ord(inp_list[i]) for i in range(0 + len(inp_list))]})
    #inp_listout.append({'binary': ['{:08b}'.format(inp_listout[1]['ascii'][i]) for i in range(0 + len(inp_list))]})
    return inp_listout

def xor(a, b):
    xored = int(a) ^ int(b)
    return xored

def addition_mod(inp0, inp1):
    added = []
    added_modulo = []
    for x in range(0, len(inp0)):
        added.append(inp0[x] + inp1[x])
        #added_modulo.append(added[x]&pow(2, 64))
    #print added
    #print added_modulo

    # jika bit yang didapat lebih dari 64 maka harus di mood 2^64
    added_binary = ''.join(['{:08b}'.format(added[c]) for c in range(len(added))])
    if len(inp0)>64:
        added_binary=added_binary[-64:]
        added_binary_splited=[]
        binary_temp=[]
        for y in range(len(added_binary)):
            binary_temp.append(y)
            if y%4==0 or y==len(added_binary):
                added_binary_splited.append(binary_temp)
                binary_temp=[]
        added_number_splited=[]
        for y in added_binary_splited:
            added_number_splited.append(int(y, 2))
        return added_binary_splited
    else:
        return added

def encryp(inp_l, inp_asc, sec0, sec1):
    start = 0
    added_moded = []
    for x in range(0, inp_l):
        xored = []
        for y in range(0, 4):
            xored.append(xor(inp_asc[1]['ascii'][start], sec0[y]))
            if start==len(inp_asc[1]['ascii'])-1:
                break
            start+=1
        #print xored
        added_moded.append(addition_mod(xored, sec1))
    return added_moded

def additive_mod(inp0, inp1, loop_addtv_s):
    subtracted = []
    y = 0
    for x in range(loop_addtv_s, loop_addtv_s+4):
        subtracted.append(inp0[x] - inp1[y])
        loop_addtv_e = x
        y+=1
        if loop_addtv_e == len(inp0)-1:
            break
    #print subtracted
    return subtracted, loop_addtv_e+1

def decryp(inp_l, inp, sec0, sec1):
    start = 0
    decrypted = []

    loop_addtv = 0
    for x in range(0, inp_l):
        #mendapatkan additive mod
        d_added_moded, loop_addtv = additive_mod(inp, sec1, loop_addtv)

        #mendapatkan hasil xor
        for y in range(0, len(d_added_moded)):
            #d_exored = decryp(added_moded[y], secretkey0[y], secretkey1[y])
            decrypted.append(xor(d_added_moded[y], sec0[y]))
            start+=1
        #print d_exored
        #print("".join([chr(c) for c in d_xored]))

    return decrypted

def generate_secrekey():
    secretkey = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
    secretkey_ascii = make_list(secretkey)
    secretkey0 = secretkey_ascii[1]['ascii'][0:4]
    secretkey1 = secretkey_ascii[1]['ascii'][4:8]
    return secretkey, secretkey0, secretkey1

if __name__ == '__main__':
    #request input dari pengguna, input berupa text tanpa enter
    inp = raw_input('Masukkan pesan : ')

    #mendapatkan jumlah loop yang diperlukan
    inp_loop = input_processing(inp)
    #print (inp, inp_loop)

    #membuat list ascii dari input
    inp_ascii=list()
    inp_ascii=make_list(inp)
    #print inp_ascii[1]['ascii']

    #membuat secretkey yang terdiri dari angka dan huruf kapital
    secretkey, secretkey0, secretkey1 = generate_secrekey()
    print(secretkey, secretkey0, secretkey1)

    #proses encryp
    encrypted = encryp(inp_loop, inp_ascii, secretkey0, secretkey1)
    #print encrypted
    #print("".join([chr(c) for c in encrypted]))
    encrypted_join = []
    print 'Encrypted : '
    for x in range(0, len(encrypted)):
        for c in encrypted[x]:
            encrypted_join.append(c)
    print "".join([chr(c) for c in encrypted_join])

        #if x==len(encrypted)-1:
        #    print("".join([chr(c) for c in encrypted[x]]))
        #else:
        #    print("".join([chr(c) for c in encrypted[x]])),

    #proses decryp
    decrypted = decryp(inp_loop, encrypted_join, secretkey0, secretkey1)
    #print decrypted
    print 'Decripted : '
    print "".join([chr(c) for c in decrypted])