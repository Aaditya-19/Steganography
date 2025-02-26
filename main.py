import cv2
import os
import tkinter as tk
from tkinter import simpledialog, messagebox

def embed_message(img, msg, password):
    height, width, _ = img.shape
    msg += "::END"
    
    if len(msg) > height * width * 3:
        messagebox.showerror("Error", "Message too long for this image!")
        return None
    
    d = {chr(i): i for i in range(256)}
    n, m, z = 0, 0, 0
    
    for char in msg:
        img[n, m, z] = d[char]
        m += 1
        if m >= width:
            m = 0
            n += 1
        z = (z + 1) % 3
    
    cv2.imwrite("encryptedImage.jpg", img)
    messagebox.showinfo("Success", "Message successfully embedded into encryptedImage.jpg")
    
    return img

def extract_message(img, password, correct_password):
    if password != correct_password:
        messagebox.showerror("Error", "YOU ARE NOT AUTHORIZED!")
        return
    
    height, width, _ = img.shape
    c = {i: chr(i) for i in range(256)}
    
    message, n, m, z = "", 0, 0, 0
    
    while True:
        if n >= height or m >= width:
            break
        
        char = c[img[n, m, z]]
        if message.endswith("::END"):
            message = message[:-5]
            break
        
        message += char
        m += 1
        if m >= width:
            m = 0
            n += 1
        z = (z + 1) % 3
    
    messagebox.showinfo("Decrypted Message", message)

def main():
    root = tk.Tk()
    root.withdraw()
    
    img = cv2.imread("mypic.jpg")
    if img is None:
        messagebox.showerror("Error", "Image not found!")
        return
    
    msg = simpledialog.askstring("Input", "Enter secret message:")
    password = simpledialog.askstring("Input", "Enter a passcode:", show='*')
    
    encrypted_img = embed_message(img, msg, password)
    
    os.system("start encryptedImage.jpg" if os.name == "nt" else "xdg-open encryptedImage.jpg")
    
    pas = simpledialog.askstring("Input", "Enter passcode for decryption:", show='*')
    extract_message(encrypted_img, pas, password)

if __name__ == "__main__":
    main()
