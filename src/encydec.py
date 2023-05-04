import os
import pyAesCrypt


# encryption function
def encrypt_pdf(input_file, password):
    # generate encrypted file name
    enc_file = input_file + ".aes"

    # encryption buffer size - 64K
    buffer_size = 64 * 1024

    # get file size
    file_size = os.stat(input_file).st_size

    # encrypt file
    with open(input_file, 'rb') as f_in:
        with open(enc_file, 'wb') as f_out:
            pyAesCrypt.encryptStream(f_in, f_out, password, buffer_size)

    # delete original file
    os.remove(input_file)

    # return encrypted file name
    return enc_file


# decryption function
def decrypt_pdf(input_file, password):
    # generate decrypted file name
    dec_file = os.path.splitext(input_file)[0]
    # encryption buffer size - 64K
    buffer_size = 64 * 1024
    # get file size
    file_size = os.stat(input_file).st_size

    # decrypt file
    with open(input_file, 'rb') as f_in:
        with open(dec_file, 'wb') as f_out:
        # with open('static/downloads/' + dec_file, "wb") as f_out:

            try:
                pyAesCrypt.decryptStream(f_in, f_out, password, buffer_size, file_size)
            except ValueError:
                # remove partially written file on error
                os.remove(dec_file)

    # return decrypted file name
    return dec_file



# set input file and password
input_file = r'./static/downloads/front_page.pdf.aes'
password = 'mysecretpassword'

# encrypt file
encrypted_file = encrypt_pdf(input_file, password)
print(encrypted_file)
# decrypt file
decrypted_file = decrypt_pdf(encrypted_file, password)
print(decrypted_file)
