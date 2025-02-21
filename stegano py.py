from tkinter import Tk, Label, Entry, Button, messagebox, filedialog
import cv2
import os
import hashlib

# Global variables
img = None
hashed_password = None
msg_length = 0

def load_image():
    global img
    image_path = filedialog.askopenfilename(title="Select an image file")
    img = cv2.imread(image_path)
    if img is None:
        messagebox.showerror("Error", "Image not found or unable to load.")
        exit()
    messagebox.showinfo("Success", "Image loaded successfully.")

def encrypt():
    global img, hashed_password, msg_length
    msg = msg_entry.get()
    password = password_entry.get()
    
    # Check if the message is too long for the image
    if len(msg) > img.shape[0] * img.shape[1]:
        messagebox.showerror("Error", "Message is too long to embed in the image.")
        return
    
    # Hash the password
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    # Embed the message
    d = {chr(i): i for i in range(255)}
    n, m, z = 0, 0, 0
    
    for char in msg:
        img[n, m, z] = d[char]
        n, m, z = (n + 1) % img.shape[0], (m + 1) % img.shape[1], (z + 1) % 3
    
    # Save the encrypted image
    cv2.imwrite("encryptedImage.png", img)
    os.system("start encryptedImage.png")
    
    # Store the message length for decryption
    msg_length = len(msg)
    
    # Show success message
    messagebox.showinfo("Success", "Message embedded successfully.")

def decrypt():
    global img, hashed_password, msg_length
    password = password_entry.get()
    
    # Verify the password
    if hashlib.sha256(password.encode()).hexdigest() != hashed_password:
        messagebox.showerror("Error", "Incorrect password.")
        return
    
    # Extract the message
    c = {i: chr(i) for i in range(255)}
    n, m, z = 0, 0, 0
    message = ""
    
    for _ in range(msg_length):
        message += c[img[n, m, z]]
        n, m, z = (n + 1) % img.shape[0], (m + 1) % img.shape[1], (z + 1) % 3
    
    # Show the decrypted message
    messagebox.showinfo("Decrypted Message", f"Decrypted message: {message}")

# Create the GUI
root = Tk()
root.title("Steganography Tool")

Label(root, text="Enter secret message:").grid(row=0, column=0)
msg_entry = Entry(root)
msg_entry.grid(row=0, column=1)

Label(root, text="Enter a passcode:").grid(row=1, column=0)
password_entry = Entry(root, show="*")
password_entry.grid(row=1, column=1)

Button(root, text="Load Image", command=load_image).grid(row=2, column=0)
Button(root, text="Encrypt", command=encrypt).grid(row=2, column=1)
Button(root, text="Decrypt", command=decrypt).grid(row=2, column=2)

root.mainloop()
