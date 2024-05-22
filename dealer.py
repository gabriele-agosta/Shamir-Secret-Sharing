import tkinter as tk
import numpy as np
import random

from tkinter import filedialog

class Dealer:
    def __init__(self, threshold):
        self.threshold = threshold
        self.secret = None
        self.q = None
        self.polynomials = []


    def chooseSecret(self):
        ascii_secret = None
       
        while True:
            choice = input("Choose what you want to encrypt: \n1.Text/Number; \n2.File content. \n")
            if choice.isdigit() and (1 <= int(choice) <= 2):
                break
            
        ascii_secret = []
        if choice == "1":
            secret = input("Insert your secret: ")
            ascii_secret = ascii_secret = [ord(c) for c in secret]
        else:
            root = tk.Tk()
            root.withdraw()
            file_path = filedialog.askopenfilename()

            if file_path:
                with open(file_path, "r") as file:
                    secret = file.read()
                    ascii_secret = [ord(c) for c in secret]
            else:
                print("No file selected.")
            root.destroy()
        self.secret = ascii_secret


    def chooseQ(self):
        self.q = 127

    
    def set_polynomials(self):
        for secretDigit in self.secret:
            coefficients = [random.randint(1, self.q) for _ in range(self.threshold - 1)]
            self.polynomials.append(np.polynomial.Polynomial([secretDigit] + coefficients))


    def distributeShares(self, player):
        for polynomial in self.polynomials:
            val = polynomial(player.x) % self.q
            player.addShare(int(val))
            