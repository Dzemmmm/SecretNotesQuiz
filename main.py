import tkinter as tk
from PIL import ImageTk, Image
import base64
from tkinter import messagebox

def resize_image(image_path, width, height):
    original_image = Image.open(image_path)
    resized_image = original_image.resize((width, height), Image.LANCZOS)
    return ImageTk.PhotoImage(resized_image)

def encode(key, clear):
    enc = []
    for i in range(len(clear)):
        key_c = key[i % len(key)]
        enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
        enc.append(enc_c)
    return base64.urlsafe_b64encode("".join(enc).encode()).decode()

def decode(key, enc):
    dec = []
    enc = base64.urlsafe_b64decode(enc).decode()
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)

def save_and_encrypt_notes():
    title = entry.get()
    message = text.get("1.0", "end-1c")  # Use "end-1c" to remove the trailing newline
    master_secret = keyinput.get()

    if not (title and message and master_secret):
        messagebox.showinfo(title="Error!", message="Please enter all information.")
    else:
        message_encrypted = encode(master_secret, message)

        with open("_md5.txt", "a") as data_file:
            data_file.write(f'\n{title}\n{message_encrypted}')

        entry.delete(0, "end")
        keyinput.delete(0, "end")
        text.delete("1.0", "end")

def decrypt_notes():
    message_encrypted = text.get("1.0", "end-1c")  # Use "end-1c" to remove the trailing newline
    master_secret = keyinput.get()

    if not (message_encrypted and master_secret):
        messagebox.showinfo(title="Error!", message="Please enter all information.")
    else:
        try:
            decrypted_message = decode(master_secret, message_encrypted)
            text.delete("1.0", "end")
            text.insert("1.0", decrypted_message)
        except:
            messagebox.showinfo(title="Error!", message="Please make sure of encrypted info.")

screen = tk.Tk()
screen.geometry("500x700")
screen.title("Notes Encryptor")
screen.config(bg="#E0E0E0")

image_path = "md5.png"
new_width = 140
new_height = 150
resized_image = resize_image(image_path, new_width, new_height)
label = tk.Label(screen, image=resized_image)
label.pack()

title1 = tk.Label(text="Enter Your Title:", font=("Helvetica", 12))
title1.pack()

entry = tk.Entry(width=30)
entry.pack()

title2 = tk.Label(text="Enter Your Message:", font=("Helvetica", 12))
title2.pack()

text = tk.Text(width=30, height=15)
text.pack()

title3 = tk.Label(text="Enter Your MasterKey:", font=("Helvetica", 12))
title3.pack()

keyinput = tk.Entry(width=30)
keyinput.pack()

save1 = tk.Button(text="Save & Encrypt", width=20, command=save_and_encrypt_notes)
save1.pack()
save2 = tk.Button(text="Decrypt", width=10, command=decrypt_notes)
save2.pack()

screen.mainloop()
