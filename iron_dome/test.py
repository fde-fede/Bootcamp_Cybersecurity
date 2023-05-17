import hashlib
import os
import time
import psutil
import threading

def change_entropy(file):
    with open(file, 'a') as f:
        f.write('hola')
        time.sleep(10)

def simulate_cryptographic_activity(directory):
    # Calculate the SHA-256 hash of all files in the directory
    tmp = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, "rb") as f:
                data = f.read()
                hash_value = hashlib.sha256(data).hexdigest()
                print(f"Calculated hash value of {file_path}: {hash_value}")
    while True:
        if tmp == 0:
            t = threading.Thread(target=run_entropy_change, args=("/home/kali/Desktop/tests/test1.txt",))
            t.start()
            tmp = 1
        # Encrypt and decrypt a large file using AES-256
        file_path = os.path.join(directory, "testfile")
        with open(file_path, "wb") as f:
            f.write(os.urandom(1024 * 1024 * 200))  # Write 200 MB of random data
        os.system(f"openssl enc -aes-256-cbc -salt -in {file_path} -out {file_path}.enc -pass pass:MySecretPassword")
        os.system(f"openssl enc -d -aes-256-cbc -in {file_path}.enc -out {file_path}.dec -pass pass:MySecretPassword")

        # Remove the large file and its encrypted and decrypted versions
        os.remove(f"{file_path}.enc")
        os.remove(f"{file_path}.dec")
        os.remove('/home/kali/Desktop/tests/testfile')
        # Simulate disk read abuse by repeatedly reading all files in the directory
        for i in range(10000):
            for root, dirs, files in os.walk(directory):
                for file in files:
                    for i in range(5000):
                        file_path = os.path.join(root, file)
                        with open(file_path, "rb") as f:
                            f.read()


def run_entropy_change(file):
    while True:
        change_entropy(file)
def main():
    directory = "/home/kali/Desktop/tests"
    simulate_cryptographic_activity(directory)

if __name__ == "__main__":
    main()