import os
import time
import random
import signal
from Crypto.Cipher import AES

def read_disk(filepath):
    with open(filepath, 'rb') as f:
        while True:
            chunk = f.read(1024*1024)
            if not chunk:
                break

def modify_entropy(filepath):
    with open(filepath, 'rb') as f:
        data = f.read()

    entropy = sum([data.count(bytes([i])) * float(data.count(bytes([i])))/len(data) for i in range(256)])

    new_data = b''
    for i in range(len(data)):
        new_byte = bytes([random.randint(0, 255)])
        new_data += new_byte

    with open(filepath, 'wb') as f:
        f.write(new_data)

    with open(filepath, 'rb') as f:
        new_data = f.read()

    new_entropy = sum([new_data.count(bytes([i])) * float(new_data.count(bytes([i])))/len(new_data) for i in range(256)])

    print(f'Entropía del archivo {filepath} antes: {entropy}')
    print(f'Entropía del archivo {filepath} después: {new_entropy}')

def encrypt(plaintext):
    key = os.urandom(32)
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)
    return ciphertext, cipher.nonce, tag

def decrypt(ciphertext, nonce, tag):
    key = os.urandom(32)
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    return plaintext

def signal_handler(signum, frame):
    raise Exception("El script ha superado el límite de tiempo.")

if __name__ == '__main__':
    filepath = '/home/kali/Desktop/hola.pdf'

    # Configurar temporizador para 30 segundos
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(30)

    try:
        # Abuso en lectura de disco
        start_time = time.time()
        for i in range(100):
            read_disk(filepath)
        end_time = time.time()
        print(f'Tiempo total de abuso en lectura de disco: {end_time - start_time} segundos')

        # Uso intensivo de criptografía
        data = b'Este es un mensaje de prueba'
        start_time = time.time()
        for i in range(100000):
            ciphertext, nonce, tag = encrypt(data)
            plaintext = decrypt(ciphertext, nonce, tag)
        end_time = time.time()
        print(f'Tiempo total de uso intensivo de criptografía: {end_time - start_time} segundos')

        # Cambios en la entropía del archivo
        modify_entropy(filepath)

    except Exception as e:
        print(e)